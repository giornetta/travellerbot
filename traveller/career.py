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
