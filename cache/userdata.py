import os
import pickle
from typing import Dict

from traveller.adventure import Adventure
from traveller.character import Character
from traveller.world import Attribute, AttrFilter
from traveller.npc import Npc


class UserData:
    # Used for idle player
    item: str
    item_id: int

    # Used for adventure creation
    adventure: Adventure
    npc: Npc
    scene_name: str

    # Used for character creation
    character: Character
    filters: Dict[Attribute, AttrFilter]
    homeworld_skills_left: int
    education_skills_left: int

    def init_filters(self):
        self.filters: Dict[Attribute, AttrFilter] = {}
        for attr in Attribute:
            self.filters[attr] = AttrFilter(attr)


user_data: Dict[int, UserData] = {}


def load_data(path: str):
    if os.path.isfile(path):
        with open(path, 'rb') as f:
            user_data.update(pickle.load(f))


def write_data(path: str):
    with open(path, 'wb') as f:
        pickle.dump(user_data, f)
