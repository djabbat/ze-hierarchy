# MAP — Ze-Hierarchy

**Project map: testing Ze effect via age-based hierarchy in bristlebot swarms.**

## Structure

```
Ze-Hierarchy/
│
├── README.md           ← Overview (English)
├── CONCEPT.md          ← Full concept (hypothesis, design, equations)
├── PARAMETERS.md       ← Numerical parameters
├── TODO.md             ← Task plan
├── MAP.md              ← This file
├── STATE.md            ← Current status
├── MEMORY.md           ← Decision history
├── GRANTS.md           ← Funding sources
│
├── simulator/          ← Python simulation
│   ├── bot.py          ← Robot model (RC age, LED, buzzer)
│   ├── arena.py        ← Arena (light gradient, repulsor)
│   ├── physics.py      ← Collision physics
│   └── run.py          ← Run simulation
│
├── analysis/           ← Metrics and visualization
│   ├── metrics.py      ← HI, R_leader, τ_conv
│   ├── visualize.py    ← Animation, heatmaps
│   └── run_30_seeds.py ← Batch run for statistics
│
├── hardware/           ← Hardware prototype
│   ├── README.md       ← Spec
│   ├── bom.md          ← Bill of Materials ($675)
│   └── schematic.md    ← Circuit diagram
│
└── data/               ← Simulation data (gitignored)
```

## External links

| Link | Description |
|---|---|
| `../docs/Peoch_Experiment_and_Ze.md` | René Peoc'h experiment reinterpretation |
| `../docs/Space_As_Ze_Error.md` | Space as Ze error |
| `../README.md` | Ze Vectors Theory |
| https://github.com/djabbat/ze-hierarchy | Public repository |

## File status

| File | Status |
|---|---|
| README.md | ✅ English |
| CONCEPT.md | ✅ English |
| PARAMETERS.md | ✅ English |
| TODO.md | ✅ English |
| MAP.md | ✅ This file |
| STATE.md | ✅ English |
| MEMORY.md | ✅ English |
| GRANTS.md | ✅ English |
| simulator/* | ✅ Python (comments in English) |
| analysis/* | ✅ Python (comments in English) |
| hardware/* | ✅ English |
