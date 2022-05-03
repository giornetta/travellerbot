from __future__ import annotations

from enum import Enum
from random import Random

from traveller.characteristic import Characteristic
from traveller.world import World

from psycopg2.extensions import connection

from traveller.equipment import Equipment, Armor, Weapon

from typing import Dict, List, cast, Tuple
from traveller.skill import Skill, skills


# This represents the Sex of a Character.
# It will be used to determine appropriate noble/work titles.
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
    stats: Dict[Characteristic, int] = {}
    modifiers: Dict[Characteristic, int] = {}

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
    skills: List[Skill] = []

    def equip_armor(self, armor_name: str):
        for item, qt in self.inventory:
            if item.name is armor_name and isinstance(item, Armor):
                self.equipped_armor = cast(Armor, item)

    def roll_stats(self):
        for c in Characteristic:
            v = Random().randint(1, 6) + Random().randint(1, 6)
            self.stats[c] = v
            self.modifiers[c] = v // 3 - 2

    @property
    def skill_names(self):
        return [s.name for s in self.skills]

    def acquire_skill(self, skill_name: str):
        if skill_name in skills:
            try:
                i = [s.name for s in self.skills].index(skill_name)
                self.skills[i].level += 1
            except ValueError:
                self.skills.append(Skill(skill_name, 0))

    def write(self, user_id, adventure_id, db: connection):
        with db:
            with db.cursor() as cur:
                cur.execute('INSERT INTO characters '
                            'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                            'ON CONFLICT DO NOTHING;', (
                                self.name, self.sex.value, True, user_id, adventure_id,
                                self.stats[Characteristic.STR],
                                self.stats[Characteristic.DEX],
                                self.stats[Characteristic.END],
                                self.stats[Characteristic.INT],
                                self.stats[Characteristic.EDU],
                                self.stats[Characteristic.SOC],
                                self.modifiers[Characteristic.STR],
                                self.modifiers[Characteristic.DEX],
                                self.modifiers[Characteristic.END],
                                self.modifiers[Characteristic.INT],
                                self.modifiers[Characteristic.EDU],
                                self.modifiers[Characteristic.SOC],
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
