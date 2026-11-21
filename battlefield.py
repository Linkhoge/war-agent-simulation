"""WWII U.S. Army and German Heer formations and casualty areas."""
from dataclasses import dataclass
import random
from agent import Agent, RANK_ORDERS, Team


@dataclass(frozen=True)
class Battlefield:
    width: float = 100.0
    height: float = 70.0
    margin: float = 8.0
    blue_front_x: float = 36.0
    red_front_x: float = 64.0
    formation_columns: int = 8
    formation_spacing: float = 3.8
    row_spacing: float = 0.9
    casualty_columns: int = 8

    def clamp(self, x: float, y: float) -> tuple[float, float]:
        return (
            min(self.width - self.margin, max(self.margin, x)),
            min(self.height - self.margin, max(self.margin, y)),
        )

    def front_line_x(self, team: Team) -> float:
        return self.blue_front_x if team == Team.BLUE else self.red_front_x

    def casualty_slot(self, team: Team, index: int) -> tuple[float, float]:
        row, column = divmod(index, self.casualty_columns)
        y = self.margin + 3.0 + column * 5.5
        depth = self.margin + 3.0 + row * 2.6
        x = depth if team == Team.BLUE else self.width - depth
        return self.clamp(x, y)


def _place_formation(agents: list[Agent], team: Team, world: Battlefield) -> None:
    centre_y = world.height / 2
    direction = -1 if team == Team.BLUE else 1
    front_x = world.front_line_x(team)
    depth_rows = 0
    for rank in RANK_ORDERS[team]:
        ranked = sorted(
            (agent for agent in agents if agent.team == team and agent.rank == rank),
            key=lambda agent: agent.agent_id,
        )
        if not ranked:
            continue
        rows_for_rank = (len(ranked) + world.formation_columns - 1) // world.formation_columns
        for index, agent in enumerate(ranked):
            row, column = divmod(index, world.formation_columns)
            y = centre_y + (column - (world.formation_columns - 1) / 2) * world.formation_spacing
            x = front_x + direction * ((depth_rows + row) * world.row_spacing)
            agent.x, agent.y = world.clamp(x, y)
            agent.metadata["formation_rank_order"] = RANK_ORDERS[team].index(rank)
            agent.metadata["formation_row"] = row
            agent.metadata["formation_column"] = column
            agent.metadata["formation_x"] = agent.x
            agent.metadata["formation_y"] = agent.y
        depth_rows += rows_for_rank


def build_armies(blue_count: int, red_count: int, rng: random.Random,
                 world: Battlefield | None = None) -> list[Agent]:
    if blue_count < 1 or red_count < 1:
        raise ValueError("Each army must contain at least one agent")
    world = world or Battlefield()
    agents = []
    next_id = 0
    for team, count in ((Team.BLUE, blue_count), (Team.RED, red_count)):
        ranks = RANK_ORDERS[team]
        # Enlisted grades dominate; officer and general ranks are progressively rarer.
        weights = [1.0 / ((index + 1) ** 1.45) for index in range(len(ranks))]
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
