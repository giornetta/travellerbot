from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional, Dict, List, Union

from traveller.characteristic import Characteristic as Ch


class ReEnlistmentOutcome(Enum):
    MUST_RETIRE = auto()
    FORCED_CONTINUE = auto()
    SUCCESS = auto()
    FAIL = auto()

class Career:
    career_type: CareerType
    rank: int
    terms: int
    drafted: bool
    injury_crisis_debt: int
    aging_crisis_debt: int

    def __init__(self, career_type: CareerType, drafted=False):
        self.career_type = career_type
        self.rank = 0
        self.terms = 1
        self.drafted = drafted
        self.injury_crisis_debt = 0
        self.aging_crisis_debt = 0

@dataclass
class CareerType:
    name: str
    qualification: Tuple[Ch, int]
    survival: Tuple[Ch, int]
    commission: Optional[Tuple[Ch, int]]
    advancement: Optional[Tuple[Ch, int]]
    re_enlistment: int
    ranks: Dict[int, Union[Ch, str]]
    skill_and_training: List[Dict[int, Union[Ch, str]]]
    material_benefits: Dict[int, Union[Ch, str, int]]  # str for 'Weapon' or 'Society', int for Ship Shares
    cash: Dict[int, int]
    patron_rates: List[float, float, float]


athlete = CareerType(
    name='Athlete',
    qualification=(Ch.END, 8),
    survival=(Ch.DEX, 5),
    commission=None,
    advancement=None,
    re_enlistment=6,
    ranks={0: 'Athletics'},
    skill_and_training=[{1: Ch.DEX, 2: Ch.INT, 3: Ch.EDU, 4: Ch.SOC, 5: "Carousing", 6: "Melee Combat"},
                        {1: 'Athletics', 2: 'Admin', 3: 'Carousing',
                         4: 'Computer', 5: 'Gambling', 6: 'Vehicle'},
                        {1: 'Zero-G', 2: 'Athletics', 3: 'Athletics',
                         4: 'Computer', 5: 'Leadership', 6: 'Gambling'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Liaison',
                         4: 'Linguistics', 5: 'Medicine', 6: 'Sciences'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'LightWeapon', 4: 3, 5: 'Society', 6: 3},
    cash={1: 200, 2: 10000, 3: 20000, 4: 20000, 5: 50000, 6: 100000, 7: 100000},
    patron_rates=[0.5, 0.75, 1]
)

maritime_defense = CareerType(
    name='Maritime Defense',
    qualification=(Ch.END, 5),
    survival=(Ch.END, 5),
    commission=(Ch.INT, 6),
    advancement=(Ch.EDU, 7),
    re_enlistment=5,
    ranks={0: 'Vehicle', 3: 'Leadership'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Athletics', 5: "Melee Combat", 6: "Vehicle"},
                        {1: 'Mechanics', 2: 'Gun Combat', 3: 'Gun Combat',
                         4: 'Melee Combat', 5: 'Survival', 6: 'Vehicle'},
                        {1: 'Comms', 2: 'Electronics', 3: 'Gun Combat',
                         4: 'Demolitions', 5: 'Recon', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Jack-of-All-Trades',
                         4: 'Medicine', 5: 'Leadership', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: 'Rifle', 4: 2, 5: 'Rifle', 6: 3, 7: Ch.SOC},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000},
    patron_rates=[0.75, 1, 1]
)

mercenary = CareerType(
    name='Mercenary',
    qualification=(Ch.INT, 4),
    survival=(Ch.END, 6),
    commission=(Ch.INT, 7),
    advancement=(Ch.END, 6),
    re_enlistment=5,
    ranks={0: 'Gun Combat', 3: 'Tactics'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Zero-G', 5: "Melee Combat", 6: "Gambling"},
                        {1: 'Comms', 2: 'Mechanics', 3: 'Gun Combat',
                         4: 'Melee Combat', 5: 'Gambling', 6: 'Battle Dress'},
                        {1: 'Gravitics', 2: 'Gun Combat', 3: 'Gun Combat',
                         4: 'Melee Combat', 5: 'Recon', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Engineering', 3: 'Medicine',
                         4: 'Medicine', 5: 'Sciences', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'AssaultWeapon', 4: 3, 5: Ch.SOC, 6: 3, 7: -1},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 20000, 5: 20000, 6: 50000, 7: 100000},
    patron_rates=[0.5, 0.75, 1]
)

merchant = CareerType(
    name='Merchant',
    qualification=(Ch.INT, 4),
    survival=(Ch.INT, 5),
    commission=(Ch.INT, 5),
    advancement=(Ch.EDU, 8),
    re_enlistment=4,
    ranks={0: 'Steward', 3: 'Pilot'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Zero-G', 5: "Melee Combat", 6: "Steward"},
                        {1: 'Comms', 2: 'Engineering', 3: 'Gun Combat',
                         4: 'Melee Combat', 5: 'Broker', 6: 'Vehicle'},
                        {1: 'Carousing', 2: 'Gun Combat', 3: 'Jack-of-All-Trades',
                         4: 'Medicine', 5: 'Navigation', 6: 'Piloting'},
                        {1: 'Advocate', 2: 'Engineering', 3: 'Medicine',
                         4: 'Medicine', 5: 'Sciences', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: 'Shotgun', 4: 3, 5: -1, 6: 3, 7: 'Society'},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 20000, 5: 20000, 6: 50000, 7: 100000},
    patron_rates=[0.5, 0.75, 1]
)

navy = CareerType(
    name='Navy',
    qualification=(Ch.INT, 6),
    survival=(Ch.INT, 5),
    commission=(Ch.INT, 7),
    advancement=(Ch.EDU, 6),
    re_enlistment=5,
    ranks={0: 'Zero-G', 3: 'Tactics'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: Ch.INT, 5: Ch.EDU, 6: "Melee Combat"},
                        {1: 'Comms', 2: 'Engineering',
                         3: 'Gun Combat', 4: 'Gun Combat', 5: 'Melee Combat', 6: 'Vehicle'},
                        {1: 'Gravitics', 2: 'Jack-of-All-Trades',
                         3: 'Melee Combat', 4: 'Navigation', 5: 'Leadership', 6: 'Piloting'},
                        {1: 'Advocate', 2: 'Piloting', 3: 'Engineering',
                         4: 'Medicine', 5: 'Navigation', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: 'Rifle', 4: 2, 5: Ch.SOC, 6: 3, 7: 'Society'},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000},
    patron_rates=[0.75, 1, 1]
)

noble = CareerType(
    name='Noble',
    qualification=(Ch.SOC, 8),
    survival=(Ch.SOC, 4),
    commission=(Ch.EDU, 5),
    advancement=(Ch.INT, 8),
    re_enlistment=6,
    ranks={0: 'Carousing', 3: 'Advocate'},
    skill_and_training=[{1: Ch.DEX, 2: Ch.INT, 3: Ch.EDU, 4: Ch.SOC, 5: 'Carousing', 6: "Melee Combat"},
                        {1: 'Athletics', 2: 'Admin', 3: 'Carousing',
                         4: 'Leadership', 5: 'Gambling', 6: 'Vehicle'},
                        {1: 'Computer', 2: 'Carousing', 3: 'Gun Combat',
                         4: 'Melee Combat', 5: 'Liaison', 6: 'Liaison'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Liaison',
                         4: 'Liaison', 5: 'Liaison', 6: 'Sciences'}],
    material_benefits={1: 3, 2: Ch.EDU, 3: Ch.INT, 4: 3, 5: 'Society', 6: 3, 7: -1},
    cash={1: 2000, 2: 10000, 3: 20000, 4: 20000, 5: 50000, 6: 100000, 7: 100000},
    patron_rates=[0.5, 0.75, 1]
)

physician = CareerType(
    name='Physician',
    qualification=(Ch.EDU, 6),
    survival=(Ch.INT, 4),
    commission=(Ch.INT, 5),
    advancement=(Ch.EDU, 8),
    re_enlistment=5,
    ranks={0: 'Medicine', 3: 'Admin'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: Ch.INT, 5: Ch.EDU, 6: "Gun Combat"},
                        {1: 'Admin', 2: 'Computer', 3: 'Mechanics',
                         4: 'Medicine', 5: 'Leadership', 6: 'Sciences'},
                        {1: 'Computer', 2: 'Carousing', 3: 'Electronics',
                         4: 'Medicine', 5: 'Medicine', 6: 'Sciences'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Jack-of-All-Trades',
                         4: 'Linguistics', 5: 'Medicine', 6: 'Sciences'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: Ch.INT, 4: 3, 5: 'Society', 6: 3, 7: Ch.SOC},
    cash={1: 2000, 2: 10000, 3: 20000, 4: 20000, 5: 50000, 6: 100000, 7: 100000},
    patron_rates=[0.5, 0.75, 1]
)

pirate = CareerType(
    name='Pirate',
    qualification=(Ch.DEX, 5),
    survival=(Ch.DEX, 6),
    commission=(Ch.STR, 5),
    advancement=(Ch.INT, 6),
    re_enlistment=5,
    ranks={0: 'Gun Combat', 3: 'Pilot'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Melee Combat', 5: 'Bribery', 6: "Gambling"},
                        {1: 'Streetwise', 2: 'Electronics', 3: 'Gun Combat',
                         4: 'Melee Combat', 5: 'Recon', 6: 'Vehicle'},
                        {1: 'Zero-G', 2: 'Comms', 3: 'Engineering',
                         4: 'Gun Combat', 5: 'Navigation', 6: 'Navigation'},
                        {1: 'Computer', 2: 'Gravitics', 3: 'Jack-of-All-Trades',
                         4: 'Medicine', 5: 'Advocate', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'Sword', 4: 2, 5: Ch.SOC, 6: 3, 7: Ch.SOC},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 20000, 5: 20000, 6: 50000, 7: 100000},
    patron_rates=[0.5, 0.75, 1]
)

rogue = CareerType(
    name='Rogue',
    qualification=(Ch.DEX, 5),
    survival=(Ch.DEX, 4),
    commission=(Ch.STR, 6),
    advancement=(Ch.INT, 7),
    re_enlistment=4,
    ranks={0: 'Streetwise', 3: 'Gun Combat'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Melee Combat', 5: 'Bribery', 6: "Gambling"},
                        {1: 'Streetwise', 2: 'Mechanics', 3: 'Gun Combat',
                         4: 'Melee Combat', 5: 'Recon', 6: 'Vehicle'},
                        {1: 'Computer', 2: 'Electronics', 3: 'Bribery',
                         4: 'Broker', 5: 'Recon', 6: 'Vehicle'},
                        {1: 'Computer', 2: 'Gravitics', 3: 'Jack-of-All-Trades',
                         4: 'Medicine', 5: 'Advocate', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'LightWeapon', 4: 2, 5: 'LightWeapon', 6: 3, 7: Ch.SOC},
    cash={1: 1000, 2: 5000, 3: 5000, 4: 5000, 5: 10000, 6: 20000, 7: 50000},
    patron_rates=[0, 0.5, 0.75]
)

scientist = CareerType(
    name='Scientist',
    qualification=(Ch.EDU, 6),
    survival=(Ch.EDU, 5),
    commission=(Ch.INT, 7),
    advancement=(Ch.INT, 6),
    re_enlistment=5,
    ranks={0: 'Sciences', 3: 'Computer'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: Ch.INT, 5: Ch.EDU, 6: "Gun Combat"},
                        {1: 'Admin', 2: 'Computer', 3: 'Electronics', 4: 'Electronics', 5: 'Bribery', 6: 'Sciences'},
                        {1: 'Sciences', 2: 'Admin', 3: 'Sciences', 4: 'Sciences', 5: 'Animals', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Jack-of-All-Trades', 4: 'Linguistics', 5: 'Medicine',
                         6: 'Sciences'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: Ch.INT, 4: 2, 5: Ch.SOC, 6: 3, 7: 5},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000},
    patron_rates=[0.5, 0.75, 1]
)

scout = CareerType(
    name='Scout',
    qualification=(Ch.INT, 6),
    survival=(Ch.EDU, 7),
    commission=None,
    advancement=None,
    re_enlistment=6,
    ranks={0: 'Pilot'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Jack-of-All-Trades', 5: Ch.EDU, 6: "Melee Combat"},
                        {1: 'Comms', 2: 'Electronics', 3: 'Gun Combat', 4: 'Gun Combat', 5: 'Recon', 6: 'Piloting'},
                        {1: 'Engineering', 2: 'Gun Combat', 3: 'Demolitions', 4: 'Navigation', 5: 'Medicine', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Linguistics', 4: 'Medicine', 5: 'Navigation', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: 'Pistol', 4: 2, 5: 'Society', 6: 4},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000},
    patron_rates=[0.75, 1, 1]
)

aerospace_defense = CareerType(
    name='Aerospace Defense',
    qualification=(Ch.END, 5),
    survival=(Ch.DEX, 5),
    commission=(Ch.EDU, 6),
    advancement=(Ch.EDU, 7),
    re_enlistment=5,
    ranks={0: 'Aircraft', 3: 'Leadership'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Athletics', 5: 'Melee Combat', 6: 'Vehicle'},
                        {1: 'Electronics', 2: 'Gun Combat', 3: 'Gun Combat',
                         4: 'Melee Combat', 5: 'Survival', 6: 'Vehicle'},
                        {1: 'Comms', 2: 'Gravitics', 3: 'Gun Combat',
                         4: 'Gun Combat', 5: 'Recon', 6: 'Piloting'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Jack-of-All-Trades',
                         4: 'Medicine', 5: 'Leadership', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: 'Rifle', 4: 2, 5: 3, 6: 3, 7: Ch.SOC},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000},
    patron_rates=[0.75, 1, 1]
)

agent = CareerType(
    name='Agent',
    qualification=(Ch.SOC, 6),
    survival=(Ch.INT, 6),
    commission=(Ch.EDU, 7),
    advancement=(Ch.EDU, 6),
    re_enlistment=6,
    ranks={0: 'Streetwise', 4: 'Leadership'},
    skill_and_training=[{1: Ch.DEX, 2: Ch.END, 3: Ch.INT, 4: Ch.EDU, 5: 'Athletics', 6: 'Carousing'},
                        {1: 'Admin', 2: 'Computer', 3: 'Streetwise',
                         4: 'Bribery', 5: 'Leadership', 6: 'Vehicle'},
                        {1: 'Gun Combat', 2: 'Melee Combat', 3: 'Bribery',
                         4: 'Leadership', 5: 'Recon', 6: 'Survival'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Liaison',
                         4: 'Linguistics', 5: 'Medicine', 6: 'Leadership'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'Pistol', 4: 2, 5: Ch.SOC, 6: 3, 7: 'Society'},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000},
    patron_rates=[0.5, 0.75, 1]
)

barbarian = CareerType(
    name='Barbarian',
    qualification=(Ch.END, 5),
    survival=(Ch.STR, 6),
    commission=None,
    advancement=None,
    re_enlistment=5,
    ranks={0: 'Melee Combat'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: Ch.INT, 5: 'Athletics', 6: 'Gun Combat'},
                        {1: 'Mechanics', 2: 'Gun Combat', 3: 'Melee Combat',
                         4: 'Recon', 5: 'Survival', 6: 'Animals'},
                        {1: 'Gun Combat', 2: 'Jack-of-All-Trades', 3: 'Melee Combat',
                         4: 'Recon', 5: 'Recon', 6: 'Animals'},
                        {1: 'Advocate', 2: 'Linguistics', 3: 'Medicine',
                         4: 'Leadership', 5: 'Tactics', 6: 'Broker'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'HeavyWeapon', 4: 'HeavyWeapon', 5: Ch.END, 6: 2},
    cash={1: 0, 2: 1000, 3: 2000, 4: 5000, 5: 5000, 6: 10000, 7: 10000},
    patron_rates=[0, 0.5, 0.75]
)

belter = CareerType(
    name='Belter',
    qualification=(Ch.INT, 4),
    survival=(Ch.DEX, 7),
    commission=None,
    advancement=None,
    re_enlistment=5,
    ranks={0: 'Zero-G'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Zero-G', 5: 'Melee Combat', 6: 'Gambling'},
                        {1: 'Comms', 2: 'Demolition', 3: 'Gun Combat',
                         4: 'Gun Combat', 5: 'Prospecting', 6: 'Piloting'},
                        {1: 'Zero-G', 2: 'Computer', 3: 'Electronics',
                         4: 'Prospecting', 5: 'Sciences', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Engineering', 3: 'Medicine',
                         4: 'Navigation', 5: 'Comms', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'HeavyWeapon', 4: 2, 5: -1, 6: 3},
    cash={1: 1000, 2: 5000, 3: 5000, 4: 5000, 5: 10000, 6: 20000, 7: 50000},
    patron_rates=[0, 0.5, 0.75]
)

bureaucrat = CareerType(
    name='Bureaucrat',
    qualification=(Ch.SOC, 6),
    survival=(Ch.EDU, 4),
    commission=(Ch.SOC, 5),
    advancement=(Ch.INT, 8),
    re_enlistment=5,
    ranks={0: 'Admin', 4: 'Advocate'},
    skill_and_training=[{1: Ch.DEX, 2: Ch.END, 3: Ch.INT, 4: Ch.EDU, 5: 'Athletics', 6: 'Carousing'},
                        {1: 'Admin', 2: 'Computer', 3: 'Carousing',
                         4: 'Bribery', 5: 'Leadership', 6: 'Vehicle'},
                        {1: 'Admin', 2: 'Computer', 3: 'Perception',
                         4: 'Leadership', 5: 'Steward', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Liaison',
                         4: 'Linguistics', 5: 'Medicine', 6: 'Admin'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: Ch.INT, 4: 2, 5: 2, 6: 3, 7: Ch.SOC},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000},
    patron_rates=[0.5, 0.75, 1]
)

colonist = CareerType(
    name='Colonist',
    qualification=(Ch.END, 5),
    survival=(Ch.EDU, 6),
    commission=(Ch.INT, 7),
    advancement=(Ch.EDU, 6),
    re_enlistment=5,
    ranks={0: 'Survival', 3: 'Liaison'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: Ch.INT, 5: 'Athletics', 6: 'Gun Combat'},
                        {1: 'Mechanics', 2: 'Gun Combat', 3: 'Animals',
                         4: 'Electronics', 5: 'Survival', 6: 'Vehicle'},
                        {1: 'Athletics', 2: 'Carousing', 3: 'Jack-of-All-Trades',
                         4: 'Engineering', 5: 'Animals', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Linguistics', 3: 'Medicine',
                         4: 'Liaison', 5: 'Admin', 6: 'Animals'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'Sword', 4: 2, 5: 2, 6: 3, 7: Ch.SOC},
    cash={1: 1000, 2: 5000, 3: 5000, 4: 5000, 5: 10000, 6: 20000, 7: 50000},
    patron_rates=[0, 0.5, 0.75]
)

diplomat = CareerType(
    name='Diplomat',
    qualification=(Ch.SOC, 6),
    survival=(Ch.EDU, 5),
    commission=(Ch.INT, 7),
    advancement=(Ch.SOC, 7),
    re_enlistment=5,
    ranks={0: 'Liaison', 3: 'Admin'},
    skill_and_training=[{1: Ch.DEX, 2: Ch.END, 3: Ch.INT, 4: Ch.EDU, 5: 'Athletics', 6: 'Carousing'},
                        {1: 'Admin', 2: 'Computer', 3: 'Carousing',
                         4: 'Bribery', 5: 'Liaison', 6: 'Vehicle'},
                        {1: 'Carousing', 2: 'Linguistics', 3: 'Bribery',
                         4: 'Liaison', 5: 'Steward', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Liaison',
                         4: 'Linguistics', 5: 'Medicine', 6: 'Leadership'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: 2, 4: 3, 5: Ch.SOC, 6: 3, 7: 'Society'},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 20000, 5: 20000, 6: 50000, 7: 100000},
    patron_rates=[0.5, 0.75, 1]
)

drifter = CareerType(
    name='Drifter',
    qualification=(Ch.DEX, 5),
    survival=(Ch.END, 5),
    commission=None,
    advancement=None,
    re_enlistment=5,
    ranks={},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Melee Combat', 5: 'Bribery', 6: 'Gambling'},
                        {1: 'Streetwise', 2: 'Mechanics', 3: 'Gun Combat',
                         4: 'Melee Combat', 5: 'Recon', 6: 'Vehicle'},
                        {1: 'Electronics', 2: 'Melee Combat', 3: 'Bribery',
                         4: 'Streetwise', 5: 'Gambling', 6: 'Recon'},
                        {1: 'Computer', 2: 'Engineering', 3: 'Jack-of-All-Trades',
                         4: 'Medicine', 5: 'Liaison', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'Pistol', 4: 'Pistol', 5: 2, 6: 2},
    cash={1: 0, 2: 1000, 3: 2000, 4: 5000, 5: 5000, 6: 10000, 7: 10000},
    patron_rates=[0, 0.5, 0.75]
)

entertainer = CareerType(
    name='Entertainer',
    qualification=(Ch.SOC, 8),
    survival=(Ch.INT, 4),
    commission=None,
    advancement=None,
    re_enlistment=6,
    ranks={0: 'Carousing'},
    skill_and_training=[{1: Ch.DEX, 2: Ch.INT, 3: Ch.EDU, 4: Ch.SOC, 5: 'Carousing', 6: 'Melee Combat'},
                        {1: 'Athletics', 2: 'Admin', 3: 'Carousing',
                         4: 'Bribery', 5: 'Gambling', 6: 'Vehicle'},
                        {1: 'Computer', 2: 'Carousing', 3: 'Bribery',
                         4: 'Liaison', 5: 'Gambling', 6: 'Recon'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Carousing',
                         4: 'Linguistics', 5: 'Medicine', 6: 'Sciences'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: Ch.SOC, 4: 3, 5: 'Society', 6: 3},
    cash={1: 2000, 2: 10000, 3: 20000, 4: 20000, 5: 50000, 6: 100000, 7: 100000},
    patron_rates=[0.5, 0.75, 1]
)

hunter = CareerType(
    name='Hunter',
    qualification=(Ch.END, 5),
    survival=(Ch.INT, 8),
    commission=None,
    advancement=None,
    re_enlistment=6,
    ranks={0: 'Survival'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: Ch.INT, 5: 'Athletics', 6: 'Gun Combat'},
                        {1: 'Mechanics', 2: 'Gun Combat', 3: 'Melee Combat ',
                         4: 'Recon', 5: 'Survival', 6: 'Vehicle'},
                        {1: 'Admin', 2: 'Comms', 3: 'Electronics',
                         4: 'Recon', 5: 'Animals', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Linguistics', 3: 'Medicine',
                         4: 'Liaison', 5: 'Tactics', 6: 'Animals'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'Bow', 4: 3, 5: -1, 6: 3},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 20000, 5: 20000, 6: 50000, 7: 100000},
    patron_rates=[0.5, 0.75, 1]
)

marine = CareerType(
    name='Marine',
    qualification=(Ch.SOC, 6),
    survival=(Ch.EDU, 6),
    commission=(Ch.INT, 6),
    advancement=(Ch.SOC, 7),
    re_enlistment=6,
    ranks={0: 'Zero-G', 3: 'Tactics'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: Ch.INT, 5: Ch.EDU, 6: 'Melee Combat'},
                        {1: 'Comms', 2: 'Demolitions', 3: 'Gun Combat',
                         4: 'Gun Combat', 5: 'Melee Combat', 6: 'Battle Dress'},
                        {1: 'Electronics', 2: 'Gun Combat', 3: 'Melee Combat',
                         4: 'Survival', 5: 'Recon', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Gravitics',
                         4: 'Medicine', 5: 'Navigation', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: 'Rifle', 4: 2, 5: Ch.SOC, 6: 3, 7: 'Society'},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000},
    patron_rates=[0.75, 1, 1]
)

technician = CareerType(
    name='Technician',
    qualification=(Ch.EDU, 6),
    survival=(Ch.DEX, 4),
    commission=(Ch.EDU, 5),
    advancement=(Ch.INT, 8),
    re_enlistment=5,
    ranks={0: 'Computer', 4: 'Admin'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: Ch.INT, 5: Ch.EDU, 6: 'Gun Combat'},
                        {1: 'Admin', 2: 'Computer', 3: 'Mechanics',
                         4: 'Medicine', 5: 'Electronics', 6: 'Sciences'},
                        {1: 'Computer', 2: 'Electronics', 3: 'Gravitics',
                         4: 'Linguistics', 5: 'Engineering', 6: 'Animals'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Jack-of-All-Trades',
                         4: 'Linguistics', 5: 'Medicine', 6: 'Sciences'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: Ch.INT, 4: 2, 5: 2, 6: 3, 7: Ch.SOC},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000},
    patron_rates=[0.5, 0.75, 1]
)

surface_defense = CareerType(
    name='Surface Defense',
    qualification=(Ch.END, 5),
    survival=(Ch.EDU, 5),
    commission=(Ch.END, 6),
    advancement=(Ch.EDU, 7),
    re_enlistment=5,
    ranks={0: 'Gun Combat', 3: 'Leadership'},
    skill_and_training=[{1: Ch.DEX, 2: Ch.INT, 3: Ch.EDU, 4: Ch.SOC, 5: 'Carousing', 6: 'Melee Combat'},
                        {1: 'Mechanics', 2: 'Gun Combat', 3: 'Gun Combat',
                         4: 'Melee Combat', 5: 'Recon', 6: 'Battle Dress'},
                        {1: 'Comms', 2: 'Demolitions', 3: 'Gun Combat',
                         4: 'Melee Combat', 5: 'Survival', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Jack-of-All-Trades',
                         4: 'Medicine', 5: 'Leadership', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'Rifle', 4: 2, 5: 'Rifle', 6: 3, 7: Ch.SOC},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000},
    patron_rates=[0.75, 1, 1]
)

careers: Dict[str, CareerType] = {
    athlete.name: athlete,
    maritime_defense.name: maritime_defense,
    mercenary.name: mercenary,
    merchant.name: merchant,
    navy.name: navy,
    noble.name: noble,
    physician.name: physician,
    pirate.name: pirate,
    rogue.name: rogue,
    scientist.name: scientist,
    scout.name: scout,
    aerospace_defense.name: aerospace_defense,
    agent.name: agent,
    barbarian.name: barbarian,
    belter.name: belter,
    bureaucrat.name: bureaucrat,
    colonist.name: colonist,
    diplomat.name: diplomat,
    drifter.name: drifter,
    entertainer.name: entertainer,
    hunter.name: hunter,
    marine.name: marine,
    technician.name: technician,
    surface_defense.name: surface_defense
}
