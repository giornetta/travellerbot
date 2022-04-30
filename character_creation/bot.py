from collections import OrderedDict
from enum import Enum, auto
from typing import List, Callable

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, CallbackContext, Filters

from bot.context import Context
from character_creation import kb
from character_creation.service import CharacterCreator
from traveller.common import Characteristics
from traveller.world import Attribute, starport_values
from travellermap import api


class State(Enum):
    MIN_STARPORT = auto()
    MAX_STARPORT = auto()
    MIN_SIZE = auto()
    MAX_SIZE = auto()
    MIN_ATM = auto()
    MAX_ATM = auto()
    MIN_HYDRO = auto()
    MAX_HYDRO = auto()
    MIN_POP = auto()
    MAX_POP = auto()
    MIN_GOV = auto()
    MAX_GOV = auto()
    MIN_LAW = auto()
    MAX_LAW = auto()
    MIN_TECH = auto()
    MAX_TECH = auto()
    WORLD = auto()
    HOMEWORLD_SKILL = auto()


params = OrderedDict({
    'starport': ('Starport', 'A'),
    'size': ('Size', 10),
    'atm': ('Atmosphere', 15),
    'hydro': ('Hydrographics', 10),
    'pop': ('Population', 10),
    'gov': ('Government', 15),
    'law': ('Law Level', 10),
    'tech': ('Technology Level', 15)
})

filter_starport = Filters.regex('^(X|E|D|C|B|A|Ignore)$')
filter_10 = Filters.regex('^([0-9]|10|Ignore)$')
filter_15 = Filters.regex('^([0-9]|1[0-5]|Ignore)$')


class CharacterCreationConversation:
    service: CharacterCreator

    def __init__(self, service: CharacterCreator):
        self.service = service

    def handlers(self) -> List[ConversationHandler]:
        return [ConversationHandler(
            entry_points=[MessageHandler(filter_starport, self._handle_min_starport)],
            states={
                State.MIN_STARPORT: [MessageHandler(filter_starport, self._handle_min_starport)],
                State.MAX_STARPORT: [MessageHandler(filter_starport, self._handle_max_starport)],
                State.MIN_SIZE: [MessageHandler(filter_10, self._handle_min(Attribute.SIZE))],
                State.MAX_SIZE: [MessageHandler(filter_10, self._handle_max(Attribute.SIZE))],
                State.MIN_ATM: [MessageHandler(filter_15, self._handle_min(Attribute.ATM))],
                State.MAX_ATM: [MessageHandler(filter_15, self._handle_max(Attribute.ATM))],
                State.MIN_HYDRO: [MessageHandler(filter_10, self._handle_min(Attribute.HYDRO))],
                State.MAX_HYDRO: [MessageHandler(filter_10, self._handle_max(Attribute.HYDRO))],
                State.MIN_POP: [MessageHandler(filter_10, self._handle_min(Attribute.POP))],
                State.MAX_POP: [MessageHandler(filter_10, self._handle_max(Attribute.POP))],
                State.MIN_GOV: [MessageHandler(filter_15, self._handle_min(Attribute.GOV))],
                State.MAX_GOV: [MessageHandler(filter_15, self._handle_max(Attribute.GOV))],
                State.MIN_LAW: [MessageHandler(filter_10, self._handle_min(Attribute.LAW))],
                State.MAX_LAW: [MessageHandler(filter_10, self._handle_max(Attribute.LAW))],
                State.MIN_TECH: [MessageHandler(filter_15, self._handle_min_tech)],
                State.MAX_TECH: [MessageHandler(filter_15, self._handle_max_tech)],
                State.WORLD: [MessageHandler(Filters.text, self._handle_world)],
                State.HOMEWORLD_SKILL: [MessageHandler(Filters.text, self._handle_homeworld_skill)]
            },
            fallbacks=[]
        )]

    def _handle_min_starport(self, update: Update, context: Context) -> State:
        context.user_data.new_filters()

        if update.message.text == 'Ignore':
            context.user_data.homeworld_filters[Attribute.STARPORT].min = 0
            context.user_data.homeworld_filters[Attribute.STARPORT].max = Attribute.STARPORT.max

            kb.ask_min.reply_text(update, params=Attribute.SIZE.full_name, keys=num_keys(0, Attribute.SIZE.max))

            return State.MIN_SIZE

        context.user_data.homeworld_filters[Attribute.STARPORT].min = starport_values[update.message.text]

        vals = ['X', 'E', 'D', 'C', 'B', 'A', 'Ignore']
        kl = [vals[i] for i in range(vals.index(update.message.text), len(vals))]
        keys = [kl[i: i + 3] for i in range(0, len(kl), 3)]

        kb.ask_max.reply_text(update, params=Attribute.STARPORT.full_name, keys=keys)

        return State.MAX_STARPORT

    def _handle_max_starport(self, update: Update, context: Context) -> State:
        val = update.message.text
        vals = ['X', 'E', 'D', 'C', 'B', 'A', 'Ignore']

        if val == 'Ignore':
            context.user_data.homeworld_filters[Attribute.STARPORT].max = Attribute.STARPORT.max
        else:
            if starport_values[val] < context.user_data.homeworld_filters[Attribute.STARPORT].min:
                context.user_data.homeworld_filters[Attribute.STARPORT].max = context.user_data.homeworld_filters[Attribute.STARPORT].min
            else:
                context.user_data.homeworld_filters[Attribute.STARPORT].max = val

        kb.ask_min.reply_text(update, params=Attribute.SIZE.full_name, keys=num_keys(0, Attribute.SIZE.max))
        return State.MIN_SIZE

    def _handle_min(self, attr: Attribute) -> Callable[[Update, Context], State]:
        def min_cb(update: Update, context: Context) -> State:
            if update.message.text == 'Ignore':
                context.user_data.homeworld_filters[attr].min = 0
                context.user_data.homeworld_filters[attr].max = attr.max

                next_index = list(Attribute).index(attr) + 1
                next_attr: Attribute = list(Attribute)[next_index]

                kb.ask_min.reply_text(update, params=next_attr.full_name, keys=num_keys(0, next_attr.max))

                return State[f'MIN_{next_attr.name}']

            val = int(update.message.text)
            context.user_data.homeworld_filters[attr].min = val

            kb.ask_max.reply_text(update, params=attr.full_name, keys=num_keys(val, attr.max))

            return State[f'MAX_{attr.name}']

        return min_cb

    def _handle_max(self, attr: Attribute) -> Callable[[Update, Context], State]:
        def max_cb(update: Update, context: Context) -> State:
            if update.message.text == 'Ignore':
                context.user_data.homeworld_filters[attr].max = attr.max
            else:
                val = int(update.message.text)
                if val >= context.user_data.homeworld_filters[attr].min:
                    context.user_data.homeworld_filters[attr].max = val
                else:
                    context.user_data.homeworld_filters[attr].max = context.user_data.homeworld_filters[attr].min

            next_index = list(Attribute).index(attr) + 1
            next_attr: Attribute = list(Attribute)[next_index]

            kb.ask_min.reply_text(update, params=next_attr.full_name, keys=num_keys(0, next_attr.max))
            return State[f'MIN_{next_attr.name}']

        return max_cb

    def _handle_min_tech(self, update: Update, context: Context):
        if update.message.text == 'Ignore':
            context.user_data.homeworld_filters[Attribute.TECH].min = 0
            context.user_data.homeworld_filters[Attribute.TECH].max = Attribute.TECH.max

            return self._world_selection(update, context)

        val = int(update.message.text)
        context.user_data.homeworld_filters[Attribute.TECH].min = val
        kb.ask_max.reply_text(update, params=Attribute.TECH.full_name, keys=num_keys(val, Attribute.TECH.max))

        return State.MAX_TECH

    def _handle_max_tech(self, update: Update, context: Context) -> State:
        if update.message.text == 'Ignore':
            context.user_data.homeworld_filters[Attribute.TECH].max = Attribute.TECH.max
        else:
            val = int(update.message.text)
            if val >= context.user_data.homeworld_filters[Attribute.TECH].min:
                context.user_data.homeworld_filters[Attribute.TECH].max = val
            else:
                context.user_data.homeworld_filters[Attribute.TECH].max = context.user_data.homeworld_filters[Attribute.TECH].min

        return self._world_selection(update, context)

    def _world_selection(self, update: Update, context: Context):
        worlds = api.world_filter(context.user_data.adventure.sector, context.user_data.homeworld_filters)

        if len(worlds) == 0:
            kb.no_world_found.reply_text(update)
            kb.ask_min.reply_text(update, params=Attribute.STARPORT.full_name, keys=[['X', 'E', 'D'], ['C', 'B', 'A'], ['Ignore']])
            return State.MIN_STARPORT

        kb.choose_world.reply_text(update, params=context.user_data.adventure.sector, keys=single_keys(worlds))

        return State.WORLD

    def _handle_world(self, update: Update, context: Context):
        homeworld = api.world(context.user_data.adventure.sector, update.message.text)
        if not homeworld:
            return State.WORLD

        context.user_data.character.homeworld = homeworld
        context.user_data.initial_skills_left = 3 + context.user_data.character.modifiers[Characteristics.EDU]

        kb.ask_homeworld_skill.reply_text(update, keys=single_keys(homeworld.homeworld_skills))
        return State.HOMEWORLD_SKILL

    def _handle_homeworld_skill(self, update: Update, context: Context):
        skill = update.message.text
        if skill not in context.user_data.character.homeworld.homeworld_skills:
            return State.HOMEWORLD_SKILL

        if len(context.user_data.character.skills) == 0:
            context.user_data.character.skills = []

        context.user_data.character.skills.append(skill)

def num_keys(start: int, end: int) -> List[List[str]]:
    kl = [str(i) for i in range(start, end + 1)]
    kl.append('Ignore')

    return [kl[i: i + 3] for i in range(0, len(kl), 3)]

def single_keys(l: List[str]) -> List[List[str]]:
    return [l[i: i + 1] for i in range(0, len(l), 1)]