from __future__ import annotations

from enum import Enum
from psycopg2.extensions import connection
from random import Random

from traveller.common import Characteristics
from traveller.equipment import Equipment, Armor, Weapon

from typing import Dict, List, cast, Tuple
from traveller.skill import Skill

# This represents the Sex of a Character.
# It will be used to determine appropriate noble/work titles.
from traveller.world import World


class Sex(Enum):
    M: str = 'M'
    F: str = 'F'


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
    stats: Dict[Characteristics, int]
    modifiers: Dict[Characteristics, int]

    # Homeworld
    homeworld: World

    # Possessions
    credits: int
    equipped_armor: Armor = None
    equipped_reflec: Armor = None
    drawn_weapon: Weapon = None
    inventory: List[Tuple[Equipment, int]]

    # Statuses
    stance: Stance = 2
    rads: int = 0
    is_fatigued: bool = False
    stims_taken: int = 0

    # Skills
    skills: List[Skill]

    # Skills
    skills: List[str]  # TODO Turn into List[Skill] and add functionalities

    def equip_armor(self, armor_name: str):
        for item, qt in self.inventory:
            if item.name is armor_name and item.__class__ is Armor:
                self.equipped_armor = cast(Armor, item)

    def write(self, user_id, adventure_id, db: connection):
        with db:
            with db.cursor() as cur:
                cur.execute('INSERT INTO characters '
                            'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                            'ON CONFLICT DO NOTHING;',
                            (self.name, self.sex.value, True, self.age, user_id, adventure_id,
                             self.stats[Characteristics.STR],
                             self.stats[Characteristics.DEX],
                             self.stats[Characteristics.END],
                             self.stats[Characteristics.INT],
                             self.stats[Characteristics.EDU],
                             self.stats[Characteristics.SOC],
                             self.modifiers[Characteristics.STR],
                             self.modifiers[Characteristics.DEX],
                             self.modifiers[Characteristics.END],
                             self.modifiers[Characteristics.INT],
                             self.modifiers[Characteristics.EDU],
                             self.modifiers[Characteristics.SOC],
                             self.credits, None, None, None, self.stance, self.rads,
                             self.is_fatigued, self.stims_taken
                             ))
                cur.execute('SELECT id FROM characters WHERE alive=TRUE AND user_id = %s AND adventure_id = %s;',
                            (user_id, adventure_id))
                char_id = cur.fetchone()[0]
                for eq, qt in self.inventory:
                    cur.execute('INSERT INTO inventories VALUES(%s, %s, %s, 0);', (char_id, eq.id, qt))
                for skill in self.skills:
                    cur.execute('INSERT INTO skill_sets VALUES(%s, %s, %s);', (char_id, skill.name, skill.level))

    def roll_stats(self):
        for c in Characteristics:
            v = Random().randint(1, 6) + Random().randint(1, 6)
            self.stats[c] = v
            self.modifiers[c] = v // 3 - 2

    @property
    def stats_tuple(self) -> Tuple[int, int, int, int, int, int]:
        return (
            self.stats[Characteristics.STR],
            self.stats[Characteristics.END],
            self.stats[Characteristics.DEX],
            self.stats[Characteristics.INT],
            self.stats[Characteristics.EDU],
            self.stats[Characteristics.SOC]
        )
