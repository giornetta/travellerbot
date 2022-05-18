from dataclasses import dataclass


@dataclass
class Npc:
    STR: int = 2
    DEX: int = 2
    END: int = 2
    INT: int = 2
    EDU: int = 2
    SOC: int = 2
    career: str = ""
    rank: int = 0
    armor: int = 0
    weapon: int = 0
    name: str = ""
    ally: bool = False
