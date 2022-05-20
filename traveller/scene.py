from typing import Dict, List, Tuple

from traveller import dice
from traveller.characteristic import Characteristic


class NPC:
    stats: Dict[Characteristic, int]

    career: str
    rank: int

    armor: int
    weapon: int

    name: str
    ally: bool

    def __init__(self):
        self.stats = dict.fromkeys(Characteristic, 0)

    def roll_characteristics(self):
        for k in self.stats.keys():
            self.stats[k] = dice.roll(2)

    @property
    def stats_tuple(self) -> Tuple[int, int, int, int, int, int]:
        return (
            self.stats[Characteristic.STR],
            self.stats[Characteristic.END],
            self.stats[Characteristic.DEX],
            self.stats[Characteristic.INT],
            self.stats[Characteristic.EDU],
            self.stats[Characteristic.SOC]
        )


class Scene:
    name: str
    npcs: List[NPC]

    def __init__(self, name: str):
        self.name = name
        self.npcs = []

    def add_npc(self):
        self.npcs.append(NPC())

    @property
    def npc(self) -> NPC:
        return self.npcs[-1]


