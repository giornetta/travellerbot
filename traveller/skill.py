from __future__ import annotations

from typing import Dict

skills: Dict[str, bool] = {  # Name, is_passive
    "Battle Dress": True,
    "Jack-of-All-Trades": True,
    "Zero-G": True,
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


class Skill:
    name: str
    level: int

    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level

    def __str__(self) -> str:
        return f'{self.name}-{self.level}'
