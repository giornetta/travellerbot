import json
import os
import random
from random import Random
from typing import List, Dict, Tuple, Optional

from traveller.world import World, Attribute, AttrFilter

BASE_URI: str = 'https://travellermap.com/api/'

# Each sector has a list of worlds attached to it
data: Dict[str, List[World]] = {}


def load_map(path: str):
    if os.path.isfile(path):
        with open(path) as f:
            d: Dict[str, List[Tuple[str, str]]] = json.load(f)

            for sec in d:
                data[sec] = []
                for w in d[sec]:
                    data[sec].append(World(w[0], w[1], '0000'))


def random_sector() -> str:
    return random.choice(list(data))


def sectors() -> List[str]:
    return list(data.keys())


def world_names(sector: str) -> List[str]:
    return [w.name for w in data[sector]]


def random_world(sector: str) -> World:
    index = Random().randint(0, len(data[sector]) - 1)
    return data[sector][index]


def world(sector: str, world_name: str) -> Optional[World]:
    worlds = data.get(sector)
    if worlds:
        for w in worlds:
            if w.name == world_name:
                return w

    return None


def world_filter(sector: str, filters: Dict[Attribute, AttrFilter]) -> List[str]:
    worlds = []
    for w in data[sector]:
        skip: bool = False

        for attr in Attribute:
            if w.attr[attr] < filters[attr].min or w.attr[attr] > filters[attr].max:
                skip = True
                break

        if not skip:
            worlds.append(w.name)

    return worlds
