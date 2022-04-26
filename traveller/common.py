from __future__ import annotations

from enum import Enum


# This represents the available Characteristics for any character.
class Characteristics(Enum):
    STR: str = 'Strength'
    DEX: str = 'Dexterity'
    END: str = 'Endurance'
    INT: str = 'Intelligence'
    EDU: str = 'Education'
    SOC: str = 'Social Standing'
