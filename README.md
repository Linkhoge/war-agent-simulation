# War Agent Simulation

An educational, fictional agent-based simulation with two opposing forces, visible formations, a full rank ladder, and animated abstract combat events.

The project borrows modular agent/state/update/visualisation ideas from [Linkhoge/rumour-sim](https://github.com/Linkhoge/rumour-sim) and agent-based modelling concepts from Le Nguyen's [Simulation 102](https://medium.com/@ln8378/simulation-102-agent-based-disease-modeling-17307f2de2f3).

This is a toy model, not a realistic military simulator, tactical planner, or predictor. Hit probabilities, resilience and visual effects are illustrative game parameters.

## What's in it

- Blue and Red forces face each other across an open central gap.
- Each force forms up by rank: recruits and junior enlisted ranks first, senior NCOs and warrant officers behind them, then commissioned officers.
- Rank titles include Private, Private First Class, Corporal, Sergeant, Staff Sergeant, Warrant Officer, Second Lieutenant, Captain, Major, Colonel and General.
- Rank affects marker size and illustrative resilience.
- Firing produces a short-lived animated tracer; hits produce a flash.
- Wounded and dead agents move out of their formation slots into a casualty area.
- Surviving agents hold their original places, leaving visible gaps.
- Runs are seeded and can be run without the graphical viewer.

The rank list is a simplified U.S.-style army progression for recognisable titles. Rank systems and equivalent grades differ between countries and services.

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

## Reading the screen

- Blue and red markers show the opposing forces.
- Marker size grows with rank.
- Recruits begin closest to the open gap; higher ranks stand further back.
- Gold markers are wounded; grey crossed markers are dead.
- Coloured rings show firing and hit reactions.
- Tracer lines animate across the gap. They are visual event indicators, not physical projectile paths.
- Casualty areas sit behind each formation.

## Main files

| File | Responsibility |
|---|---|
| `agent.py` | Rank ladder, agent attributes and states |
| `battlefield.py` | Formation placement and casualty slots |
| `simulation.py` | Seeded simulation, event sampling and casualty animation |
| `viewer.py` | Arcade display and visual effects |
| `tests/` | Model regression tests |
| `MODEL.md` | Rules and assumptions |
| `REFERENCES.md` | Rank and modelling references |
