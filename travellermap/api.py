import json
import os
import random
from random import Random
from typing import List, Dict, Tuple


class TravellerMap:
    BASE_URI: str = 'https://travellermap.com/api/'

    # Each sector has a list of worlds attached to it.
    # Every world is represented as a tuple (name, uwp)
    data: Dict[str, List[Tuple[str, str]]]

    def __init__(self, path: str):
        self._path = path
        if os.path.isfile(path):
            with open(path) as f:
                self.data = json.load(f)

    def random_sector(self) -> str:
        return random.choice(list(self.data))

    @property
    def sectors(self) -> List[str]:
        return list(self.data.keys())

    def worlds(self, sector: str) -> List[str]:
        return [w[0] for w in self.data[sector]]

    def random_world(self, sector: str) -> str:
        index = Random().randint(0, len(self.data[sector]) - 1)
        return self.data[sector][index][0]