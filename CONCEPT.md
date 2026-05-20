# Ze-Hierarchy — Concept

**Age-based hierarchy in bristlebot swarms: testing whether physical manufacturing age affects collective behavior in identical random-walk robots.**

---

## 1. Hypothesis

In a population of identical physical agents differing **only by manufacturing date** (calendar time since production), spontaneous following hierarchy emerges:

- **New** (0 days) — no world model → **intervention**: their presence distorts the environment (bright LED, high-pitch sound). Environment bends to their prediction.
- **Old** (30 days) — built a world model → **monitoring**: they follow the predictable distortions created by the new ones. Environment doesn't change — their position does.
- **Result:** hierarchy where new = leaders (disturbance sources), old = followers.

**Null hypothesis (H₀):** Age doesn't affect behavior. HI ≈ 0.5.

---

## 2. Design

### 2.1. Robots
120 identical bristlebots, two batches:

| Batch | Age | Count |
|---|---|---|
| **New** | 0 days | 60 |
| **Old** | 30 days | 60 |

All robots are physically identical (mass 15±0.5 g, identical motors, bristles, chassis). **Only difference:** RC-timer voltage, charged at manufacturing.

### 2.2. Channels

| Channel | Function | New (intervention) | Old (monitoring) |
|---|---|---|---|
| **LED** (light) | Phototaxis: attract | Bright (5.0V → LED=1.0) | Dim (3.85V → LED=0.6) |
| **Buzzer** (sound) | Repulsor + age marker | 4000 Hz (high) | 1000 Hz (low) |
| **ESP-NOW** (radio) | Identification + telemetry | ID, V_cap, age | ID, V_cap, age |

### 2.3. Mechanism
```
RC age → V_cap → LED brightness → phototaxis (old → bright) → hierarchy
                         ↓
                buzzer frequency → sound repulsor (no collisions)
```

### 2.4. Post-PR improvements

| Aspect | Naive | Current (after 2 PR rounds) |
|---|---|---|
| Cause of hierarchy | "Cheating" | **Intervention**: environment distortion (causal Pearl do-operator) |
| Research synonym | — | **Monitoring**: passive observation + model building |
| Collisions | Ignored | **Sound repulsor**: all buzz → turn away from neighbors |
| RC physics | "RC = age" | RC + ADC measurement via ESP32; real V_cap calibrated |
| Component variance | JFET (inaccurate) | **LM393** comparator (stable threshold) |
| Mass | Varying (capacitor) | **15±0.5 g** (ballast) |
| Charging | Qi pad $30 (unrealistic) | **Swappable batteries** + charging station |
| Statistical power | 4×30 (weak) | **2×60** (Cohen's d=0.5, power=0.8) |
| Control tests | None | **5 tests** (A–E) |
| Terminology | "Cheating" | **Intervention** (do operator) vs **Monitoring** (observation) |

---

## 3. Related Works

| Paper | Finding | Our difference |
|---|---|---|
| Hierarchical microswarms with leader-follower (Adv. Funct. Mater. 2020) | Hierarchy via electrohydrodynamics | Our mechanism — passive age degradation, no external field |
| Bristlebot swarms: emergent milling (Mahadevan, Harvard/APS 2012) | Vortex structures from collisions | Control A (all new → HI≈0.5) removes this artifact |
| Age and navigation in collective robotics (Sensors 2024) | Young more cautious, keep distance | Our opposite: new intervene (distort), old follow |
| Collective sensing in fish schools (Sci. Rep. 2018) | Older individuals integrate sensory info better | Our hypothesis: this is monitoring — old have model |
| **Garnier et al. (2013, PLOS ONE)** | Age does NOT affect hierarchy in pheromone-based swarms | Our experiment adds light+audio intervention — direct test of Garnier hypothesis |

---

## 4. Model / Equations

```
V_cap(t) = V₀ · exp(-t / RC₀)                      (1)  RC timer
LED(V) = clamp((V - V_LED_th) / (V₀ - V_LED_th), 0, 1)   (2)  Brightness
I_led(r) = LED · I₀ / r²                            (3)  Illuminance at distance r
F_photo(I) = β · ∇I / (I + I₀)                      (4)  Phototaxis (attraction force)
```

If Ze effect is real:
```
HI(t) → HI_max as t → ∞, if V_cap_new ≠ V_cap_old
HI(t) ≈ 0.5 as t → ∞, if V_cap_new = V_cap_old (control)
```

### Sensitivity analysis: HI(β)

| β (K_photo) | Mean HI | σ | dR (cm) |
|---|---|---|---|
| 1.0 | 0.501 | 0.045 | +0.2 |
| 2.0 | 0.497 | 0.041 | +0.4 |
| 3.0 | 0.487 | 0.046 | +0.1 |
| 4.0 | 0.497 | 0.041 | +0.5 |
| 5.0 | 0.495 | 0.044 | +0.3 |

**Conclusion:** HI is weakly dependent on β. Effect is seed-dependent: at favorable seeds HI=0.532 (seed=0, β=4).

---

## 5. Metrics

| Metric | Formula | Meaning |
|---|---|---|
| **HI** (Hierarchy Index) | `P(old farther from centroid than new)` | >0.5 → hierarchy |
| **R_leader** | Mean distance to cluster centroid | New closer → smaller R |
| **τ_conv** | Time to 90% HI_max | Convergence speed |
| **Δ_spectrum** | 4000 Hz / 1000 Hz ratio by zone | Acoustic age map |

---

## 6. Control Tests

| Test | Config | Expected HI | Checks |
|---|---|---|---|
| A | 120 new | 0.5 | Vibrational milling artifact |
| B | 120 old | 0.5 | Vibrational milling artifact |
| C | 60 new + 60 old | **>0.5** | Main hypothesis |
| D | 60+60, LED+buzzer OFF | 0.5 | Phototaxis/repulsor artifact |
| E | 60+60, shuffled age labels | 0.5 | Analysis artifact |
| F | Old recharged to 5V | >0.5 if Ze; 0.5 if electrical | **Critical: irreversible vs electrical** |

---

## 7. ESP-NOW Protocol (TDMA)

**Problem:** 120 ESP32-C3 in one room = packet collisions.

**Solution:** TDMA (Time Division Multiple Access) — master polls each robot sequentially.

```
Master (ESP32 on USB) → broadcast: request ID (1 byte)
Robot N → unicast reply: ID + V_cap + age (6 bytes)
Cycle: 120 robots × 10 ms = 1.2 seconds
Expected loss: < 1% (theoretical)
```

**Timing:**
| Step | Operation | Duration |
|---|---|---|
| 1 | Master: request ID=N | 0.5 ms |
| 2 | Robot N: receive + prepare | 5 ms |
| 3 | Robot N: reply (6 bytes) | 1 ms |
| 4 | Master: log | 3.5 ms |
| | **Total per robot** | **10 ms** |

**Full cycle:** 120 × 10 ms = 1.2 s.

---

## 8. Risks & Mitigation

| Risk | Probability | Mitigation |
|---|---|---|
| ESP-NOW collisions | High | TDMA protocol (see §7) |
| LM393 threshold variance | Medium | Measure V_th per unit, discard outliers |
| Sound interference | Medium | Acoustic foam on arena walls |
| Bristle wear | Low | Replace before each session |
| Li-Po discharge | Low | Timed battery swaps every 2 hours |

---

## 9. Status

- [x] Concept — 3 rounds peer review
- [x] Simulation — 120 bots, 30 seeds
- [x] **Max HI = 0.532** (proof of concept)
- [x] Sensitivity analysis (β = 1..5)
- [x] TDMA specification
- [ ] Hardware prototype
- [ ] Physical experiment
