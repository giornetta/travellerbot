import json
import os
import random
from random import Random
from typing import List, Dict, Tuple


BASE_URI: str = 'https://travellermap.com/api/'

# Each sector has a list of worlds attached to it.
# Every world is represented as a tuple (name, uwp)
data: Dict[str, List[Tuple[str, str]]] = {}


def load_map(path: str):
    if os.path.isfile(path):
        with open(path) as f:
            data.update(json.load(f))


def random_sector() -> str:
    return random.choice(list(data))


def sectors() -> List[str]:
    return list(data.keys())


def worlds(sector: str) -> List[str]:
    return [w[0] for w in data[sector]]


def random_world(sector: str) -> str:
    index = Random().randint(0, len(data[sector]) - 1)
    return data[sector][index][0]
