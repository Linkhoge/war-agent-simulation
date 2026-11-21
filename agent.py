"""Agents, teams, states, and a recognisable army rank ladder."""
from dataclasses import dataclass, field
from enum import Enum


class Team(str, Enum):
    BLUE = "blue"
    RED = "red"


class Rank(str, Enum):
    # A simplified U.S.-style land-force progression. Some pay grades have
    # alternative titles in real services; this model chooses one title each.
    RECRUIT = "recruit"
    PRIVATE = "private"
    PRIVATE_FIRST_CLASS = "private_first_class"
    SPECIALIST = "specialist"
    CORPORAL = "corporal"
    SERGEANT = "sergeant"
    STAFF_SERGEANT = "staff_sergeant"
    SERGEANT_FIRST_CLASS = "sergeant_first_class"
    MASTER_SERGEANT = "master_sergeant"
    SERGEANT_MAJOR = "sergeant_major"
    WARRANT_OFFICER_1 = "warrant_officer_1"
    CHIEF_WARRANT_OFFICER_2 = "chief_warrant_officer_2"
    CHIEF_WARRANT_OFFICER_3 = "chief_warrant_officer_3"
    CHIEF_WARRANT_OFFICER_4 = "chief_warrant_officer_4"
    CHIEF_WARRANT_OFFICER_5 = "chief_warrant_officer_5"
    SECOND_LIEUTENANT = "second_lieutenant"
    FIRST_LIEUTENANT = "first_lieutenant"
    CAPTAIN = "captain"
    MAJOR = "major"
    LIEUTENANT_COLONEL = "lieutenant_colonel"
    COLONEL = "colonel"
    BRIGADIER_GENERAL = "brigadier_general"
    MAJOR_GENERAL = "major_general"
    LIEUTENANT_GENERAL = "lieutenant_general"
    GENERAL = "general"


class AgentState(str, Enum):
    ACTIVE = "active"
    WOUNDED = "wounded"
    DEAD = "dead"


RANK_LABELS = {
    Rank.RECRUIT: ("Recruit", "REC"),
    Rank.PRIVATE: ("Private", "PVT"),
    Rank.PRIVATE_FIRST_CLASS: ("Private First Class", "PFC"),
    Rank.SPECIALIST: ("Specialist", "SPC"),
    Rank.CORPORAL: ("Corporal", "CPL"),
    Rank.SERGEANT: ("Sergeant", "SGT"),
    Rank.STAFF_SERGEANT: ("Staff Sergeant", "SSG"),
    Rank.SERGEANT_FIRST_CLASS: ("Sergeant First Class", "SFC"),
    Rank.MASTER_SERGEANT: ("Master Sergeant", "MSG"),
    Rank.SERGEANT_MAJOR: ("Sergeant Major", "SGM"),
    Rank.WARRANT_OFFICER_1: ("Warrant Officer 1", "WO1"),
    Rank.CHIEF_WARRANT_OFFICER_2: ("Chief Warrant Officer 2", "CW2"),
    Rank.CHIEF_WARRANT_OFFICER_3: ("Chief Warrant Officer 3", "CW3"),
    Rank.CHIEF_WARRANT_OFFICER_4: ("Chief Warrant Officer 4", "CW4"),
    Rank.CHIEF_WARRANT_OFFICER_5: ("Chief Warrant Officer 5", "CW5"),
    Rank.SECOND_LIEUTENANT: ("Second Lieutenant", "2LT"),
    Rank.FIRST_LIEUTENANT: ("First Lieutenant", "1LT"),
    Rank.CAPTAIN: ("Captain", "CPT"),
    Rank.MAJOR: ("Major", "MAJ"),
    Rank.LIEUTENANT_COLONEL: ("Lieutenant Colonel", "LTC"),
    Rank.COLONEL: ("Colonel", "COL"),
    Rank.BRIGADIER_GENERAL: ("Brigadier General", "BG"),
    Rank.MAJOR_GENERAL: ("Major General", "MG"),
    Rank.LIEUTENANT_GENERAL: ("Lieutenant General", "LTG"),
    Rank.GENERAL: ("General", "GEN"),
}
RANK_ORDER = tuple(Rank)


def rank_index(rank: Rank) -> int:
    return RANK_ORDER.index(rank)


def rank_profile(rank: Rank) -> dict:
    """Return illustrative visual and game attributes for a rank."""
    progress = rank_index(rank) / max(1, len(RANK_ORDER) - 1)
    return {
        "visual_scale": 0.68 + 0.72 * progress,
        "resilience": 0.55 + 0.39 * progress,
        "experience": 0.10 + 0.88 * progress,
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
    fire_flash_until: int = -1
    hit_flash_until: int = -1
    casualty_start: tuple[float, float] | None = None
    casualty_target: tuple[float, float] | None = None
    casualty_started_tick: int = -1
    metadata: dict = field(default_factory=dict)

    @property
    def profile(self):
        return rank_profile(self.rank)

    @property
    def rank_name(self):
        return RANK_LABELS[self.rank][0]

    @property
    def rank_abbreviation(self):
        return RANK_LABELS[self.rank][1]

    @property
    def seniority(self):
        return rank_index(self.rank)

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
        """Apply an illustrative game hit; rank adjusts abstract health loss."""
        if self.state != AgentState.ACTIVE:
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
