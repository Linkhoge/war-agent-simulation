# Model specification

## Scenario
A fictional, stylised Western Front encounter in 1944 between U.S. Army and German Heer forces. It is not a reconstruction of a named battle.

## Agents and experience
Each side uses its own WWII-era rank ladder. Rank affects marker size and a small illustrative experience/resilience score. A separate random recruit flag gives a modest vulnerability penalty; rank alone does not mean a soldier is a veteran.

## Basic combat loop
- Soldiers have a small ammunition supply and pause briefly to reload when empty.
- Experience slightly improves abstract hit chance.
- Suppression rises when a soldier is targeted and slowly fades. Suppressed soldiers move towards the nearest cover feature.
- Cover gives a modest protection bonus. The model does not trace realistic lines of sight or calculate ballistic penetration.
- Wounded soldiers move slowly towards their casualty area; dead agents remain in the simulation.

## Battlefield
A small fixed map includes a trench, wall, building, forest patch, road and craters. Features are simple rectangles with basic cover values. They are visual/gameplay zones, not detailed geometry. The road is easier to read visually but has no special movement bonus in this first pass.

## Limits
All combat values are illustrative and uncalibrated. There is no realistic weapon, projectile, aiming, medical, command, or tactical model. This is a small educational toy simulation, not a tactical planner or historical casualty predictor.
