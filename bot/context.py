from typing import Optional, Dict

from telegram import Update
from telegram.ext import CallbackContext, Dispatcher
from telegram.ext.utils.types import UD

from traveller.adventure import Adventure
from traveller.character import Character
from traveller.world import Attribute, AttrFilter


class UserData:
    active_adventure_id: Optional[str]
    adventure: Optional[Adventure]

    character: Optional[Character]
    homeworld_filters: Dict[Attribute, AttrFilter]
    initial_skills_left: int

    def __init__(self):
        self.active_adventure_id = None
        self.character = None
        self.adventure = None

    def new_adventure(self):
        self.adventure = Adventure()

    def new_character(self):
        self.character = Character()

    def new_filters(self):
        self.homeworld_filters = {}


class Context(CallbackContext[UserData, dict, dict]):
    def __init__(self, dispatcher: Dispatcher):
        super().__init__(dispatcher=dispatcher)
