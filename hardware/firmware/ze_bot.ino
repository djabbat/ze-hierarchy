/*
 * ze_bot.ino — прошивка бота Ze-Hierarchy
 * Платформа: ESP32-C3 (RISC-V)
 * 
 * Функции:
 * - Измерение V_cap (RC-таймер возраста) через ADC
 * - Управление LED + пьезо через LM393 компаратор
 * - Фототаксис: движение к яркому LED другого бота
 * - Звуковой репульсор: избегание столкновений
 * - ESP-NOW: передача ID + V_cap + возраст + τ_sick
 */

#include <esp_now.h>
#include <WiFi.h>
#include <esp_wifi.h>

// ======================== ПИНЫ ========================
#define PIN_LED          1   // GPIO1 — LED через LM393
#define PIN_BUZZER       2   // GPIO2 — пьезо через 2N3904
#define PIN_ADC_V_COND   3   // GPIO3 — V_cap (через делитель 100k/100k)
#define PIN_PHOTODIODE   4   // GPIO4 — фотодиод (через 10k pull-up)
#define PIN_MICROPHONE   5   // GPIO5 — MAX9814 микрофон
#define PIN_MOTOR        6   // GPIO6 — мотор через 2N3904
#define PIN_BUTTON_RESET 7   // GPIO7 — кнопка сброса
#define PIN_LM393_OUT    8   // GPIO8 — выход компаратора LM393

// ======================== ПАРАМЕТРЫ ========================
#define BOT_ID            1   // ID бота (1-120)
#define AGE_DAYS          0   // возраст в днях (0 = новый)
#define V0                5.0 // начальное напряжение RC
#define RC_TAU_DAYS       115.0 // постоянная времени RC
#define V_LED_TH          1.8 // порог LED
#define V_BUZZER_TH       2.5 // порог зуммера
#define V_REF             2.5 // опорное напряжение компаратора

#define PHOTOTAXIS_RADIUS 30.0  // см — радиус фототаксиса
#define SONAR_RADIUS      3.0   // см — радиус звукового репульсора
#define MOTOR_SPEED_BASE  150   // базовая скорость мотора (PWM 0-255)
#define MOTOR_SPEED_MAX   255   // макс скорость

#define ESP_NOW_CHANNEL   1     // WiFi канал для ESP-NOW

// ======================== ESP-NOW ПАКЕТ ========================
typedef struct {
  uint8_t id;           // 1B — ID бота
  uint16_t v_cap_adc;   // 2B — ADC V_cap
  uint16_t age_days;    // 2B — возраст в днях
  uint8_t tau_sick;     // 1B — τ_sick (0-255)
  uint8_t crc;          // 1B — контрольная сумма
} __attribute__((packed)) BotPacket;

BotPacket tx_packet;
BotPacket rx_packets[120]; // буфер принятых пакетов
int rx_count = 0;

// ======================== MAC-АДРЕС МАСТЕРА ========================
// MAC адрес ESP32-мастера (на USB)
uint8_t master_mac[] = {0x34, 0x85, 0x18, 0x00, 0x00, 0x00};

// ======================== СОСТОЯНИЕ ========================
float v_cap;          // текущее напряжение конденсатора
float led_brightness; // яркость LED (0.0 - 1.0)
bool buzzer_on;       // зуммер включён?
float buzzer_freq;    // частота зуммера (Гц)
float phototaxis_x;   // направление фототаксиса X
float phototaxis_y;   // направление фототаксиса Y
float sonar_x;        // направление репульсора X
float sonar_y;        // направление репульсора Y
int motor_pwm;        // PWM мотора

// ======================== ФУНКЦИИ ========================

// Измерение V_cap через ADC
float read_v_cap() {
  int adc_raw = analogRead(PIN_ADC_V_COND);
  // Делитель 100k/100k → V_adc = V_cap / 2
  // ADC ESP32-C3: 12-bit, 0-3.3V → V_cap = adc_raw * 3.3 / 4096 * 2
  float v_adc = (float)adc_raw * 3.3 / 4096.0;
  return v_adc * 2.0; // компенсация делителя
}

// Вычисление возраста из V_cap
float compute_age_days(float v) {
  if (v <= 0.0) return 999.0;
  return -RC_TAU_DAYS * log(v / V0);
}

// Яркость LED
float compute_led_brightness(float v) {
  float b = (v - V_LED_TH) / (V0 - V_LED_TH);
  if (b < 0.0) b = 0.0;
  if (b > 1.0) b = 1.0;
  return b;
}

// Состояние зуммера
bool is_buzzer_on(float v) {
  return v > V_BUZZER_TH;
}

// Частота зуммера
float compute_buzzer_freq(float v) {
  if (v <= V_BUZZER_TH) return 0.0;
  if (v > V_BUZZER_TH) return 4000.0; // молодой — высокий тон
  return 1000.0; // старый — низкий тон (если когда-нибудь переключится)
}

// PWM для заданной частоты (использует LEDC)
void set_buzzer_freq(float freq) {
  if (freq <= 0.0) {
    ledcWrite(0, 0); // выключить
    return;
  }
  // LEDC канал 0, разрешение 8-bit
  ledcWriteTone(0, freq);
}

// Фототаксис: анализ градиента света
void update_phototaxis() {
  // Читаем фотодиод
  int light_raw = analogRead(PIN_PHOTODIODE);
  
  // Если есть принятые пакеты от других ботов ищем ярких
  float target_x = 0.0, target_y = 0.0;
  int count = 0;
  
  for (int i = 0; i < rx_count; i++) {
    // Проверяем яркость LED другого бота по его V_cap
    float other_v = (float)rx_packets[i].v_cap_adc * 3.3 / 4096.0 * 2.0;
    float other_led = compute_led_brightness(other_v);
    
    if (other_led > 0.7) { // яркий бот
      // Упрощённо: случайное направление (в реальности — trilateration)
      target_x += (float)random(-100, 100) / 100.0;
      target_y += (float)random(-100, 100) / 100.0;
      count++;
    }
  }
  
  if (count > 0) {
    phototaxis_x = target_x / count;
    phototaxis_y = target_y / count;
  } else {
    // Случайное блуждание
    phototaxis_x = (float)random(-50, 50) / 100.0;
    phototaxis_y = (float)random(-50, 50) / 100.0;
  }
}

// Контрольная сумма (XOR всех байт)
uint8_t compute_crc(uint8_t *data, int len) {
  uint8_t crc = 0;
  for (int i = 0; i < len; i++) {
    crc ^= data[i];
  }
  return crc;
}

// ======================== ESP-NOW ОБРАБОТЧИКИ ========================

// Обработчик отправки
void on_data_sent(const uint8_t *mac, esp_now_send_status_t status) {
  // Не используется
}

// Обработчик приёма
void on_data_recv(const uint8_t *mac, const uint8_t *data, int len) {
  if (len != sizeof(BotPacket)) return;
  
  BotPacket *pkt = (BotPacket*)data;
  
  // Проверка CRC
  uint8_t crc = compute_crc((uint8_t*)pkt, sizeof(BotPacket) - 1);
  if (crc != pkt->crc) return;
  
  // Сохраняем в буфер
  if (rx_count < 120) {
    rx_packets[rx_count++] = *pkt;
  }
}

// ======================== SETUP ========================

void setup() {
  Serial.begin(115200);
  Serial.printf("\n\n=== Ze-Bot #%d ===\n", BOT_ID);
  Serial.printf("Age: %d days\n", AGE_DAYS);
  
  // Инициализация пинов
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_MOTOR, OUTPUT);
  pinMode(PIN_PHOTODIODE, INPUT);
  pinMode(PIN_MICROPHONE, INPUT);
  pinMode(PIN_BUTTON_RESET, INPUT_PULLUP);
  pinMode(PIN_LM393_OUT, INPUT);
  
  // PWM настройка
  ledcSetup(0, 4000, 8); // канал 0, 4 кГц, 8 бит
  ledcAttachPin(PIN_BUZZER, 0);
  
  ledcSetup(1, 1000, 8); // канал 1, 1 кГц (мотор)
  ledcAttachPin(PIN_MOTOR, 1);
  
  // Измеряем V_cap при старте
  v_cap = read_v_cap();
  Serial.printf("V_cap: %.3f V\n", v_cap);
  
  // Настраиваем WiFi для ESP-NOW
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  
  // ESP-NOW инициализация
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed!");
    return;
  }
  
  // Регистрируем обработчики
  esp_now_register_send_cb(on_data_sent);
  esp_now_register_recv_cb(on_data_recv);
  
  // Добавляем мастера
  esp_now_peer_info_t peer;
  memset(&peer, 0, sizeof(peer));
  memcpy(peer.peer_addr, master_mac, 6);
  peer.channel = ESP_NOW_CHANNEL;
  peer.encrypt = false;
  
  if (esp_now_add_peer(&peer) != ESP_OK) {
    Serial.println("Master peer add failed!");
    return;
  }
  
  // Заполняем пакет
  tx_packet.id = BOT_ID;
  tx_packet.v_cap_adc = (uint16_t)((v_cap / 2.0) / 3.3 * 4096.0); // ADC value
  tx_packet.age_days = (uint16_t)AGE_DAYS;
  tx_packet.tau_sick = 0; // будет обновляться
  tx_packet.crc = compute_crc((uint8_t*)&tx_packet, sizeof(BotPacket) - 1);
  
  Serial.println("Ze-Bot ready!");
}

// ======================== LOOP ========================

void loop() {
  // 1. Измеряем V_cap
  v_cap = read_v_cap();
  
  // 2. Обновляем выходы
  led_brightness = compute_led_brightness(v_cap);
  buzzer_on = is_buzzer_on(v_cap);
  buzzer_freq = compute_buzzer_freq(v_cap);
  
  // 3. Управление LED (через LM393)
  if (led_brightness > 0.1) {
    analogWrite(PIN_LED, (int)(led_brightness * 255));
  } else {
    digitalWrite(PIN_LED, LOW);
  }
  
  // 4. Управление зуммером
  if (buzzer_on) {
    set_buzzer_freq(buzzer_freq);
  } else {
    ledcWrite(0, 0);
  }
  
  // 5. Фототаксис
  rx_count = 0; // сбрасываем буфер
  update_phototaxis();
  
  // 6. Движение
  // Направление = фототаксис + случайный шум
  float move_x = phototaxis_x;
  float move_y = phototaxis_y;
  float move_norm = sqrt(move_x * move_x + move_y * move_y);
  
  if (move_norm > 0.1) {
    motor_pwm = MOTOR_SPEED_BASE + (int)(50.0 * move_norm);
    if (motor_pwm > MOTOR_SPEED_MAX) motor_pwm = MOTOR_SPEED_MAX;
  } else {
    motor_pwm = MOTOR_SPEED_BASE / 2; // медленное случайное блуждание
  }
  
  ledcWrite(1, motor_pwm);
  
  // 7. Отправка ESP-NOW пакета
  tx_packet.v_cap_adc = (uint16_t)((v_cap / 2.0) / 3.3 * 4096.0);
  tx_packet.age_days = (uint16_t)compute_age_days(v_cap);
  tx_packet.crc = compute_crc((uint8_t*)&tx_packet, sizeof(BotPacket) - 1);
  
  esp_err_t result = esp_now_send(master_mac, (uint8_t*)&tx_packet, sizeof(tx_packet));
  
  // 8. Ждём
  delay(100); // 10 Hz цикл
}
