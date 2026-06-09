# MEMORY — Ze-Hierarchy

**Decision history, open questions, bans.**

---

## 2026-05-20: Project created

**Decision:** Separate subproject `Ze-Hierarchy` inside Ze.
**Reason:** Experiment testing Ze effect on physical RNG automata — separate line, not mixing with Ze theory (Poincare) or existing simulators.

**Structure:**
- Core files at root level (CONCEPT, PARAMETERS, TODO, MAP, STATE, MEMORY)
- simulator/ — Python simulation
- analysis/ — metrics and visualization
- hardware/ — prototype

---

## 2026-05-20: Robot type

**Decision:** Bristlebots (vibration robots) with LED + photodiode for phototaxis.
**Reason:** Cheap ($0.50-0.75/unit), pure mechanical randomness, can build 120 for $540.

**Alternatives considered:**
- ESP32-robots ($15/unit) — too expensive for 120
- Balls on vibration table — no individual marking, no age tracking
- Pure simulation — no physical effect (if Ze is physical)

---

## 2026-05-20: Age as only variable

**Decision:** Age set by RC timer (supercapacitor 1F + 10MΩ, τ ≈ 115 days).
**Reason:** RC — analog, irreversible, predictable "age memory" without microcontroller. Age = calendar time since manufacturing.

**Ban:** Do NOT replace age with battery discharge.
**Ban:** Do NOT replace age with software counter (not "physical age").

---

## 2026-05-20: Power

**Decision:** Swappable batteries (Li-Po 100 mAh) + charging station.
**Reason:** Qi pad 60×60 cm unrealistic for $30 (PR criticism). Swappable batteries cheaper and more reliable.

**Ban:** Qi charging — do not use (budget artifact).

---

## 2026-05-20: Rename "cheating" → "intervention"

**Decision:** Term "cheating" replaced with "intervention" in all core files.
**Reason:** "Intervention" is a scientific term from causal inference (Pearl's do-operator), no moral connotation. Pair: intervention (act) vs monitoring (observe).

---

## 2026-05-20: Post-PR fixes

1. **Collisions:** added sound repulsor + physics collision model
2. **Qi charging:** replaced with swappable batteries
3. **Statistical power:** 2×60 instead of 4×30
4. **JFET replaced:** LM393 comparator (stable threshold)
5. **Mass:** ballast 15±0.5 g
6. **RC age:** ADC measurement via ESP32
7. **Control tests:** A–F
8. **GitHub:** https://github.com/djabbat/ze-hierarchy

---

## 2026-05-22: NLnet Commons Fund — заявка зарегистрирована

**Событие:** Получено подтверждение от NLnet Foundation (dashboard@nlnet.nl) о регистрации заявки на грант Commons Fund.

**Код заявки:** 2026-06-21e
**Проект:** Ze-Hierarchy: Age-Based Physical Hierarchy in Identical Random-Walk Robots
**Сумма:** €4,675
**Организация:** Georgia Longevity Alliance
**Статус:** Зарегистрирована, ожидание письма после дедлайна (ориентировочно ~21 июня 2026)

**Решение:** Добавить задачу в Plane для отслеживания. Обновить STATE.md и TODO.md.
**Ban:** Не заливать в Outline без команды пользователя.

---

## 2026-06-01 — Multilayer Age Model introduced

**Решение:** Расширить концепцию возраста в Ze-Hierarchy с плоской (τ_create) до четырёхслойной.

**Изменения в концепте:**
- Раздел 6.1: Expanded Test Matrix — тесты F1–F4, G (вместо одного F)
- Раздел 11: Multilayer Age Model Extension (полное описание)
- Новый параметр τ_profile для каждого бота
- ESP-NOW пакет расширен с 6B до 10B (добавлены batch IDs компонентов)

**Ban:** Не заменять τ_profile одним числом. Всегда хранить вектор возрастов.
**Ban:** Не пропускать тесты F2-F4, G — они критичны для верификации модели.

## Open Questions

- Is vibrational clustering (Mahadevan 2012) necessary for HI > 0.5 in real bristlebots?
- Optimal K_photo for real photodiodes?
- Does ESP-NOW TDMA work at 120 devices without packet loss?
- Can τ_sick be measured in simulation before hardware?
- Which component carries age memory best — silicon, solder, or plastic?
