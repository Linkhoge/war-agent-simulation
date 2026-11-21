"""Seeded, discrete-time abstract agent simulation.

Agents hold two opposing formations. Recruits occupy the front rank, regulars
stand behind them, and veterans form the rear ranks. Combat remains an
abstract stochastic game mechanic, not a realistic tactical or weapon model.
"""
from dataclasses import dataclass, field
import random
from agent import Agent, AgentState, Team
from battlefield import Battlefield, build_armies


@dataclass
class SimulationConfig:
    blue_count: int = 30
    red_count: int = 30
    steps: int = 1200
    seed: int = 42
    movement: float = 0.0
    encounter_probability: float = 0.035
    hit_probability: float = 0.28
    wound_severity: float = 0.38


@dataclass
class Tracer:
    source_id: int
    target_id: int
    start: tuple[float, float]
    end: tuple[float, float]
    created_at: int


@dataclass
class Simulation:
    config: SimulationConfig
    world: Battlefield = field(default_factory=Battlefield)
    agents: list[Agent] = field(init=False)
    tick: int = 0
    rng: random.Random = field(init=False)
    tracers: list[Tracer] = field(default_factory=list)
    history: list[dict] = field(default_factory=list)

    def __post_init__(self):
        self.rng = random.Random(self.config.seed)
        self.agents = build_armies(
            self.config.blue_count, self.config.red_count, self.rng, self.world
        )
        self.record()

    def by_id(self, agent_id: int) -> Agent:
        return self.agents[agent_id]

    def _move_agents(self):
        # Formation positions remain fixed in this milestone. This makes the
        # front line and the rank depth easy to inspect and compare.
        return

    def _abstract_encounters(self):
        blue = [a for a in self.agents if a.team == Team.BLUE and a.is_operational]
        red = [a for a in self.agents if a.team == Team.RED and a.is_operational]
        if not blue or not red:
            return
        # Random pairings are abstract event sampling, not tactical target choice.
        pairs = min(len(blue), len(red), max(1, (len(blue) + len(red)) // 12))
        for _ in range(pairs):
            if self.rng.random() >= self.config.encounter_probability:
                continue
            source = self.rng.choice(blue if self.rng.random() < 0.5 else red)
            opposing = red if source.team == Team.BLUE else blue
            target = self.rng.choice(opposing)
            source.shots_fired += 1
            if self.rng.random() < self.config.hit_probability:
                target.apply_abstract_hit(self.config.wound_severity)
                self.tracers.append(Tracer(
                    source.agent_id, target.agent_id,
                    (source.x, source.y), (target.x, target.y), self.tick
                ))

    def step(self):
        if self.tick >= self.config.steps:
            return False
        self._move_agents()
        self._abstract_encounters()
        self.tick += 1
        self.tracers = [t for t in self.tracers if self.tick - t.created_at <= 5]
        self.record()
        return True

    def record(self):
        row = {"tick": self.tick}
        for team in Team:
            members = [a for a in self.agents if a.team == team]
            row[f"{team.value}_active"] = sum(a.state == AgentState.ACTIVE for a in members)
            row[f"{team.value}_wounded"] = sum(a.state == AgentState.WOUNDED for a in members)
            row[f"{team.value}_dead"] = sum(a.state == AgentState.DEAD for a in members)
        self.history.append(row)

    def run(self):
        while self.step():
            pass
        return self.history[-1]

    def summary(self):
        return self.history[-1].copy()
