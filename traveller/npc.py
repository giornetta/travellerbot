from dataclasses import dataclass

from traveller.career import Career
from traveller.equipment import Armor, Weapon

@dataclass
class Npc:
    STR: int = 2
    DEX: int = 2
    END: int = 2
    INT: int = 2
    EDU: int = 2
    SOC: int = 2
    career: Career = None
    rank: int = 0
    armor: Armor = None
    weapon: Weapon = None
    name: str = ""
    ally: bool = False
