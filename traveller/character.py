from __future__ import annotations

from enum import Enum
from random import Random

from traveller.characteristic import Characteristic
from traveller.equipment import Equipment, Armor, Weapon

from typing import Dict, List, cast
from traveller.world import World


# This represents the Sex of a Character.
# It will be used to determine appropriate noble/work titles.
class Sex(Enum):
    M: str = 'Male'
    F: str = 'Female'


# This represents the current Stance of a Character,
# and will be mainly used during combat to determine damage or movement modifiers.
class Stance(Enum):
    Prone: int = 0
    Crouched: int = 1
    Standing: int = 2


class NobleTitle(Enum):
    Lord: Dict[Sex, int] = {}


class Character:
    # Anagraphic Information
    name: str
    age: int
    sex: Sex

    # Statistics
    stats: Dict[Characteristics, int] = {}
    modifiers: Dict[Characteristics, int] = {}

    # Homeworld
    homeworld: World
    
    # Possessions
    credits: int
    equipped_armor: Armor
    equipped_reflec: Armor
    drawn_weapon: Weapon
    inventory: List[Equipment]

    # Statuses
    stance: Stance
    rads: int
    is_fatigued: bool
    stims_taken: int

    # Skills
    skills: List[str] = []  # TODO Turn into List[Skill] and add functionalities

    def equip_armor(self, armor_name: str):
        for item in self.inventory:
            if item.name is armor_name and isinstance(item, Armor):
                self.equipped_armor = cast(Armor, item)

    def roll_stats(self):
        for c in Characteristic:
            v = Random().randint(1, 6) + Random().randint(1, 6)
            self.stats[c] = v
            self.modifiers[c] = v // 3 - 2
