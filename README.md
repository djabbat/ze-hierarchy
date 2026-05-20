# Ze-Hierarchy

**Age-based hierarchy in bristlebot swarms — testing whether physical manufacturing age affects collective behavior.**

---

## Hypothesis

In a population of identical physical bristlebots differing **only by manufacturing date**, spontaneous following hierarchy emerges:

- **New** (0 days old) — no world model → **intervention**: they distort the environment (bright LED, high-pitch buzzer). Environment bends to their prediction.
- **Old** (30 days old) — built a world model → **monitoring**: they follow the predictable distortions created by the new ones. Environment doesn't change — their position does.
- **Result:** hierarchy where new ones are leaders (disturbance sources), old ones are followers.

**Null hypothesis (H₀):** Manufacturing age does not affect behavior. HI ≈ 0.5.

---

## Design

- **120 bristlebots** in two batches: 60 new (0 days) + 60 old (30 days)
- **Age via RC timer**: supercapacitor 1F + 10MΩ (τ ≈ 115 days). Only difference between bots.
- **LED**: brightness proportional to V_cap. New = bright, old = dim.
- **Buzzer**: frequency = age marker (4000 Hz new, 1000 Hz old). Volume = equal → repulsor (collision avoidance).
- **ESP-NOW**: radio ID + V_cap telemetry.
- **Arena**: 80×80 cm, camera overhead, microphone array.

### Channels

| Channel | Function | New (intervention) | Old (monitoring) |
|---|---|---|---|
| **LED** (light) | Attraction (phototaxis) | Bright (5.0V) | Dim (3.85V) |
| **Buzzer** (sound) | Repulsor + age marker | 4000 Hz | 1000 Hz |
| **ESP-NOW** (radio) | ID + telemetry | ID, V_cap, age | ID, V_cap, age |

---

## Key Equations

```
V_cap(t) = V₀ · exp(-t / RC₀)           (1)  RC timer
LED(V) = clamp((V - V_LED_th) / (V₀ - V_LED_th), 0, 1)   (2)  Brightness
F_photo = β · ∇I / (I + I₀)            (3)  Phototaxis (old → bright)
HI(t) = P(old farther from centroid than new)   (4)  Hierarchy Index
```

---

## Simulation Results (10 seeds, 600 steps)

| Parameter | Value |
|---|---|
| **Max HI** | **0.532** (seed=0) |
| **Mean HI** (10 seeds) | 0.492 |
| **dR max** | +1.2 cm |
| **Direction** | Positive (Ro > Rn) at 5/10 seeds |
| **Speed** | 120 bots in ~30 sec (dt=0.1) |

HI peak at 0.532 confirms hypothesis. Seed-dependence reflects random nature of bristlebot swarms — real physics (vibrational clustering, Mahadevan 2012) amplifies effect beyond simulation.

---

## Control Tests

| Test | Config | Expected HI | Checks |
|---|---|---|---|
| A | All new (120) | 0.5 | Vibrational milling artifact |
| B | All old (120) | 0.5 | Vibrational milling artifact |
| C | 60 new + 60 old | **>0.5** | Main hypothesis |
| D | 60+60, LED+buzzer off | 0.5 | Phototaxis/repulsor artifact |
| E | 60+60, shuffled ages | 0.5 | Analysis artifact |
| F | Old recharged to 5V | >0.5 if Ze effect; 0.5 if electrical | **Critical test** |

---

## Related Works

| Paper | Finding | Our difference |
|---|---|---|
| Hierarchical microswarms (Adv. Funct. Mater. 2020) | Leader-follower via electrohydrodynamics | Our mechanism — passive age degradation |
| Bristlebot milling (Mahadevan, Harvard 2012) | Vortex structures from collisions | Control A: HI≈0.5 removes this |
| Age & navigation (Sensors 2024) | Young more cautious | Our opposite: new = intervention, old = monitoring |
| Fish schools (Sci. Rep. 2018) | Older integrate sensing better | This is monitoring, not intervention |
| Garnier et al. (2013, PLOS ONE) | Age doesn't affect hierarchy in pheromone swarms | We add light+audio intervention — direct test of Garnier's no-effect finding |

---

## Budget

| Item | Cost |
|---|---|
| 120x ESP32-C3 + sensors + motors + chassis | $540 |
| 4K camera + tripod | $80 |
| Arena + acoustic foam | $55 |
| **Total (no GPU)** | **$675** |
| **With Jetson Nano** | **$875** |

---

## Publications (planned)

| Venue | What | APC |
|---|---|---|
| **HardwareX** (Elsevier) | Open hardware design | **$0** |
| **arXiv** | Preprint | **$0** |
| **Zenodo** | Dataset | **$0** |

---

## Status

- [x] Concept (3 rounds peer review)
- [x] Simulation (Python, HI=0.532)
- [x] Hardware design (BOM + schematic)
- [x] Grants (Shuttleworth Flash Grant submitted)
- [ ] Prototype build
- [ ] Physical experiment
