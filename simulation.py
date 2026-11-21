"""Small, seeded agent-based battle model with simple cover and combat behaviour."""
from dataclasses import dataclass, field
import random
from agent import Agent, AgentState, Team
from battlefield import Battlefield, build_armies


@dataclass
class SimulationConfig:
    blue_count: int=30
    red_count: int=30
    steps: int=1200
    seed: int=42
    encounter_probability: float=.055
    hit_probability: float=.28
    wound_severity: float=.38
    casualty_animation_ticks: int=10
    tracer_lifetime: int=6
    magazine_size: int=8
    reload_duration: int=3


@dataclass
class Tracer:
    source_id: int
    target_id: int
    start: tuple[float,float]
    end: tuple[float,float]
    created_at: int
    hit: bool=False


@dataclass
class Simulation:
    config: SimulationConfig
    world: Battlefield=field(default_factory=Battlefield)
    agents: list[Agent]=field(init=False)
    tick: int=0
    rng: random.Random=field(init=False)
    tracers: list[Tracer]=field(default_factory=list)
    history: list[dict]=field(default_factory=list)

    def __post_init__(self):
        self.rng=random.Random(self.config.seed)
        self.agents=build_armies(self.config.blue_count,self.config.red_count,self.rng,self.world)
        for a in self.agents: a.ammo=self.config.magazine_size
        self.record()

    def by_id(self,agent_id): return self.agents[agent_id]

    def _send_to_casualty_area(self,agent):
        casualties=[o for o in self.agents if o.team==agent.team and o.state!=AgentState.ACTIVE
                    and o.casualty_target is not None and o.agent_id!=agent.agent_id]
        agent.casualty_start=(agent.x,agent.y)
        agent.casualty_target=self.world.casualty_slot(agent.team,len(casualties))
        agent.casualty_started_tick=self.tick

    def _advance_casualties(self):
        duration=max(1,self.config.casualty_animation_ticks)
        for a in self.agents:
            if a.casualty_target is None or a.casualty_start is None: continue
            # Wounded soldiers crawl under their own power in _move_agents.
            if a.state == AgentState.WOUNDED: continue
            elapsed=self.tick-a.casualty_started_tick
            progress=min(1,max(0,elapsed/duration))
            sx,sy=a.casualty_start; tx,ty=a.casualty_target
            a.x=sx+(tx-sx)*progress; a.y=sy+(ty-sy)*progress

    def _move_agents(self):
        for a in self.agents:
            if a.state==AgentState.DEAD: continue
            if a.state==AgentState.WOUNDED:
                if a.casualty_target is not None:
                    dx=a.casualty_target[0]-a.x; dy=a.casualty_target[1]-a.y
                    dist=max(1.0,(dx*dx+dy*dy)**.5)
                    a.x,a.y=self.world.clamp(a.x+dx/dist*.12,a.y+dy/dist*.12)
                continue
            a.suppression=max(0.0,a.suppression-.012)
            if a.suppression>.18:
                if a.cover_x is None:
                    cover=self.world.nearest_cover(a.x,a.y)
                    if cover: a.cover_x,a.cover_y=cover
                if a.cover_x is not None:
                    dx=a.cover_x-a.x; dy=a.cover_y-a.y
                    dist=max(1.0,(dx*dx+dy*dy)**.5)
                    a.x,a.y=self.world.clamp(a.x+dx/dist*.22,a.y+dy/dist*.22)
            elif a.cover_x is not None and (a.x-a.cover_x)**2+(a.y-a.cover_y)**2<1.0:
                a.cover_x=a.cover_y=None
            if a.reload_ticks>0:
                a.reload_ticks-=1
                if a.reload_ticks==0: a.ammo=self.config.magazine_size

    def _abstract_encounters(self):
        blue=[a for a in self.agents if a.team==Team.BLUE and a.is_operational]
        red=[a for a in self.agents if a.team==Team.RED and a.is_operational]
        if not blue or not red: return
        attempts=min(len(blue),len(red),max(1,(len(blue)+len(red))//8))
        for _ in range(attempts):
            if self.rng.random()>=self.config.encounter_probability: continue
            source=self.rng.choice(blue if self.rng.random()<.5 else red)
            opposing=red if source.team==Team.BLUE else blue
            target=self.rng.choice(opposing)
            target.suppression=min(1.0,target.suppression+.16)
            if source.reload_ticks>0: continue
            if source.ammo<=0:
                source.reload_ticks=self.config.reload_duration
                continue
            source.ammo-=1; source.shots_fired+=1; source.fire_flash_until=self.tick+2
            # Cover and experience influence the abstract chance, not a physical ballistics model.
            target_feature=self.world.feature_at(target.x,target.y)
            cover_bonus=target_feature.cover if target_feature else 0.0
            experience_bonus=source.experience*.10
            accuracy=max(.04,min(.8,self.config.hit_probability+experience_bonus-cover_bonus*.22
                                 -source.suppression*.12))
            hit=self.rng.random()<accuracy
            self.tracers.append(Tracer(source.agent_id,target.agent_id,(source.x,source.y),
                                       (target.x,target.y),self.tick,hit))
            if hit:
                previous=target.state
                target.apply_abstract_hit(self.config.wound_severity)
                target.hit_flash_until=self.tick+4
                if previous==AgentState.ACTIVE and target.state!=AgentState.ACTIVE:
                    self._send_to_casualty_area(target)

    def step(self):
        if self.tick>=self.config.steps: return False
        self._move_agents(); self._abstract_encounters()
        self.tick+=1; self._advance_casualties()
        self.tracers=[t for t in self.tracers if self.tick-t.created_at<=self.config.tracer_lifetime]
        self.record(); return True

    def record(self):
        row={"tick":self.tick}
        for team in Team:
            members=[a for a in self.agents if a.team==team]
            row[f"{team.value}_active"]=sum(a.state==AgentState.ACTIVE for a in members)
            row[f"{team.value}_wounded"]=sum(a.state==AgentState.WOUNDED for a in members)
            row[f"{team.value}_dead"]=sum(a.state==AgentState.DEAD for a in members)
            row[f"{team.value}_shots"]=sum(a.shots_fired for a in members)
            row[f"{team.value}_ammo"]=sum(a.ammo for a in members)
        self.history.append(row)

    def run(self):
        while self.step(): pass
        return self.history[-1]
    def summary(self): return self.history[-1].copy()
