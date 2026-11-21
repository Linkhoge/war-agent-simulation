"""Seeded agent simulation with static formations and animated event effects.

The battle is a fictional, abstract game model. Event sampling is stochastic;
tracer graphics are visual feedback rather than physical projectile simulation.
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
    encounter_probability: float = 0.055
    hit_probability: float = 0.28
    wound_severity: float = 0.38
    casualty_animation_ticks: int = 10
    tracer_lifetime: int = 6


@dataclass
class Tracer:
    source_id: int
    target_id: int
    start: tuple[float, float]
    end: tuple[float, float]
    created_at: int
    hit: bool = False


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

    def _send_to_casualty_area(self, agent: Agent) -> None:
        casualties = [
            other for other in self.agents
            if other.team == agent.team
            and other.state != AgentState.ACTIVE
            and other.casualty_target is not None
            and other.agent_id != agent.agent_id
        ]
        agent.casualty_start = (agent.x, agent.y)
        agent.casualty_target = self.world.casualty_slot(agent.team, len(casualties))
        agent.casualty_started_tick = self.tick

    def _advance_casualties(self) -> None:
        duration = max(1, self.config.casualty_animation_ticks)
        for agent in self.agents:
            if agent.casualty_target is None or agent.casualty_start is None:
                continue
            elapsed = self.tick - agent.casualty_started_tick
            progress = min(1.0, max(0.0, elapsed / duration))
            sx, sy = agent.casualty_start
            tx, ty = agent.casualty_target
            agent.x = sx + (tx - sx) * progress
            agent.y = sy + (ty - sy) * progress

    def _move_agents(self):
        # The living ranks hold their assigned formation slots in this version.
        return

    def _abstract_encounters(self):
        blue = [a for a in self.agents if a.team == Team.BLUE and a.is_operational]
        red = [a for a in self.agents if a.team == Team.RED and a.is_operational]
        if not blue or not red:
            return
        attempts = min(len(blue), len(red), max(1, (len(blue) + len(red)) // 8))
        for _ in range(attempts):
            if self.rng.random() >= self.config.encounter_probability:
                continue
            source = self.rng.choice(blue if self.rng.random() < 0.5 else red)
            opposing = red if source.team == Team.BLUE else blue
            target = self.rng.choice(opposing)
            source.shots_fired += 1
            source.fire_flash_until = self.tick + 2
            hit = self.rng.random() < self.config.hit_probability
            self.tracers.append(Tracer(
                source.agent_id, target.agent_id,
                (source.x, source.y), (target.x, target.y), self.tick, hit
            ))
            if hit:
                previous_state = target.state
                target.apply_abstract_hit(self.config.wound_severity)
                target.hit_flash_until = self.tick + 4
                if previous_state == AgentState.ACTIVE and target.state != AgentState.ACTIVE:
                    self._send_to_casualty_area(target)

    def step(self):
        if self.tick >= self.config.steps:
            return False
        self._move_agents()
        self._abstract_encounters()
        self.tick += 1
        self._advance_casualties()
        self.tracers = [
            tracer for tracer in self.tracers
            if self.tick - tracer.created_at <= self.config.tracer_lifetime
        ]
        self.record()
        return True

    def record(self):
        row = {"tick": self.tick}
        for team in Team:
            members = [a for a in self.agents if a.team == team]
            row[f"{team.value}_active"] = sum(a.state == AgentState.ACTIVE for a in members)
            row[f"{team.value}_wounded"] = sum(a.state == AgentState.WOUNDED for a in members)
            row[f"{team.value}_dead"] = sum(a.state == AgentState.DEAD for a in members)
            row[f"{team.value}_shots"] = sum(a.shots_fired for a in members)
        self.history.append(row)

    def run(self):
        while self.step():
            pass
        return self.history[-1]

    def summary(self):
        return self.history[-1].copy()
