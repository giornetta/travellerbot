from enum import Enum, auto
from typing import List


class TradeCode(Enum):
    AGRICULTURAL = auto()
    ASTEROID = auto()
    BARREN = auto()
    DESERT = auto()
    FLUID_OCEANS = auto()
    GARDEN = auto()
    HIGH_POPULATION = auto()
    HIGH_TECHNOLOGY = auto()
    ICE_CAPPED = auto()
    INDUSTRIAL = auto()
    LOW_POPULATION = auto()
    LOW_TECHNOLOGY = auto()
    NON_AGRICULTURAL = auto()
    NON_INDUSTRIAL = auto()
    POOR = auto()
    RICH = auto()
    WATER_WORLD = auto()
    VACUUM = auto()


def trade_codes(uwp: str) -> List[TradeCode]:
    codes: List[TradeCode] = []

    v = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
         '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

    if 4 <= v[uwp[2]] <= 9 and 4 <= v[uwp[3]] <= 8 and 5 <= v[uwp[4]] <= 7:
        codes.append(TradeCode.AGRICULTURAL)
    elif 0 <= v[uwp[2]] <= 3 and 0 <= v[uwp[3]] <= 3 and v[uwp[4]] >= 6:
        codes.append(TradeCode.NON_AGRICULTURAL)

    if v[uwp[1]] == 0 and v[uwp[2]] == 0 and v[uwp[3]] == 0:
        codes.append(TradeCode.ASTEROID)

    if v[uwp[4]] == 0 and v[uwp[5]] == 0 and v[uwp[6]] == 0:
        codes.append(TradeCode.BARREN)

    if v[uwp[2]] >= 2 and v[uwp[3]] == 0:
        codes.append(TradeCode.DESERT)

    if v[uwp[2]] >= 10 and v[uwp[3]] >= 1:
        codes.append(TradeCode.FLUID_OCEANS)

    if v[uwp[2]] in [5, 6, 8] and 4 <= v[uwp[3]] <= 9 and 4 <= v[uwp[4]] <= 8:
        codes.append(TradeCode.GARDEN)

    if v[uwp[4]] >= 9:
        codes.append(TradeCode.HIGH_POPULATION)
    elif 1 <= v[uwp[4]] <= 3:
        codes.append(TradeCode.LOW_POPULATION)

    if v[uwp[8]] >= 12:
        codes.append(TradeCode.HIGH_TECHNOLOGY)
    elif v[uwp[8]] <= 5:
        codes.append(TradeCode.LOW_TECHNOLOGY)

    if 0 <= v[uwp[2]] <= 1 and v[uwp[3]] >= 1:
        codes.append(TradeCode.ICE_CAPPED)

    if v[uwp[2]] in [0, 1, 2, 4, 7, 9] and v[uwp[4]] >= 9:
        codes.append(TradeCode.INDUSTRIAL)
    elif 4 <= v[uwp[4]] <= 6:
        codes.append(TradeCode.NON_INDUSTRIAL)

    if 2 <= v[uwp[2]] <= 5 and 0 <= v[uwp[3]] <= 3:
        codes.append(TradeCode.POOR)
    elif v[uwp[2]] in [6, 8] and 6 <= v[uwp[4]] <= 8:
        codes.append(TradeCode.RICH)

    if v[uwp[3]] == 10:
        codes.append(TradeCode.WATER_WORLD)

    if v[uwp[2]] == 0:
        codes.append(TradeCode.VACUUM)

    return codes


def homeworld_skills(law_level: int, codes: List[TradeCode]) -> List[str]:
    skills: List[str] = []

    if 0 <= law_level <= 6:
        skills.append('Gun Combat-0')
    elif 7 <= law_level <= 9:
        skills.append('Melee Combat-0')

    tc_skills = {
        TradeCode.AGRICULTURAL: 'Animals-0',
        TradeCode.ASTEROID: 'Zero-G-0',
        TradeCode.DESERT: 'Survival-0',
        TradeCode.FLUID_OCEANS: 'Vehicle-0',
        TradeCode.GARDEN: 'Animals-0',
        TradeCode.HIGH_TECHNOLOGY: 'Streetwise-0',
        TradeCode.ICE_CAPPED: 'Zero-G-0',
        TradeCode.INDUSTRIAL: 'Broker-0',
        TradeCode.LOW_TECHNOLOGY: 'Survival-0',
        TradeCode.POOR: 'Animals-0',
        TradeCode.RICH: 'Carousing-0',
        TradeCode.WATER_WORLD: 'Vehicle-0',
        TradeCode.VACUUM: 'Zero-G-0'
    }

    for c in TradeCode:
        if c in codes:
            if tc_skills.get(c):
                skills.append(tc_skills[c])

    return skills






