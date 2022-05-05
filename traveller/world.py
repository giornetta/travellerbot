from enum import Enum, auto
from typing import List, Dict, NamedTuple


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


class AttrVal(NamedTuple):
    full_name: str
    max: int


class Attribute(AttrVal, Enum):
    STARPORT = AttrVal('Starport', 5)
    SIZE = AttrVal('Size', 10)
    ATM = AttrVal('Atmosphere', 15)
    HYDRO = AttrVal('Hydrographics', 10)
    POP = AttrVal('Population', 10)
    GOV = AttrVal('Government', 15)
    LAW = AttrVal('Law', 10)
    TECH = AttrVal('Tech', 15)


class AttrFilter:
    min: int
    max: int

    def __init__(self, attr: Attribute):
        self.min = 0
        self.max = attr.max


starport_values = {'X': 0, 'E': 1, 'D': 2, 'C': 3, 'B': 4, 'A': 5}


class World:
    name: str
    attr: Dict[Attribute, int]
    hex: str

    def __init__(self, name: str, uwp: str, hex: str):
        self.name = name
        self.hex = hex
        self.attr = {Attribute.STARPORT: starport_values[uwp[0]]}

        v = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
             '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}

        self.attr[Attribute.SIZE] = v[uwp[1]]
        self.attr[Attribute.ATM] = v[uwp[2]]
        self.attr[Attribute.HYDRO] = v[uwp[3]]
        self.attr[Attribute.POP] = v[uwp[4]]
        self.attr[Attribute.GOV] = v[uwp[5]]
        self.attr[Attribute.LAW] = v[uwp[6]]
        self.attr[Attribute.TECH] = v[uwp[8]]

    @property
    def trade_codes(self) -> List[TradeCode]:
        codes: List[TradeCode] = []

        if 4 <= self.attr[Attribute.ATM] <= 9 and 4 <= self.attr[Attribute.HYDRO] <= 8 and 5 <= self.attr[Attribute.POP] <= 7:
            codes.append(TradeCode.AGRICULTURAL)
        elif 0 <= self.attr[Attribute.ATM] <= 3 and 0 <= self.attr[Attribute.HYDRO] <= 3 and self.attr[Attribute.POP] >= 6:
            codes.append(TradeCode.NON_AGRICULTURAL)

        if self.attr[Attribute.SIZE] == 0 and self.attr[Attribute.ATM] == 0 and self.attr[Attribute.HYDRO] == 0:
            codes.append(TradeCode.ASTEROID)

        if self.attr[Attribute.POP] == 0 and self.attr[Attribute.GOV] == 0 and self.attr[Attribute.LAW] == 0:
            codes.append(TradeCode.BARREN)

        if self.attr[Attribute.ATM] >= 2 and self.attr[Attribute.HYDRO] == 0:
            codes.append(TradeCode.DESERT)

        if self.attr[Attribute.ATM] >= 10 and self.attr[Attribute.HYDRO] >= 1:
            codes.append(TradeCode.FLUID_OCEANS)

        if self.attr[Attribute.ATM] in [5, 6, 8] and 4 <= self.attr[Attribute.HYDRO] <= 9 and 4 <= self.attr[Attribute.POP] <= 8:
            codes.append(TradeCode.GARDEN)

        if self.attr[Attribute.POP] >= 9:
            codes.append(TradeCode.HIGH_POPULATION)
        elif 1 <= self.attr[Attribute.POP] <= 3:
            codes.append(TradeCode.LOW_POPULATION)

        if self.attr[Attribute.TECH] >= 12:
            codes.append(TradeCode.HIGH_TECHNOLOGY)
        elif self.attr[Attribute.TECH] <= 5:
            codes.append(TradeCode.LOW_TECHNOLOGY)

        if 0 <= self.attr[Attribute.ATM] <= 1 and self.attr[Attribute.HYDRO] >= 1:
            codes.append(TradeCode.ICE_CAPPED)

        if self.attr[Attribute.ATM] in [0, 1, 2, 4, 7, 9] and self.attr[Attribute.POP] >= 9:
            codes.append(TradeCode.INDUSTRIAL)
        elif 4 <= self.attr[Attribute.POP] <= 6:
            codes.append(TradeCode.NON_INDUSTRIAL)

        if 2 <= self.attr[Attribute.ATM] <= 5 and 0 <= self.attr[Attribute.HYDRO] <= 3:
            codes.append(TradeCode.POOR)
        elif self.attr[Attribute.ATM] in [6, 8] and 6 <= self.attr[Attribute.HYDRO] <= 8:
            codes.append(TradeCode.RICH)

        if self.attr[Attribute.HYDRO] == 10:
            codes.append(TradeCode.WATER_WORLD)

        if self.attr[Attribute.ATM] == 0:
            codes.append(TradeCode.VACUUM)

        return codes

    @property
    def homeworld_skills(self) -> List[str]:
        skills: List[str] = []

        if 0 <= self.attr[Attribute.LAW] <= 6:
            skills.append('Gun Combat')
        elif 7 <= self.attr[Attribute.LAW] <= 9:
            skills.append('Melee Combat')

        tc_skills = {
            TradeCode.AGRICULTURAL: 'Animals',
            TradeCode.ASTEROID: 'Zero-G',
            TradeCode.DESERT: 'Survival',
            TradeCode.FLUID_OCEANS: 'Vehicle',
            TradeCode.GARDEN: 'Animals',
            TradeCode.HIGH_TECHNOLOGY: 'Streetwise',
            TradeCode.ICE_CAPPED: 'Zero-G',
            TradeCode.INDUSTRIAL: 'Broker',
            TradeCode.LOW_TECHNOLOGY: 'Survival',
            TradeCode.POOR: 'Animals',
            TradeCode.RICH: 'Carousing',
            TradeCode.WATER_WORLD: 'Vehicle',
            TradeCode.VACUUM: 'Zero-G'
        }

        for c in self.trade_codes:
            s = tc_skills.get(c)
            if s and s not in skills:
                skills.append(s)

        return skills






