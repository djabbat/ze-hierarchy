# PARAMETERS — Ze-Hierarchy

## Robot Parameters

| Parameter | Value | Description |
|---|---|---|
| N | 120 | Total robots |
| Groups | 2 | New (0 days) vs Old (30 days) |
| Per group | 60 | Robots per age group |
| Mass | 15 ± 0.5 g | All with ballast to equal weight |

### RC Timer (age)

| Parameter | Value | Notes |
|---|---|---|
| C | 1 F (supercapacitor) | Leakage < 0.01 mA (ADC-measured) |
| R | 10 MΩ ± 5% | — |
| τ = RC | 10⁷ s ≈ 115.7 days | V(t) = V₀·exp(-t/τ) |
| V₀ | 5.0 V | Charged at manufacturing |
| V_LED_th | 1.8 V | LED threshold |
| V_buzzer_th | 2.5 V | Buzzer threshold (above = 4 kHz, below = 1 kHz) |
| ADC | ESP32, 12-bit | Measures real V_cap every 100 ms |

### Outputs by age

| Age | V_cap | LED | Sound |
|---|---|---|---|
| 0 days (new) | 5.00 V | 1.00 (max) | 4000 Hz (high) |
| 7 days | 4.70 V | 0.85 | 4000 Hz |
| 30 days (old) | 3.85 V | 0.60 | 1000 Hz (low) |

Sound switching: **sharp** (LM393 comparator) at V_cap = 2.5 V.

### Phototaxis (attraction)

| Parameter | Value | Description |
|---|---|---|
| Range | 30 cm | Bright LED detection radius |
| K_photo | 4.0 | Only old follow bright centers of mass |

### Sound Repulsor (collision avoidance)

| Parameter | Value | Description |
|---|---|---|
| Range | 3.0 cm | Buzzer heard within this radius → turn away |
| K_repuls | 2.0 | Turn strength |
| Volume | 1.0 (equal) | Same for all |
| New frequency | 4000 Hz | High pitch |
| Old frequency | 1000 Hz | Low pitch |
| Transition | Sharp (LM393 at 2.5V) | Step change |

### Radio (ESP-NOW)

| Parameter | Value |
|---|---|
| Module | ESP32-C3 (RISC-V) |
| Packet | ID (1B) + V_cap_ADC (2B) + age_days (2B) + CRC (1B) = 6B |
| Interval | 100 ms (TDMA: 10 ms slot per bot) |
| Power | CR2032 (separate from RC and motor) |

### Motion

| Parameter | Value |
|---|---|
| v_base | 3 cm/s |
| v_max | 5 cm/s |
| noise_angle | 15° |
| dt_simulation | 0.1 s |

### Arena

| Parameter | Value |
|---|---|
| Size | 100 × 100 cm |
| Surface | Smooth plastic, matte white |
| Soundproofing | Acoustic foam on walls |
| Camera | 4K, 60fps, 120cm height |
| Microphone array | 4 × MAX9814 (corners) |
| GPU (optional) | Jetson Nano / RTX 3060 for real-time tracking |

### Metrics

| Metric | Expectation | Description |
|---|---|---|
| HI | >0.5 for C; 0.5 for A,B,D,E | Hierarchy Index |
| R_leader | <30 cm for new; >30 cm for old (approximately) | Leadership radius |
| τ_conv | <120 s | Convergence time |
| Δ_spectrum | >2:1 (4000/1000 Hz) in cluster center | Acoustic age map |

### Control Tests (A–F)

| Test | N_new | N_old | LED/sound | Expected HI |
|---|---|---|---|---|
| A | 120 | 0 | on | 0.5 |
| B | 0 | 120 | on | 0.5 |
| C | 60 | 60 | on | **>0.5** |
| D | 60 | 60 | **off** | 0.5 |
| E | 60 | 60 | on (blind) | 0.5 |
| F | 60 old (recharged) | 60 new | on | >0.5 if Ze; 0.5 if electrical |

### Budget

| Component | Qty | Unit price | Total |
|---|---|---|---|
| ESP32-C3 | 120 | $1.50 | $180 |
| Supercapacitor 1F | 120 | $0.50 | $60 |
| Resistor 10 MΩ | 120 | $0.05 | $6 |
| LM393 comparator | 120 | $0.15 | $18 |
| LED 5mm | 120 | $0.05 | $6 |
| Piezo buzzer | 120 | $0.10 | $12 |
| Photodiode | 120 | $0.10 | $12 |
| MAX9814 microphone | 120 | $0.50 | $60 |
| 2N3904 transistor | 120 | $0.05 | $6 |
| Pager motor | 120 | $0.20 | $24 |
| Li-Po 100 mAh | 120 | $0.50 | $60 |
| CR2032 + holder | 120 | $0.30 | $36 |
| 3D-printed chassis + ballast | 120 | $0.50 | $60 |
| **Subtotal robots** | | | **$540** |
| 4K camera (ELP/USB) + lens | 1 | $80 | $80 |
| Acoustic foam | 1 | $15 | $15 |
| Arena plastic | 1 | $20 | $20 |
| ESP32 receiver + USB | 1 | $5 | $5 |
| Li-Po charging station | 1 | $15 | $15 |
| **Subtotal arena** | | | **$135** |
| **TOTAL (no GPU)** | | | **$675** |
| **TOTAL (with Jetson Nano)** | | | **$875** |
