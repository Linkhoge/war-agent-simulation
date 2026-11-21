"""WWII-era formations and casualty areas on a simple empty battlefield."""
import random
from dataclasses import dataclass
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

    def clamp(self, x, y):
        return (min(self.width-self.margin,max(self.margin,x)),
                min(self.height-self.margin,max(self.margin,y)))

    def front_line_x(self, team):
        return self.blue_front_x if team == Team.BLUE else self.red_front_x

    def casualty_slot(self, team, index):
        row,column=divmod(index,self.casualty_columns)
        y=self.margin+3+column*5.5
        depth=self.margin+3+row*2.6
        x=depth if team==Team.BLUE else self.width-depth
        return self.clamp(x,y)


def _place_formation(agents,team,world):
    centre_y=world.height/2
    direction=-1 if team==Team.BLUE else 1
    front_x=world.front_line_x(team)
    depth_rows=0
    for rank in RANK_ORDERS[team]:
        ranked=sorted((a for a in agents if a.team==team and a.rank==rank),key=lambda a:a.agent_id)
        if not ranked: continue
        rows=(len(ranked)+world.formation_columns-1)//world.formation_columns
        for index,agent in enumerate(ranked):
            row,column=divmod(index,world.formation_columns)
            y=centre_y+(column-(world.formation_columns-1)/2)*world.formation_spacing
            x=front_x+direction*((depth_rows+row)*world.row_spacing)
            agent.x,agent.y=world.clamp(x,y)
            agent.metadata.update(formation_rank_order=RANK_ORDERS[team].index(rank),
                                  formation_row=row,formation_column=column,
                                  formation_x=agent.x,formation_y=agent.y)
        depth_rows+=rows


def build_armies(blue_count,red_count,rng,world=None):
    if blue_count<1 or red_count<1:
        raise ValueError("Each army must contain at least one agent")
    world=world or Battlefield()
    agents=[]; next_id=0
    for team,count in ((Team.BLUE,blue_count),(Team.RED,red_count)):
        ranks=RANK_ORDERS[team]
        weights=[1.0/((i+1)**1.45) for i in range(len(ranks))]
        for _ in range(count):
            rank=rng.choices(ranks,weights=weights,k=1)[0]
            recruit=rng.random()<.18
            agents.append(Agent(agent_id=next_id,team=team,rank=rank,
                                x=world.front_line_x(team),y=world.height/2,
                                morale=rng.uniform(.65,1.0),
                                metadata={"recruit":recruit}))
            next_id+=1
    _place_formation(agents,Team.BLUE,world)
    _place_formation(agents,Team.RED,world)
    return agents
