from __future__ import annotations

from enum import Enum
from traveller.common import Characteristics
from traveller.equipment import Equipment, Armor, Weapon

from typing import Dict, List


# This represent the Sex of a Character.
# It will be used to determine appropriate noble/work titles.
class Sex(Enum):
    M: str = 'Male'
    F: str = 'Female'


# This represents the current Stance of a Character, and will be mainly used during combat to determine damage or movement modifiers.
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
    stats: Dict[Characteristics, int]
    modifiers: Dict[Characteristics, int]
    
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

    def equip_armor(self, armor_name: str):
        for item in self.inventory:
            if item.name is armor_name and item.__class__ is Armor:
                self.equipped_armor = item


