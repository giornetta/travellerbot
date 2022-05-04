from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

skills: Dict[str, bool] = {  # Name, is_passive
    "Battle Dress": True,
    "Jack-of-All-Trades": True,
    "Zero-G": True,
    "Archery": True,
    "Energy Pistol": True,
    "Energy Rifle": True,
    "Shotgun": True,
    "Slug Pistol": True,
    "Slug Rifle": True,
    "Bludgeoning Weapons": True,
    "Natural Weapons": True,
    "Piercing Weapons": True,
    "Slashing Weapons": True,
    "Gun Combat": True,
    "Melee Combat": True,
    "Vehicle": False,
    "Admin": False,
    "Advocate": False,
    "Animals": False,
    "Athletics": False,
    "Broker": False,
    "Carousing": False,
    "Comms": False,
    "Computer": False,
    "Demolition": False,
    "Electronics": False,
    "Engineering": False,
    "Gambling": False,
    "Gravitics": False,
    "Linguistic": False,
    "Liason": False,
    "Mechanics": False,
    "Medicine": False,
    "Navigation": False,
    "Piloting": False,
    "Recon": False,
    "Sciences": False,
    "Steward": False,
    "Streetwise": False,
    "Tactics": False,
    "Bribery": False,
    "Leadership": False
}

education_skills = [
    'Admin', 'Advocate', 'Animals', 'Carousing', 'Comms', 'Computer', 'Electronics', 'Engineering',
    'Life Sciences', 'Linguistics', 'Mechanics', 'Medicine', 'Physical Sciences', 'Social Sciences', 'Space Sciences'
]


@dataclass
class Skill:
    name: str
    level: int
