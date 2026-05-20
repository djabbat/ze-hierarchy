# Ze-Hierarchy — Карта проекта

**Проверка Ze-эффекта:** иерархия следования в колонии RNG-автоматов разного физического возраста.

## Структура

```
Ze-Hierarchy/
│
├── CONCEPT.md          ← концепция эксперимента (Ze-интервенция → иерархия)
├── PARAMETERS.md       ← численные параметры (N, возраст, RC, фототаксис)
├── TODO.md             ← план работ (симуляция → прототип → эксперимент)
├── MAP.md              ← этот файл (карта)
├── STATE.md            ← текущий статус
├── MEMORY.md           ← история решений, запреты
│
├── _pi.md              ← правила для pi-агента
│
├── simulator/          ← Python-симуляция
│   ├── bot.py          ← модель бота (RC-возраст, LED, random walk)
│   ├── arena.py        ← арена (60×60, градиент света, стены)
│   ├── physics.py      ← физика: движение, столкновения (пока нет)
│   └── run.py          ← запуск: N ботов, T секунд, запись
│
├── analysis/           ← анализ данных
│   ├── metrics.py      ← HI, R_leader, τ_conv
│   └── visualize.py    ← анимация, heatmap
│
├── hardware/           ← железо
│   ├── README.md       ← спецификация
│   ├── schematic.md    ← схема
│   └── bom.md          ← Bill of Materials
│
└── refs/               ← ссылки, заметки (будущее)
```

## Внешние связи

| Связь | Файл |
|---|---|
| Ze Vectors Theory | `../README.md` |
| Эксперимент Пьоша | `../docs/Peoch_Experiment_and_Ze.md` |
| Пространство как ошибка Ze | `../docs/Space_As_Ze_Error.md` |
| Коллективный RNG-эксперимент | `../docs/Experiment_Collective_RNG_Automata.md` |

## Статус файлов

| Файл | Статус |
|---|---|
| CONCEPT.md | ✅ Готов |
| PARAMETERS.md | ✅ Готов |
| TODO.md | ✅ Готов |
| MAP.md | ✅ Этот файл |
| STATE.md | 🔧 Создаётся |
| MEMORY.md | 🔧 Создаётся |
| _pi.md | 🔧 Создаётся |
| simulator/bot.py | ✅ Готов |
| simulator/arena.py | ✅ Готов |
| simulator/run.py | 🔧 Создаётся |
| analysis/metrics.py | ❌ Не создан |
| analysis/visualize.py | ❌ Не создан |
| hardware/* | ❌ Не создан |
