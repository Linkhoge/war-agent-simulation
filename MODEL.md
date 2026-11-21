# Model specification and assumptions

## Purpose

A small, inspectable agent-based modelling exercise with two fictional teams facing each other across an open central gap.

## Formation layout

- Blue and Red occupy opposite sides of the battlefield.
- Each side has a visible front battle line.
- The space between the two front lines is intentionally left open.
- Recruits occupy the first rank nearest the central gap.
- Regulars form the next rank behind recruits.
- Veterans occupy the rear ranks.
- If a rank has more agents than fit in one row, it wraps into additional rows behind that rank.
- Each agent keeps a fixed formation slot in this milestone. When an agent becomes wounded or dead, its marker changes state but its slot remains, making casualties and gaps in the line easy to see.

The formation is a visual and organisational abstraction. It does not encode real-world battle doctrine or tactical positioning.

## Agent heterogeneity

Each agent has a team, rank, position, morale, health, and state. Rank changes visual scale and illustrative resilience. Recruits are smaller and assigned lower resilience; veterans are larger and more resilient. Parameters are design choices, not empirical estimates.

## States

- **Active:** participates in abstract event sampling.
- **Wounded:** remains visible but does not participate in further events in this milestone.
- **Dead:** persistent terminal state, shown as a grey crossed marker.

## Update loop

1. Agents retain their assigned formation slots.
2. The model samples a small number of abstract cross-team encounter events.
3. A successful abstract event may create a short-lived visual tracer and apply an illustrative health change.
4. Agents transition to wounded or dead according to remaining health.
5. Team state counts are recorded.

There is no realistic weapon model, aiming, ballistics, range calculation, target prioritisation, cover simulation, or tactical decision support. Tracers are event visualisations only.

## Reproducibility

A local random.Random(seed) instance controls the run. Repeating the same configuration with the same Python version should reproduce the same model sequence.

## Limitations and future work

- Parameters are illustrative and not empirically calibrated.
- No real-world casualty inference should be made.
- Formations are static; dynamic advance, retreat, and morale effects are future modelling options.
- Wounded agents are inactive in this milestone.
- Future experiments should report multiple seeds, means, dispersion, and sensitivity to parameter choices.
