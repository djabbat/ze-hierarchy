"""
bot.py — модель бота с LED, звуком (пищалка), фото- и фонотаксисом.
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Bot:
    """Один вибробот с RC-возрастом, LED, зуммером, фото- и фонотаксисом."""
    
    id: int
    x: float = 0.0
    y: float = 0.0
    theta: float = 0.0
    speed: float = 0.0
    
    # === Возраст (RC-таймер) ===
    age_days: float = 0.0
    V0: float = 5.0
    RC_tau: float = 115.0       # дней
    V_th_led: float = 1.8       # порог LED
    V_th_buzzer: float = 2.5    # порог зуммера
    
    # === Фототаксис ===
    phototaxis_radius: float = 15.0    # см
    phototaxis_gain: float = 3.0       # сильное притяжение к свету
    # === Звуковой репульсор (избегание столкновений) ===
    sonar_radius: float = 2.5          # см — только чтобы не слипались
    sonar_repulsion: float = 1.0       # слабый отворот
    # === Движение ===
    noise_angle: float = np.deg2rad(15)
    base_speed: float = 3.0
    max_speed: float = 5.0
    turn_rate: float = np.deg2rad(60)
    noise_speed: float = 0.3
    
    def __post_init__(self):
        self.update_outputs()
    
    @property
    def V_age(self) -> float:
        return self.V0 * np.exp(-self.age_days / self.RC_tau)
    
    def led_brightness(self) -> float:
        """Яркость LED: 0 (погас) .. 1 (максимум)."""
        b = (self.V_age - self.V_th_led) / (self.V0 - self.V_th_led)
        return float(np.clip(b, 0.0, 1.0))
    
    def buzzer_volume(self) -> float:
        """
        Громкость зуммера: 1.0 для всех (одинаковая).
        Зуммер или включён (если V_age > V_th_buzzer), или молчит.
        """
        if self.V_age < self.V_th_buzzer:
            return 0.0  # слишком старый — зуммер сдох
        return 1.0  # все пищат одинаково громко
    
    def buzzer_freq(self) -> float:
        """
        Частота зуммера: резкий переход по возрасту.
        Молодые (< threshold дней): 4000 Гц (высокий, резкий)
        Старые (> threshold дней): 1000 Гц (низкий, гулкий)
        
        Переключатель — компаратор LM393 с порогом V_buzzer_th.
        Пока V_age > V_buzzer_th — высокая частота.
        Как только V_age падает ниже V_buzzer_th — низкая.
        """
        if self.buzzer_volume() < 0.01:
            return 0.0  # умер
        
        # Резкий переход: компаратор с гистерезисом
        if self.V_age > self.V_th_buzzer:
            return 4000.0  # молодой — высокий тон
        else:
            return 1000.0  # старый — низкий тон
    
    def update_outputs(self):
        self.led = self.led_brightness()
        self.piezo = self.buzzer_volume()   # 0..1
        self.piezo_freq = self.buzzer_freq()
    
    def move(self, dt: float, 
             grad_light_x: float = 0.0, grad_light_y: float = 0.0,
             repulsion_x: float = 0.0, repulsion_y: float = 0.0):
        """
        Шаг движения.
        
        grad_light — градиент света (фототаксис, притяжение к ярким)
        repulsion — направление от ближайших зуммеров (звуковой репульсор)
        """
        grad_norm = np.hypot(grad_light_x, grad_light_y)
        rep_norm = np.hypot(repulsion_x, repulsion_y)
        
        # Взвешенное направление: фототаксис (притяжение) + сонар (отталкивание)
        gx = grad_light_x * self.phototaxis_gain + repulsion_x * self.sonar_repulsion
        gy = grad_light_y * self.phototaxis_gain + repulsion_y * self.sonar_repulsion
        total_norm = np.hypot(gx, gy)
        
        if total_norm > 0.01 and grad_norm > 0.001:
            # Фототаксис перевешивает случайное блуждание
            target_theta = np.arctan2(gy, gx)
            dtheta = np.arctan2(np.sin(target_theta - self.theta),
                                np.cos(target_theta - self.theta))
            max_dtheta = self.turn_rate * dt
            dtheta = np.clip(dtheta, -max_dtheta, max_dtheta)
            self.theta += dtheta
            
            target_speed = self.base_speed + 0.3 * grad_norm
            self.speed += (target_speed - self.speed) * 0.1
        else:
            # RANDOM WALK: случайный поворот
            dtheta = np.random.normal(0.0, self.noise_angle)
            self.theta += dtheta * dt * 10
            self.speed += np.random.normal(0.0, self.noise_speed) * dt
            self.speed = np.clip(self.speed, 0.5, self.max_speed)
        
        # Двигаемся
        self.x += self.speed * np.cos(self.theta) * dt
        self.y += self.speed * np.sin(self.theta) * dt


def create_bot(id: int, age_days: float, arena_size: float = 100.0) -> Bot:
    """Создать бота в случайной позиции."""
    return Bot(
        id=id,
        age_days=age_days,
        x=np.random.uniform(3.0, arena_size - 3.0),
        y=np.random.uniform(3.0, arena_size - 3.0),
        theta=np.random.uniform(0, 2 * np.pi),
        speed=np.random.uniform(1.0, 3.0),
    )


def create_population(ages: list[float], bots_per_group: int,
                      arena_size: float = 100.0) -> list[Bot]:
    """Создать популяцию ботов."""
    bots = []
    idx = 0
    for age in ages:
        for _ in range(bots_per_group):
            bots.append(create_bot(idx, age_days=age, arena_size=arena_size))
            idx += 1
    return bots
