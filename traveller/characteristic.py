from __future__ import annotations

from enum import Enum


# This represents the available Characteristics for any character.
from typing import List


class Characteristic(Enum):
    STR = 'Strength'
    DEX = 'Dexterity'
    END = 'Endurance'
    INT = 'Intelligence'
    EDU = 'Education'
    SOC = 'Social Standing'

    @classmethod
    def physical(cls) -> List[Characteristic]:
        return [Characteristic.STR, Characteristic.DEX, Characteristic.END]

    @classmethod
    def mental(cls) -> List[Characteristic]:
        return [Characteristic.INT, Characteristic.EDU, Characteristic.SOC]
