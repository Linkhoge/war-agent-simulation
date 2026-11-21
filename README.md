# War Agent Simulation

An educational, fictional agent-based battlefield toy model. It adapts the modular agent/state/update/visualisation ideas in [Linkhoge/rumour-sim](https://github.com/Linkhoge/rumour-sim) and the mobile-agent framing in Le Nguyen's [Simulation 102: Agent-Based Disease Modeling](https://medium.com/@ln8378/simulation-102-agent-based-disease-modeling-17307f2de2f3).

This is **not** a realistic military simulator, tactical planner, or predictor. Combat is an abstract stochastic game mechanic; parameters are illustrative and are not calibrated to real-world weapons, people, or conflicts.

## Features in the first milestone

- Two fictional teams: Blue and Red.
- Individual agents with rank, experience, morale, health, and operational state.
- Recruit, regular, and veteran visual hierarchy.
- Recruits have higher *abstract* casualty vulnerability; veterans have greater *abstract* resilience.
- Discrete simulation steps and reproducible seeded random runs.
- Abstract projectile/tracer events for visual feedback.
- Persistent wounded and dead states, plus team-level statistics.
- Headless mode for repeatable experiments.

## Requirements

Python 3.10+.

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
python main.py --blue 40 --red 40 --steps 1500 --seed 42
python main.py --headless --blue 100 --red 100 --steps 500 --seed 7
python -m unittest discover -s tests -v
```

The graphical viewer uses Arcade. If Arcade is unavailable, use `--headless` or install the requirements.

## Controls

- Space: pause/resume
- Up / Down: simulation speed
- R: restart with the same seed
- Esc: quit

## Model overview

Each agent is an independent entity. A step updates agent movement, evaluates abstract encounters, emits short-lived visual tracer events, updates health/state, and records statistics. The model uses a seeded Python random generator rather than global random state.

Ranks influence visual scale and illustrative resilience/vulnerability parameters. They do not represent real-world survival probabilities. See [MODEL.md](MODEL.md) for assumptions and limitations.

## Project structure

| File | Responsibility |
|---|---|
| `agent.py` | Agent attributes, ranks, and states |
| `battlefield.py` | World bounds and team setup |
| `simulation.py` | Seeded discrete-time model and statistics |
| `viewer.py` | Optional Arcade visualisation |
| `main.py` | CLI and entry point |
| `tests/` | Model regression tests |
| `MODEL.md` | Rules, assumptions, and limitations |
| `REFERENCES.md` | Attribution and reading list |

## Attribution

The architecture borrows general agent-based modelling ideas from the linked rumour simulation and disease-modeling article. This repository is a new implementation; it does not copy the rumour model's domain-specific rules or claim that the cited work validates these combat abstractions.
