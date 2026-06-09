# TODO — Ze-Hierarchy

## Phase 1: Simulation (DONE)

- [x] CONCEPT.md (3x peer review)
- [x] PARAMETERS.md (LED, buzzer, radio, 2 groups)
- [x] simulator/bot.py — LED, piezo, phototaxis, repulsor, random walk
- [x] simulator/arena.py — arena, light gradient, sound repulsor, walls
- [x] simulator/physics.py — collision repulsion model
- [x] simulator/run.py — run simulation
- [x] analysis/metrics.py — HI, R_leader, τ_conv
- [x] analysis/visualize.py — animation, plots
- [x] analysis/run_30_seeds.py — batch statistics
- [x] HI max = 0.532 (proof of concept)
- [x] Control tests: HI ≈ 0.5

## Phase 2: Prototype

- [ ] Build 1 prototype breadboard
- [ ] Calibrate RC timer (measure V_cap via ESP32 ADC)
- [ ] Test ESP-NOW TDMA (2→120 devices)
- [ ] Test piezo buzzer (frequency vs age)
- [ ] Test phototaxis (old bot follows bright LED)
- [ ] Test sound repulsor (bots avoid collisions)

## Phase 3: Pilot

- [ ] Build 30 bots (15 new + 15 old)
- [ ] Test A: all same age
- [ ] Test C: 15 new + 15 old
- [ ] Test D: LED + buzzer off
- [ ] Record: camera + radio + microphone array
- [ ] Compute HI from real data

## Phase 4: Full Experiment

- [ ] 120 bots
- [ ] All control tests A–F
- [ ] Blind analysis
- [ ] Statistics (HI, t-test, Cohen's d)

## Phase 5: Publication

- [ ] HardwareX paper (open hardware design)
- [ ] arXiv preprint
- [ ] Dataset on Zenodo

## Grant Tracking

- [x] Shuttleworth Flash Grant — submitted (2026-05-20)
- [x] NLnet Commons Fund — заявка зарегистрирована (2026-05-22, код 2026-06-21e)
- [ ] NLnet — дождаться письма после дедлайна (~21 июня 2026)
- [ ] NLnet — если одобрят, обновить TODO и начать Phase 2 (Prototype)

## After Peer Review (complete)

- [x] Radio identification (ESP-NOW TDMA)
- [x] Sound (piezo, repulsor)
- [x] 2×60 instead of 4×30
- [x] Qi → swappable batteries
- [x] JFET → LM393 comparator
- [x] Ballast to 15g
- [x] Control tests A–F
- [x] English documentation
- [x] GitHub: https://github.com/djabbat/ze-hierarchy
- [x] Grant: Shuttleworth Flash Grant submitted
