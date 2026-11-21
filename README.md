# War Agent Simulation

An educational, fictional agent-based battlefield toy model. It adapts the modular agent/state/update/visualisation ideas in [Linkhoge/rumour-sim](https://github.com/Linkhoge/rumour-sim) and the mobile-agent framing in Le Nguyen's [Simulation 102: Agent-Based Disease Modeling](https://medium.com/@ln8378/simulation-102-agent-based-disease-modeling-17307f2de2f3).

This is **not** a realistic military simulator, tactical planner, or predictor. Combat is an abstract stochastic game mechanic; parameters are illustrative and are not calibrated to real-world weapons, people, or conflicts.

## Current features

- Two opposing teams with a visible front battle line and an open central gap.
- Organised formations: recruits at the front, regulars behind them, veterans in the rear.
- Agents are arranged in rows and columns; oversized rank groups wrap into additional rows.
- Rank-based visual scale and illustrative resilience differences.
- Abstract projectile/tracer events and persistent wounded/dead markers.
- Seeded runs, headless mode, and team-level casualty statistics.

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

The graphical viewer uses Arcade.

## Controls

- Space: pause/resume
- Up / Down: simulation speed
- R: restart with the same seed
- Esc: quit

## Formation layout

Blue stands on the left and Red on the right. Their front lines face the central open space. Recruits are closest to that space; regulars and veterans are placed progressively farther back. Casualty markers stay in their assigned slots, so losses are visible as gaps or changed markers.

## Project structure

| File | Responsibility |
|---|---|
| `agent.py` | Agent attributes, ranks, and states |
| `battlefield.py` | World bounds and rank-ordered formation setup |
| `simulation.py` | Seeded discrete-time model and abstract events |
| `viewer.py` | Arcade visualisation |
| `main.py` | CLI and entry point |
| `tests/` | Model regression tests |
| `MODEL.md` | Rules, assumptions, and limitations |
| `REFERENCES.md` | Attribution and reading list |

See [MODEL.md](MODEL.md) for the assumptions and limitations. Formation and casualty parameters are illustrative and are not real-world estimates.
