from __future__ import annotations

from enum import Enum


class DamageType(Enum):
    Normal: int
    Acid: int
    Fall: int 
    Disease: int
    Cold: int
    Hot: int
    Fire: int
    Poison: int
    Radiation: int
    Starvation: int
    Dehydration: int
    Suffocation: int
    Vacuum: int
    Laser: int


class Damage:
    type: DamageType
    amount: int
