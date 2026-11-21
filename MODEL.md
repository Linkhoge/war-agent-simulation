# Model specification

## Purpose

A transparent, fictional agent-based model for experimenting with heterogeneous agents, formations, state changes, stochastic events and visualisation.

## Rank hierarchy

The simulation uses a simplified U.S.-style army rank sequence: Recruit, Private, Private First Class, Specialist, Corporal, Sergeant, Staff Sergeant, Sergeant First Class, Master Sergeant, Sergeant Major, Warrant Officer 1, Chief Warrant Officer 2–5, Second Lieutenant, First Lieutenant, Captain, Major, Lieutenant Colonel, Colonel, Brigadier General, Major General, Lieutenant General and General.

This is a convenient single progression for the toy model, not a claim that all armies use these titles or place every specialist grade identically. Some ranks share pay grades or are alternative appointments in real services.

## Formation layout

- Blue and Red occupy opposite sides of the field.
- Their front lines face the open central gap.
- Agents are sorted from lowest to highest rank.
- Recruits and junior ranks are nearest the gap; senior enlisted, warrant officers and commissioned officers are placed progressively further back.
- Large rank groups wrap into additional rows.
- Living agents retain their formation slots in this version.

## Rank attributes

Rank controls marker scale and an illustrative resilience value. Higher ranks are larger and more resilient in the game model because that is the requested visual/gameplay convention. These values do not represent real-world protection, combat skill, or survival rates.

## Event and animation loop

1. The model samples abstract cross-team encounter events.
2. A firing event creates a short-lived tracer whether or not it hits.
3. The firing agent briefly displays a muzzle flash ring.
4. A successful hit applies an illustrative health change and briefly flashes the affected agent.
5. When an agent becomes wounded or dead, it is assigned a casualty-area destination.
6. The agent animates from its formation slot to that destination; surviving agents stay in place.
7. Team totals and cumulative shots are recorded.

Tracer graphics are event visualisations, not ballistic paths. There is no realistic weapon, aiming, range, target-selection, cover, or tactical decision model.

## Reproducibility

A local `random.Random(seed)` instance controls each run. The same configuration and Python version should reproduce the same event sequence.

## Limitations

- Parameters are illustrative and not empirically calibrated.
- The rank ladder is a simplified reference hierarchy, not a universal armed-forces standard.
- Casualties leave the formation but remain visible in the casualty area.
- Wounded agents are inactive in this iteration.
- The formations do not advance or manoeuvre.
- No real-world casualty inference should be made.
