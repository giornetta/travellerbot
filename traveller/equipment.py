from __future__ import annotations

import json
from typing import Dict, Optional, Tuple, List

from traveller.skill import Skill

equipments: Dict[int, Equipment] = {}

ranges_description: Dict[int, str] = {
    0: "assault weapon",
    1: "rifle",
    2: "pistol",
    3: "shotgun",
    4: "rifle",
    5: "rocket",
    6: "melee (close quarters)",
    7: "melee (extended reach)",
    8: "ranged (thrown)"
}


def load_equipment(path: str):
    if len(equipments) == 0:
        with open(path) as f:
            eq = json.load(f)
        for eq_type in eq:
            for equip in eq[eq_type]:
                if eq_type == "Armor":
                    equipments[equip['id']] = Armor(equip)
                elif eq_type == "Communicator":
                    equipments[equip['id']] = Communicator(equip)
                elif eq_type == "Computers":
                    equipments[equip['id']] = Computer(equip)
                elif eq_type == "Computer Software":
                    equipments[equip['id']] = Software(equip)
                elif eq_type == "Drugs":
                    equipments[equip['id']] = Drug(equip)
                elif eq_type == "Explosives":
                    equipments[equip['id']] = Explosive(equip)
                elif eq_type == "Personal Devices":
                    equipments[equip['id']] = PersonalDevice(equip)
                elif eq_type == "Sensory Aids":
                    equipments[equip['id']] = SensoryAid(equip)
                elif eq_type == "Shelters":
                    equipments[equip['id']] = Shelter(equip)
                elif eq_type == "Survival Equipment":
                    equipments[equip['id']] = SurvivalEquipment(equip)
                elif eq_type == "Tools":
                    equipments[equip['id']] = Tool(equip)
                elif eq_type == "Melee Weapons":
                    equipments[equip['id']] = MeleeWeapon(equip)
                elif eq_type == "Ranged Weapons":
                    equipments[equip['id']] = RangedWeapon(equip)
                elif eq_type == "Ranged Ammunition":
                    equipments[equip['id']] = RangedAmmunition(equip)
                elif eq_type == "Weapon Accessories":
                    equipments[equip['id']] = WeaponAccessory(equip)
                elif eq_type == "Grenades":
                    equipments[equip['id']] = Grenade(equip)
                elif eq_type == "Heavy Weapons":
                    equipments[equip['id']] = HeavyWeapon(equip)
                elif eq_type == "Heavy Weapon Ammunition":
                    equipments[equip['id']] = HeavyWeaponAmmunition(equip)
                else:
                    equipments[equip['id']] = Equipment(equip)


class Equipment:
    id: int
    name: str
    cost: int
    technology_level: int

    def __init__(self, data: Dict):
        self.id = data["id"]
        self.name = data['name']
        self.cost = data['cost']
        self.technology_level = data['TL']


class Armor(Equipment):
    armor_rating: int
    weight: float
    laser_rating: Optional[int]
    is_AR_damageable: Optional[bool]
    required_skill: Optional[Skill]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.armor_rating = data['AR']
        self.weight = data['weight']
        self.laser_rating = data.get('AR_laser')
        self.is_AR_damageable = data.get('is_AR_damageable')
        self.required_skill = data.get('skill_required')


class Communicator(Equipment):
    weight: float
    range: int
    is_personal_communicator: Optional[bool]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data['weight']
        self.range = data['range']
        self.is_personal_communicator = data.get('is_personal_communicator')


class Computer(Equipment):
    weight: float
    rating: int
    is_terminal: Optional[bool]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data['weight']
        self.rating = data['computer_power']
        self.is_terminal = data.get('is_terminal')


class Software(Equipment):
    rating: int
    is_database: Optional[bool]
    price_range: Tuple[Optional[int], Optional[int]]
    is_interface: Optional[bool]
    is_security: Optional[bool]
    is_translator: Optional[bool]
    is_intrusion: Optional[bool]
    is_intelligent_interface: Optional[bool]
    is_expert: Optional[bool]
    is_agent: Optional[bool]
    is_intellect: Optional[bool]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.rating = data['rating']
        self.is_database = data.get('is_database')
        self.price_range = (data.get('cost_min'), data.get('cost_max'))
        self.is_interface = data.get('is_interface')
        self.is_security = data.get('is_security')
        self.is_translator = data.get('is_translator')
        self.is_intrusion = data.get('is_intrusion')
        self.is_intelligent_interface = data.get('is_intelligent_interface')
        self.is_expert = data.get('is_expert')
        self.is_agent = data.get('is_agent')
        self.is_intellect = data.get('is_intellect')


class Drug(Equipment):
    def __init__(self, data: Dict):
        super().__init__(data)


class Explosive(Equipment):
    damage: int
    radius: int
    damage_multiplier: Optional[int]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.damage = data['damage']
        self.radius = data['radius']
        self.damage_multiplier = data.get('damage_multiplier')


class PersonalDevice(Equipment):
    weight: Optional[float]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data.get('weight')


class SensoryAid(Equipment):
    weight: Optional[float]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data.get('weight')


class Shelter(Equipment):
    weight: float

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data['weight']


class SurvivalEquipment(Equipment):
    weight: Optional[float]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data.get('weight')


class Tool(Equipment):
    weight: Optional[float]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data.get('weight')


class Weapon(Equipment):
    weight: float
    law_level: int
    damage: int

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data['weight']
        self.law_level = data['LL']
        self.damage = data['damage']


class MeleeWeapon(Weapon):
    types: List[str]
    range: List[int]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.types = data['type']
        self.range = data['range']


class RangedWeapon(Weapon):
    rate_of_fire: List[int]
    type: str
    recoil: bool
    range: int

    def __init__(self, data: Dict):
        super().__init__(data)
        self.rate_of_fire = data['RoF']
        self.type = data['type']
        self.recoil = data['recoil']
        self.range = data['range']


class RangedAmmunition(Equipment):
    weight: float
    rounds: List[int]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data['weight']
        self.rounds = data['rounds']


class WeaponAccessory(Equipment):
    weight: Optional[float]

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data.get('weight')


class Grenade(Equipment):
    weight: float
    damage: Optional[List[int]]
    law_level: int

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data['weight']
        self.damage = data.get('damage')
        self.law_level = data['LL']


class HeavyWeapon(Weapon):
    rate_of_fire: List[int]
    recoil: bool
    range: int

    def __init__(self, data: Dict):
        super().__init__(data)
        self.rate_of_fire = data['Rof']
        self.recoil = data['recoil']
        self.range = data['range']


class HeavyWeaponAmmunition(Equipment):
    weight: float
    rounds: int

    def __init__(self, data: Dict):
        super().__init__(data)
        self.weight = data['weight']
        self.rounds = data['rounds']
