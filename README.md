# War Agent Simulation

A fictional, educational agent-based simulation set on a stylised Western Front battlefield in 1944, with a U.S. Army force facing a German Heer force.

The project adapts the agent/state/update/visualisation structure of [Linkhoge/rumour-sim](https://github.com/Linkhoge/rumour-sim) and agent-based modelling ideas from Le Nguyen's [Simulation 102](https://medium.com/@ln8378/simulation-102-agent-based-disease-modeling-17307f2de2f3).

## Historical setting

The default scenario is a fictional encounter inspired by the 1944 Western Front. It is not a reconstruction of a named battle and does not claim historical casualty accuracy.

- Blue side: U.S. Army, with WWII-era rank titles.
- Red side: German Heer (the army branch of the Wehrmacht), with Heer rank titles.
- German Heer ranks are distinct from Waffen-SS ranks; the project does not model the Waffen-SS.
- No Nazi political insignia or propaganda imagery is used.
- Uniform colours are simplified visual cues, not exact reproductions of a particular division's kit.

## What the simulation shows

- Separate U.S. Army and German Heer rank ladders.
- Rank-ordered formations, with junior enlisted agents nearer the central gap and senior ranks further back.
- Larger markers and higher illustrative resilience for higher-ranked agents.
- Tracer events, firing flashes and hit flashes.
- Wounded and dead agents moving into visible casualty areas.
- Live team totals and per-rank population counts.
- Seeded, reproducible runs and a headless mode.

The model is a toy simulation, not a tactical planner, weapons model, or predictor. Combat events are abstract stochastic game events; tracer graphics are visual indicators, not physical projectile paths. Rank-based resilience is an explicitly fictional gameplay rule, not a claim that senior officers were physically harder to injure.

## Requirements

Python 3.10+.

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
python main.py --blue 100 --red 100 --steps 1500 --seed 42
python main.py --headless --blue 100 --red 100 --steps 500 --seed 7
python -m unittest discover -s tests -v
```

## Controls

- Space: pause/resume
- Up / Down: simulation speed
- R: restart with the same seed
- Esc: quit

## Main files

| File | Responsibility |
|---|---|
| `agent.py` | U.S. and German rank ladders, agent attributes and states |
| `battlefield.py` | Rank-ordered formation placement and casualty areas |
| `simulation.py` | Seeded abstract event simulation and casualty animation |
| `viewer.py` | Arcade display, rank counts and event effects |
| `tests/` | Regression tests |
| `MODEL.md` | Model rules and limitations |
| `REFERENCES.md` | Historical rank and modelling sources |
