"""Agents, WWII rank titles, and simple battlefield behaviour."""
from dataclasses import dataclass, field
from enum import Enum


class Team(str, Enum):
    BLUE = "blue"
    RED = "red"


class USRank(str, Enum):
    PRIVATE="private"; PRIVATE_FIRST_CLASS="private_first_class"
    TECHNICIAN_FIFTH_GRADE="technician_fifth_grade"; CORPORAL="corporal"
    TECHNICIAN_FOURTH_GRADE="technician_fourth_grade"; SERGEANT="sergeant"
    TECHNICIAN_THIRD_GRADE="technician_third_grade"; STAFF_SERGEANT="staff_sergeant"
    TECHNICAL_SERGEANT="technical_sergeant"; FIRST_SERGEANT="first_sergeant"
    MASTER_SERGEANT="master_sergeant"; WARRANT_OFFICER_JUNIOR_GRADE="warrant_officer_junior_grade"
    WARRANT_OFFICER="warrant_officer"; SECOND_LIEUTENANT="second_lieutenant"
    FIRST_LIEUTENANT="first_lieutenant"; CAPTAIN="captain"; MAJOR="major"
    LIEUTENANT_COLONEL="lieutenant_colonel"; COLONEL="colonel"
    BRIGADIER_GENERAL="brigadier_general"; MAJOR_GENERAL="major_general"
    LIEUTENANT_GENERAL="lieutenant_general"; GENERAL="general"


class GermanRank(str, Enum):
    SCHUTZE="schuetze"; OBERSCHUTZE="oberschuetze"; GEFREITER="gefreiter"
    OBERGEFREITER="obergefreiter"; STABSGEFREITER="stabgefreiter"
    UNTEROFFIZIER="unteroffizier"; UNTERFELDWEBEL="unterfeldwebel"
    FELDWEBEL="feldwebel"; OBERFELDWEBEL="oberfeldwebel"
    STABSFELDWEBEL="stabsfeldwebel"; LEUTNANT="leutnant"
    OBERLEUTNANT="oberleutnant"; HAUPTMANN="hauptmann"; MAJOR="major"
    OBERSTLEUTNANT="oberstleutnant"; OBERST="oberst"
    GENERALMAJOR="generalmajor"; GENERALLEUTNANT="generalleutnant"
    GENERAL_DER_INFANTERIE="general_der_infanterie"; GENERALOBERST="generaloberst"
    GENERALFELDMARSCHALL="generalfeldmarschall"


Rank = USRank
US_RANK_ORDER = tuple(USRank)
GERMAN_RANK_ORDER = tuple(GermanRank)
RANK_ORDERS = {Team.BLUE: US_RANK_ORDER, Team.RED: GERMAN_RANK_ORDER}
RANK_ORDER = US_RANK_ORDER


class AgentState(str, Enum):
    ACTIVE = "active"
    WOUNDED = "wounded"
    DEAD = "dead"


RANK_LABELS = {
    USRank.PRIVATE:("Private","PVT"), USRank.PRIVATE_FIRST_CLASS:("Private First Class","PFC"),
    USRank.TECHNICIAN_FIFTH_GRADE:("Technician Fifth Grade","T/5"), USRank.CORPORAL:("Corporal","CPL"),
    USRank.TECHNICIAN_FOURTH_GRADE:("Technician Fourth Grade","T/4"), USRank.SERGEANT:("Sergeant","SGT"),
    USRank.TECHNICIAN_THIRD_GRADE:("Technician Third Grade","T/3"), USRank.STAFF_SERGEANT:("Staff Sergeant","SSG"),
    USRank.TECHNICAL_SERGEANT:("Technical Sergeant","TSG"), USRank.FIRST_SERGEANT:("First Sergeant","1SG"),
    USRank.MASTER_SERGEANT:("Master Sergeant","MSG"), USRank.WARRANT_OFFICER_JUNIOR_GRADE:("Warrant Officer Junior Grade","WOJG"),
    USRank.WARRANT_OFFICER:("Warrant Officer","WO"), USRank.SECOND_LIEUTENANT:("Second Lieutenant","2LT"),
    USRank.FIRST_LIEUTENANT:("First Lieutenant","1LT"), USRank.CAPTAIN:("Captain","CPT"),
    USRank.MAJOR:("Major","MAJ"), USRank.LIEUTENANT_COLONEL:("Lieutenant Colonel","LTC"),
    USRank.COLONEL:("Colonel","COL"), USRank.BRIGADIER_GENERAL:("Brigadier General","BG"),
    USRank.MAJOR_GENERAL:("Major General","MG"), USRank.LIEUTENANT_GENERAL:("Lieutenant General","LTG"),
    USRank.GENERAL:("General","GEN"),
    GermanRank.SCHUTZE:("Schütze","SCH"), GermanRank.OBERSCHUTZE:("Oberschütze","OBS"),
    GermanRank.GEFREITER:("Gefreiter","GFR"), GermanRank.OBERGEFREITER:("Obergefreiter","OGF"),
    GermanRank.STABSGEFREITER:("Stabsgefreiter","SGF"), GermanRank.UNTEROFFIZIER:("Unteroffizier","UO"),
    GermanRank.UNTERFELDWEBEL:("Unterfeldwebel","UFW"), GermanRank.FELDWEBEL:("Feldwebel","FW"),
    GermanRank.OBERFELDWEBEL:("Oberfeldwebel","OFW"), GermanRank.STABSFELDWEBEL:("Stabsfeldwebel","SFW"),
    GermanRank.LEUTNANT:("Leutnant","LT"), GermanRank.OBERLEUTNANT:("Oberleutnant","OLT"),
    GermanRank.HAUPTMANN:("Hauptmann","HPT"), GermanRank.MAJOR:("Major","MAJ"),
    GermanRank.OBERSTLEUTNANT:("Oberstleutnant","OL"), GermanRank.OBERST:("Oberst","OBS"),
    GermanRank.GENERALMAJOR:("Generalmajor","GM"), GermanRank.GENERALLEUTNANT:("Generalleutnant","GL"),
    GermanRank.GENERAL_DER_INFANTERIE:("General der Infanterie","GDI"),
    GermanRank.GENERALOBERST:("Generaloberst","GO"), GermanRank.GENERALFELDMARSCHALL:("Generalfeldmarschall","GFM"),
}


def rank_index(rank):
    order = US_RANK_ORDER if isinstance(rank, USRank) else GERMAN_RANK_ORDER
    return order.index(rank)


def rank_profile(rank):
    progress = rank_index(rank) / max(1, len(US_RANK_ORDER if isinstance(rank, USRank) else GERMAN_RANK_ORDER)-1)
    return {"visual_scale": 0.68+0.72*progress, "resilience": 0.55+0.39*progress,
            "experience": 0.10+0.88*progress}


@dataclass
class Agent:
    agent_id: int
    team: Team
    rank: USRank | GermanRank
    x: float
    y: float
    morale: float = 1.0
    health: float = 1.0
    state: str = "active"
    shots_fired: int = 0
    hits_taken: int = 0
    fire_flash_until: int = -1
    hit_flash_until: int = -1
    casualty_start: tuple[float,float] | None = None
    casualty_target: tuple[float,float] | None = None
    casualty_started_tick: int = -1
    ammo: int = 8
    reload_ticks: int = 0
    suppression: float = 0.0
    cover_x: float | None = None
    cover_y: float | None = None
    metadata: dict = field(default_factory=dict)

    @property
    def profile(self): return rank_profile(self.rank)
    @property
    def rank_name(self): return RANK_LABELS[self.rank][0]
    @property
    def rank_abbreviation(self): return RANK_LABELS[self.rank][1]
    @property
    def seniority(self): return rank_index(self.rank)
    @property
    def visual_scale(self): return self.profile["visual_scale"]
    @property
    def resilience(self): return self.profile["resilience"]
    @property
    def experience(self): return self.profile["experience"]
    @property
    def is_operational(self): return self.state == "active"
    @property
    def is_recruit(self): return bool(self.metadata.get("recruit", False))

    def apply_abstract_hit(self, severity=0.38):
        if not self.is_operational: return
        self.hits_taken += 1
        recruit_factor = 1.18 if self.is_recruit else 1.0
        self.health = max(0.0, self.health-severity*(1.15-self.resilience)*recruit_factor)
        if self.health <= 0: self.state = "dead"
        elif self.health < 0.55: self.state = "wounded"

    def recover_morale(self, amount=0.01):
        if self.state != "dead": self.morale = min(1.0,self.morale+amount)
