"""World setup and fictional team placement."""
from dataclasses import dataclass
import random
from agent import Agent, Rank, Team


@dataclass(frozen=True)
class Battlefield:
    width: float = 100.0
    height: float = 70.0
    margin: float = 8.0

    def clamp(self, x: float, y: float) -> tuple[float, float]:
        return (
            min(self.width - self.margin, max(self.margin, x)),
            min(self.height - self.margin, max(self.margin, y)),
        )


def build_armies(blue_count: int, red_count: int, rng: random.Random,
                 world: Battlefield | None = None) -> list[Agent]:
    """Create balanced fictional populations on opposite halves of the map."""
    if blue_count < 1 or red_count < 1:
        raise ValueError("Each team must contain at least one agent")
    world = world or Battlefield()
    agents = []
    ranks = (Rank.RECRUIT, Rank.REGULAR, Rank.VETERAN)
    weights = (0.42, 0.38, 0.20)
    next_id = 0
    for team, count, x_range in (
        (Team.BLUE, blue_count, (world.margin, world.width * 0.38)),
        (Team.RED, red_count, (world.width * 0.62, world.width - world.margin)),
    ):
        for _ in range(count):
            rank = rng.choices(ranks, weights=weights, k=1)[0]
            agents.append(Agent(
                agent_id=next_id,
                team=team,
                rank=rank,
                x=rng.uniform(*x_range),
                y=rng.uniform(world.margin, world.height - world.margin),
                morale=rng.uniform(0.65, 1.0),
            ))
            next_id += 1
    return agents
