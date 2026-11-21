"""Individual agents for a fictional, abstract agent-based simulation."""
from dataclasses import dataclass, field
from enum import Enum


class Team(str, Enum):
    BLUE = "blue"
    RED = "red"


class Rank(str, Enum):
    RECRUIT = "recruit"
    REGULAR = "regular"
    VETERAN = "veteran"


class AgentState(str, Enum):
    ACTIVE = "active"
    WOUNDED = "wounded"
    DEAD = "dead"


# Illustrative game parameters only; not empirical or real-world estimates.
RANK_PROFILE = {
    Rank.RECRUIT: {"visual_scale": 0.72, "resilience": 0.55, "experience": 0.15},
    Rank.REGULAR: {"visual_scale": 1.00, "resilience": 0.78, "experience": 0.55},
    Rank.VETERAN: {"visual_scale": 1.35, "resilience": 0.94, "experience": 0.90},
}


@dataclass
class Agent:
    agent_id: int
    team: Team
    rank: Rank
    x: float
    y: float
    morale: float = 1.0
    health: float = 1.0
    state: AgentState = AgentState.ACTIVE
    shots_fired: int = 0
    hits_taken: int = 0
    metadata: dict = field(default_factory=dict)

    @property
    def profile(self):
        return RANK_PROFILE[self.rank]

    @property
    def visual_scale(self):
        return self.profile["visual_scale"]

    @property
    def resilience(self):
        return self.profile["resilience"]

    @property
    def experience(self):
        return self.profile["experience"]

    @property
    def is_operational(self):
        return self.state == AgentState.ACTIVE

    def apply_abstract_hit(self, severity: float = 0.38) -> None:
        """Apply an illustrative game hit; rank modifies the health loss."""
        if self.state == AgentState.DEAD:
            return
        self.hits_taken += 1
        self.health = max(0.0, self.health - severity * (1.15 - self.resilience))
        if self.health <= 0.0:
            self.state = AgentState.DEAD
        elif self.health < 0.55:
            self.state = AgentState.WOUNDED

    def recover_morale(self, amount: float = 0.01) -> None:
        if self.state != AgentState.DEAD:
            self.morale = min(1.0, self.morale + amount)
