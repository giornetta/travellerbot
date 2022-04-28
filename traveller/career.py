from dataclasses import dataclass
from typing import Tuple, Optional, Dict, List, Union

from traveller.common import Characteristics as Ch


@dataclass
class Career:
    name: str
    qualification: Tuple[Ch, int]
    survival: Tuple[Ch, int]
    commission: Optional[Ch, int]
    advancement: Optional[Ch, int]
    re_enlistment: int
    ranks: Dict[int, Union[Ch, str]]
    skill_and_training: List[Dict[int, str]]
    material_benefits: Dict[int, Union[Ch, str, int]]  # str for 'Weapon' or 'Society', int for Ship Shares
    cash: Dict[int, int]


athlete = Career(
    name='Athlete',
    qualification=(Ch.END, 8),
    survival=(Ch.DEX, 5),
    commission=None,
    advancement=None,
    re_enlistment=6,
    ranks={0: 'Athletics'},
    skill_and_training=[{1: Ch.DEX, 2: Ch.INT, 3: Ch.EDU, 4: Ch.SOC, 5: "Carousing", 6: "Melee Combat"},
                        {1: 'Athletics', 2: 'Admin', 3: 'Carousing', 4: 'Computer', 5: 'Gambling', 6: 'Vehicle'},
                        {1: 'Zero-G', 2: 'Athletics', 3: 'Athletics', 4: 'Computer', 5: 'Leadership', 6: 'Gambling'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Liaison', 4: 'Linguistics', 5: 'Medicine', 6: 'Sciences'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'Weapon', 4: 3, 5: 'Society', 6: 3},
    cash={1: 200, 2: 10000, 3: 20000, 4: 20000, 5: 50000, 6: 100000, 7: 100000}
)

maritime_defence = Career(
    name='Maritime Defense',
    qualification=(Ch.END, 5),
    survival=(Ch.END, 5),
    commission=(Ch.INT, 6),
    advancement=(Ch.EDU, 7),
    re_enlistment=5,
    ranks={0: 'Vehicle',
           3: 'Leadership'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Athletics', 5: "Melee Combat", 6: "Vehicle"},
                        {1: 'Mechanics', 2: 'Gun Combat', 3: 'Gunnery', 4: 'Melee Combat', 5: 'Survival', 6: 'Vehicle'},
                        {1: 'Comms', 2: 'Electronics', 3: 'Gun Combat', 4: 'Demolitions', 5: 'Recon', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Jack-of-All-Trades', 4: 'Medicine', 5: 'Leadership', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: 'Weapon', 4: 2, 5: 'Weapon', 6: 3, 7: Ch.SOC},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000}
)

mercenary = Career(
    name='Mercenary',
    qualification=(Ch.INT, 4),
    survival=(Ch.END, 6),
    commission=(Ch.INT, 7),
    advancement=(Ch.END, 6),
    re_enlistment=5,
    ranks={0: 'Gun Combat',
           3: 'Tactics'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Zero-G', 5: "Melee Combat", 6: "Gambling"},
                        {1: 'Comms', 2: 'Mechanics', 3: 'Gun Combat', 4: 'Melee Combat', 5: 'Gambling', 6: 'Battle Dress'},
                        {1: 'Gravitics', 2: 'Gun Combat', 3: 'Gunnery', 4: 'Melee Combat', 5: 'Recon', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Engineering', 3: 'Medicine', 4: 'Medicine', 5: 'Sciences', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'Weapon', 4: 3, 5: Ch.SOC, 6: 3, 7: -1},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 20000, 5: 20000, 6: 50000, 7: 100000}
)

merchant = Career(
    name='Merchant',
    qualification=(Ch.INT, 4),
    survival=(Ch.INT, 5),
    commission=(Ch.INT, 5),
    advancement=(Ch.EDU, 8),
    re_enlistment=4,
    ranks={0: 'Steward',
           3: 'Pilot'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Zero-G', 5: "Melee Combat", 6: "Steward"},
                        {1: 'Comms', 2: 'Engineering', 3: 'Gun Combat', 4: 'Melee Combat', 5: 'Broker', 6: 'Vehicle'},
                        {1: 'Carousing', 2: 'Gunnery', 3: 'Jack-of-All-Trades', 4: 'Medicine', 5: 'Navigation', 6: 'Piloting'},
                        {1: 'Advocate', 2: 'Engineering', 3: 'Medicine', 4: 'Medicine', 5: 'Sciences', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: 'Weapon', 4: 3, 5: -1, 6: 3, 7: 'Society'},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 20000, 5: 20000, 6: 50000, 7: 100000}
)

navy = Career(
    name='Navy',
    qualification=(Ch.INT, 6),
    survival=(Ch.INT, 5),
    commission=(Ch.INT, 7),
    advancement=(Ch.EDU, 6),
    re_enlistment=5,
    ranks={0: 'Zero-G',
           3: 'Tactics'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: Ch.INT, 5: Ch.EDU, 6: "Melee Combat"},
                        {1: 'Comms', 2: 'Engineering', 3: 'Gun Combat', 4: 'Gunnery', 5: 'Melee Combat', 6: 'Vehicle'},
                        {1: 'Gravitics', 2: 'Jack-of-All-Trades', 3: 'Melee Combat', 4: 'Navigation', 5: 'Leadership', 6: 'Piloting'},
                        {1: 'Advocate', 2: 'Piloting', 3: 'Engineering', 4: 'Medicine', 5: 'Navigation', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: 'Weapon', 4: 2, 5: Ch.SOC, 6: 3, 7: 'Society'},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000}
)

noble = Career(
    name='Noble',
    qualification=(Ch.SOC, 8),
    survival=(Ch.SOC, 4),
    commission=(Ch.EDU, 5),
    advancement=(Ch.INT, 8),
    re_enlistment=6,
    ranks={0: 'Carousing',
           3: 'Advocate'},
    skill_and_training=[{1: Ch.DEX, 2: Ch.INT, 3: Ch.EDU, 4: Ch.SOC, 5: 'Carousing', 6: "Melee Combat"},
                        {1: 'Athletics', 2: 'Admin', 3: 'Carousing', 4: 'Leadership', 5: 'Gambling', 6: 'Vehicle'},
                        {1: 'Computer', 2: 'Carousing', 3: 'Gun Combat', 4: 'Melee Combat', 5: 'Liaison', 6: 'Liaison'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Liaison', 4: 'Liaison', 5: 'Liaison', 6: 'Sciences'}],
    material_benefits={1: 3, 2: Ch.EDU, 3: Ch.INT, 4: 3, 5: 'Society', 6: 3, 7: -1},
    cash={1: 2000, 2: 10000, 3: 20000, 4: 20000, 5: 50000, 6: 100000, 7: 100000}
)

physician = Career(
    name='Physician',
    qualification=(Ch.EDU, 6),
    survival=(Ch.INT, 4),
    commission=(Ch.INT, 5),
    advancement=(Ch.EDU, 8),
    re_enlistment=5,
    ranks={0: 'Medicine',
           3: 'Admin'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: Ch.INT, 5: Ch.EDU, 6: "Gun Combat"},
                        {1: 'Admin', 2: 'Computer', 3: 'Mechanics', 4: 'Medicine', 5: 'Leadership', 6: 'Sciences'},
                        {1: 'Computer', 2: 'Carousing', 3: 'Electronics', 4: 'Medicine', 5: 'Medicine', 6: 'Sciences'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Jack-of-All-Trades', 4: 'Linguistics', 5: 'Medicine', 6: 'Sciences'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: Ch.INT, 4: 3, 5: 'Society', 6: 3, 7: Ch.SOC},
    cash={1: 2000, 2: 10000, 3: 20000, 4: 20000, 5: 50000, 6: 100000, 7: 100000}
)


pirate = Career(
    name='Pirate',
    qualification=(Ch.DEX, 5),
    survival=(Ch.DEX, 6),
    commission=(Ch.STR, 5),
    advancement=(Ch.INT, 6),
    re_enlistment=5,
    ranks={0: 'Gunnery',
           3: 'Pilot'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Melee Combat', 5: 'Bribery', 6: "Gambling"},
                        {1: 'Streetwise', 2: 'Electronics', 3: 'Gun Combat', 4: 'Melee Combat', 5: 'Recon', 6: 'Vehicle'},
                        {1: 'Zero-G', 2: 'Zero-G', 3: 'Engineering', 4: 'Gunnery', 5: 'Navigation', 6: 'Navigation'},
                        {1: 'Computer', 2: 'Gravitics', 3: 'Jack-of-All-Trades', 4: 'Medicine', 5: 'Advocate', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'Weapon', 4: 2, 5: Ch.SOC, 6: 3, 7: Ch.SOC},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 20000, 5: 20000, 6: 50000, 7: 100000}
)

rogue = Career(
    name='Rogue',
    qualification=(Ch.DEX, 5),
    survival=(Ch.DEX, 4),
    commission=(Ch.STR, 6),
    advancement=(Ch.INT, 7),
    re_enlistment=4,
    ranks={0: 'Streetwise',
           3: 'Gun Combat'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Melee Combat', 5: 'Bribery', 6: "Gambling"},
                        {1: 'Streetwise', 2: 'Electronics', 3: 'Gun Combat', 4: 'Melee Combat', 5: 'Recon', 6: 'Vehicle'},
                        {1: 'Zero-G', 2: 'Zero-G', 3: 'Engineering', 4: 'Gunnery', 5: 'Navigation', 6: 'Navigation'},
                        {1: 'Computer', 2: 'Gravitics', 3: 'Jack-of-All-Trades', 4: 'Medicine', 5: 'Advocate', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.INT, 3: 'Weapon', 4: 2, 5: 'Weapon', 6: 3, 7: Ch.SOC},
    cash={1: 1000, 2: 5000, 3: 5000, 4: 5000, 5: 10000, 6: 20000, 7: 50000}
)

scientist = Career(
    name='Scientist',
    qualification=(Ch.EDU, 6),
    survival=(Ch.EDU, 5),
    commission=(Ch.INT, 7),
    advancement=(Ch.INT, 6),
    re_enlistment=5,
    ranks={0: 'Sciences',
           3: 'Computer'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: Ch.INT, 5: Ch.EDU, 6: "Gun Combat"},
                        {1: 'Admin', 2: 'Computer', 3: 'Electronics', 4: 'Electronics', 5: 'Bribery', 6: 'Sciences'},
                        {1: 'Sciences', 2: 'Admin', 3: 'Sciences', 4: 'Sciences', 5: 'Animals', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Jack-of-All-Trades', 4: 'Linguistics', 5: 'Medicine', 6: 'Sciences'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: Ch.INT, 4: 2, 5: Ch.SOC, 6: 3, 7: 5},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000}
)

scout = Career(
    name='Scout',
    qualification=(Ch.INT, 6),
    survival=(Ch.EDU, 7),
    commission=None,
    advancement=None,
    re_enlistment=6,
    ranks={0: 'Pilot'},
    skill_and_training=[{1: Ch.STR, 2: Ch.DEX, 3: Ch.END, 4: 'Jack-of-All-Trades', 5: Ch.EDU, 6: "Melee Combat"},
                        {1: 'Comms', 2: 'Electronics', 3: 'Gun Combat', 4: 'Gunnery', 5: 'Recon', 6: 'Piloting'},
                        {1: 'Engineering', 2: 'Gunnery', 3: 'Demolitions', 4: 'Navigation', 5: 'Medicine', 6: 'Vehicle'},
                        {1: 'Advocate', 2: 'Computer', 3: 'Linguistics', 4: 'Medicine', 5: 'Navigation', 6: 'Tactics'}],
    material_benefits={1: 1, 2: Ch.EDU, 3: 'Weapon', 4: 2, 5: 'Society', 6: 4},
    cash={1: 1000, 2: 5000, 3: 10000, 4: 10000, 5: 20000, 6: 50000, 7: 50000}
)

