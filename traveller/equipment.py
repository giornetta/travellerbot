from __future__ import annotations

from traveller.common import Characteristics
from traveller.skill import Skill
from traveller.damage import DamageType, Damage

from typing import Dict, List


class Equipment:
    name: str
    cost: int
    weight: int
    technology_level: int
    broken: bool
    consumable: bool


class Armor(Equipment):
    standard_rating: int
    laser_rating: int
    
    bonus_stats: Dict[Characteristics, int]
    built_in_computer: Computer

    required_skill: Skill

    protect: List[DamageType]
    rads_protection: int

    def after_hit(self, dmg: Damage):
        if self.name == 'Ablat' and dmg.type == DamageType.Laser:
            self.laser_rating = self.laser_rating - 1 if self.laser_rating > 0 else 0


class Communicator(Equipment):
    range: int


class Computer(Equipment):
    rating: int


class Software(Equipment):
    rating: int
    DM: int


class Drug(Equipment):
    rads_absorbed: int
    initiative_bonus: int
    dodge_bonus: int
    damage_reduction: int
    final_damage: bool
    required_skill: Skill


class Explosive(Equipment):
    dmg_count: int
    dmg_mult: int
    radius: int
    

class Weapon(Equipment):
    pass
