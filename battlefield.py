"""World setup and two opposing rank-ordered formations."""
from dataclasses import dataclass
import random
from agent import Agent, Rank, Team


@dataclass(frozen=True)
class Battlefield:
    width: float = 100.0
    height: float = 70.0
    margin: float = 8.0
    blue_front_x: float = 31.0
    red_front_x: float = 69.0
    formation_columns: int = 8
    formation_spacing: float = 3.8
    rank_depth: float = 4.0

    def clamp(self, x: float, y: float) -> tuple[float, float]:
        return (
            min(self.width - self.margin, max(self.margin, x)),
            min(self.height - self.margin, max(self.margin, y)),
        )

    def front_line_x(self, team: Team) -> float:
        return self.blue_front_x if team == Team.BLUE else self.red_front_x


def _place_formation(agents: list[Agent], team: Team, world: Battlefield) -> None:
    """Place recruits nearest the central gap, regulars behind, veterans rearward."""
    rank_order = (Rank.RECRUIT, Rank.REGULAR, Rank.VETERAN)
    centre_y = world.height / 2
    direction = -1 if team == Team.BLUE else 1
    front_x = world.front_line_x(team)
    for rank_index, rank in enumerate(rank_order):
        ranked = sorted(
            (agent for agent in agents if agent.team == team and agent.rank == rank),
            key=lambda agent: agent.agent_id,
        )
        for index, agent in enumerate(ranked):
            row, column = divmod(index, world.formation_columns)
            y = centre_y + (column - (world.formation_columns - 1) / 2) * world.formation_spacing
            x = front_x + direction * (rank_index * world.rank_depth + row * 2.2)
            agent.x, agent.y = world.clamp(x, y)
            agent.metadata["formation_rank_order"] = rank_index
            agent.metadata["formation_row"] = row
            agent.metadata["formation_column"] = column


def build_armies(blue_count: int, red_count: int, rng: random.Random,
                 world: Battlefield | None = None) -> list[Agent]:
    """Create opposing armies, with recruits at the front and veterans behind."""
    if blue_count < 1 or red_count < 1:
        raise ValueError("Each team must contain at least one agent")
    world = world or Battlefield()
    agents = []
    ranks = (Rank.RECRUIT, Rank.REGULAR, Rank.VETERAN)
    weights = (0.42, 0.38, 0.20)
    next_id = 0
    for team, count in ((Team.BLUE, blue_count), (Team.RED, red_count)):
        for _ in range(count):
            rank = rng.choices(ranks, weights=weights, k=1)[0]
            agents.append(Agent(
                agent_id=next_id, team=team, rank=rank,
                x=world.front_line_x(team), y=world.height / 2,
                morale=rng.uniform(0.65, 1.0),
            ))
            next_id += 1
    _place_formation(agents, Team.BLUE, world)
    _place_formation(agents, Team.RED, world)
    return agents
