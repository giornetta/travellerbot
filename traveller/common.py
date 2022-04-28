from __future__ import annotations

from enum import Enum


# This represents the available Characteristics for any character.
class Characteristics(Enum):
    STR = 'Strength'
    DEX = 'Dexterity'
    END = 'Endurance'
    INT = 'Intelligence'
    EDU = 'Education'
    SOC = 'Social Standing'
