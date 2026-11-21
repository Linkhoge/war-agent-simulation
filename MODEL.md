# Model specification and assumptions

## Purpose

A small, inspectable agent-based modelling exercise with two fictional teams. The purpose is to explore heterogeneous agents, state transitions, stochastic outcomes, visualisation, and reproducible experiments.

## Agent heterogeneity

Each agent has a team, rank, position, morale, health, and state. Rank changes visual scale and illustrative resilience. Recruits are assigned lower resilience than regulars and veterans. This makes recruit agents more vulnerable within this toy model by construction.

The rank parameters in `agent.py` are design choices, not estimates from military or medical data.

## States

- **Active:** can participate in the toy model.
- **Wounded:** remains visible but no longer participates in encounters in this initial milestone.
- **Dead:** persistent terminal state, shown with a grey marker and cross.

## Update loop

1. Active agents make a small bounded random walk.
2. The model samples a small number of abstract cross-team encounter events.
3. A successful abstract event may create a visual tracer and apply an illustrative health change.
4. Agents transition to wounded or dead according to remaining health.
5. Team state counts are recorded.

There is no realistic weapon model, aiming, ballistics, range calculation, target prioritisation, cover simulation, or tactical decision support. Tracers are event visualisations only.

## Reproducibility

A local `random.Random(seed)` instance controls the run. Repeating the same configuration with the same Python version should reproduce the same model sequence.

## Limitations and future work

- Parameters are illustrative and not empirically calibrated.
- No real-world casualty inference should be made.
- The current movement is a random walk, not tactical manoeuvring.
- Wounded agents are inactive in this milestone.
- The initial viewer uses a simple 2D map and event tracers.
- Future experiments should report multiple seeds, means, dispersion, and sensitivity to parameter choices.
