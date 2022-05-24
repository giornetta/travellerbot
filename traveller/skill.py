from __future__ import annotations

from typing import Dict, Tuple

from traveller import dice

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
    "Linguistics": False,
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


difficulty_modifiers: Dict[str, int] = {
    'Simple': +6,
    'Easy': +4,
    'Routine': +2,
    'Average': 0,
    'Difficult': -2,
    'Very Difficult': -4,
    'Formidable': -6
}


def check(skill: str, difficulty: str) -> Tuple[int, str]:
    '''
    < -6 Exceptional Failure
-1 < -5 Failure
0 < 5 Success
6 > Exceptional Success
    '''

    result = dice.roll(2)
    if result == 2:
        return result, 'Failure!'
    if result == 12:
        return result, 'Success!'

    try:
        level = int(skill.split('-')[-1])
    except ValueError:
        level = -3

    result += level + difficulty_modifiers[difficulty]
    msg: str

    effect = result - 8
    if effect <= -6:
        msg = 'Exceptional Failure!'
    elif -5 <= effect <= -1:
        msg = 'Failure!'
    elif 0 <= effect <= 5:
        msg = 'Success!'
    else:
        msg = 'Exceptional Success!'

    return result, msg


class Skill:
    name: str
    level: int

    def __init__(self, name: str, level: int):
        self.name = name
        self.level = level

    def __str__(self) -> str:
        return f'{self.name}-{self.level}'
