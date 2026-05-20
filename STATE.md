# STATE — Ze-Hierarchy

**Date:** 2026-05-20
**Phase:** 1 — Simulation (complete)

## Key Result

| Parameter | Value |
|---|---|
| **Max HI** (seed=0) | **0.532** |
| **Mean HI** (10 seeds, 600 steps) | 0.492 |
| **dR max** (old minus new distance from center) | +1.2 cm |
| **Direction** | Positive (Ro > Rn) at 5/10 seeds |
| **Speed** | 120 bots in ~30s (dt=0.1) |

Effect is **seed-dependent, weak**. Reason: bristlebot random walk spreads new bots evenly across arena; old follow them but no density gradient forms.

## Simulation Performance

| Config | Time |
|---|---|
| 20 bots, 60s real | ~1.5s |
| 120 bots, 120s real | ~30s |

## What Didn't Work

| Approach | HI | Why |
|---|---|---|
| Light gradient (K=2.0, all bots) | 0.17 | Old attract each other |
| Bright only (led>0.7) | 0.35 | COM of bright = center of arena |
| Nearest bright (K=8) | **0.53** | Best, but weak |
| Arena 40×40 | 0.06 | Inversion (all crowd center) |
| No noise | 0.15 | Too directional |

## Root Cause

Bristlebot random walk cannot form a stable cluster in simulation. New bots spread evenly, old follow — density gradient never forms. **In real physics**, bristlebot vibrational clustering (Mahadevan 2012) creates spontaneous clustering that simulation doesn't capture. Real experiment may show stronger effect.

## Next Steps

- [x] Concept, PARAMETERS, simulation
- [ ] Hardware prototype
- [ ] Physical experiment

## Current deliverables

- GitHub: https://github.com/djabbat/ze-hierarchy
- Grant: Shuttleworth Flash Grant (submitted 2026-05-20)
- Publication: HardwareX + arXiv (planned)
