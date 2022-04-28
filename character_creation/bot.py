from collections import OrderedDict
from enum import Enum, auto
from typing import List, Callable

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, CallbackContext, Filters

from character_creation import kb
from character_creation.service import CharacterCreator
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
                State.MIN_SIZE: [MessageHandler(filter_10, self._handle_min('size'))],
                State.MAX_SIZE: [MessageHandler(filter_10, self._handle_max('size'))],
                State.MIN_ATM: [MessageHandler(filter_15, self._handle_min('atm'))],
                State.MAX_ATM: [MessageHandler(filter_15, self._handle_max('atm'))],
                State.MIN_HYDRO: [MessageHandler(filter_10, self._handle_min('hydro'))],
                State.MAX_HYDRO: [MessageHandler(filter_10, self._handle_max('hydro'))],
                State.MIN_POP: [MessageHandler(filter_10, self._handle_min('pop'))],
                State.MAX_POP: [MessageHandler(filter_10, self._handle_max('pop'))],
                State.MIN_GOV: [MessageHandler(filter_15, self._handle_min('gov'))],
                State.MAX_GOV: [MessageHandler(filter_15, self._handle_max('gov'))],
                State.MIN_LAW: [MessageHandler(filter_10, self._handle_min('law'))],
                State.MAX_LAW: [MessageHandler(filter_10, self._handle_max('law'))],
                State.MIN_TECH: [MessageHandler(filter_15, self._handle_min_tech)],
                State.MAX_TECH: [MessageHandler(filter_15, self._handle_max_tech)],
                State.WORLD: [MessageHandler(Filters.text, self._handle_world)],
                State.HOMEWORLD_SKILL: [MessageHandler(Filters.text, self._handle_homeworld_skill)]

            },
            fallbacks=[]
        )]

    def _handle_min_starport(self, update: Update, context: CallbackContext) -> State:
        if update.message.text == 'Ignore':
            context.user_data['min_starport'] = 'X'
            context.user_data['max_starport'] = 'A'

            kb.ask_min.reply_text(update, params='Size', keys=num_keys(0, 10))

            return State.MIN_SIZE

        context.user_data['min_starport'] = update.message.text

        vals = ['X', 'E', 'D', 'C', 'B', 'A', 'Ignore']
        kl = [vals[i] for i in range(vals.index(update.message.text), len(vals))]
        keys = [kl[i: i + 3] for i in range(0, len(kl), 3)]

        kb.ask_max.reply_text(update, params='Starport', keys=keys)

        return State.MAX_STARPORT

    def _handle_max_starport(self, update: Update, context: CallbackContext) -> State:
        val = update.message.text
        vals = ['X', 'E', 'D', 'C', 'B', 'A', 'Ignore']

        if val == 'Ignore':
            context.user_data['max_starport'] = 'A'
        else:
            if vals.index(val) < vals.index(context.user_data['min_starport']):
                context.user_data['max_starport'] = context.user_data['min_starport']
            else:
                context.user_data['max_starport'] = val

        kb.ask_min.reply_text(update, params='Size', keys=num_keys(0, params['size'][1]))
        return State.MIN_SIZE

    def _handle_min(self, param: str) -> Callable[[Update, CallbackContext], State]:
        def min_cb(update: Update, context: CallbackContext) -> State:
            if update.message.text == 'Ignore':
                context.user_data[f'min_{param}'] = 0
                context.user_data[f'max_{param}'] = params[param][1]

                next_index = list(params).index(param) + 1
                next_param, next_val = list(params.items())[next_index]

                kb.ask_min.reply_text(update, params=next_val[0], keys=num_keys(0, next_val[1]))

                return State[f'MIN_{next_param.upper()}']

            val = int(update.message.text)
            context.user_data[f'min_{param}'] = val

            kb.ask_max.reply_text(update, params=params[param][0], keys=num_keys(val, params[param][1]))

            return State[f'MAX_{param.upper()}']

        return min_cb

    def _handle_max(self, param: str) -> Callable[[Update, CallbackContext], State]:
        def max_cb(update: Update, context: CallbackContext) -> State:
            if update.message.text == 'Ignore':
                context.user_data[f'max_{param}'] = params[param][1]
            else:
                val = int(update.message.text)
                context.user_data[f'max_{param}'] = val if val >= context.user_data[f'min_{param}'] else context.user_data[f'min_{param}']

            next_index = list(params).index(param) + 1
            next_param, next_val = list(params.items())[next_index]

            kb.ask_min.reply_text(update, params=next_val[0], keys=num_keys(0, next_val[1]))
            return State[f'MIN_{next_param.upper()}']

        return max_cb

    def _handle_min_tech(self, update: Update, context: CallbackContext):
        if update.message.text == 'Ignore':
            context.user_data[f'min_tech'] = 0
            context.user_data[f'max_tech'] = params['tech'][1]

            return self._world_selection(update, context)

        val = int(update.message.text)
        context.user_data['min_tech'] = val
        kb.ask_max.reply_text(update, params=params['tech'][0], keys=num_keys(val, params['tech'][1]))

        return State.MAX_TECH

    def _handle_max_tech(self, update: Update, context: CallbackContext) -> State:
        if update.message.text == 'Ignore':
            context.user_data['max_tech'] = params['tech'][1]
        else:
            val = int(update.message.text)
            context.user_data['max_tech'] = val if val >= context.user_data['min_tech'] else context.user_data['min_tech']

        return self._world_selection(update, context)

    def _world_selection(self, update: Update, context: CallbackContext):
        worlds = self.service.world_selection(
            context.user_data['adventure_sector'],
            min_starport=context.user_data['min_starport'], max_starport=context.user_data['max_starport'],
            min_size=context.user_data['min_size'], max_size=context.user_data['max_size'],
            min_atm=context.user_data['min_atm'], max_atm=context.user_data['max_atm'],
            min_hydro=context.user_data['min_hydro'], max_hydro=context.user_data['max_hydro'],
            min_pop=context.user_data['min_pop'], max_pop=context.user_data['max_pop'],
            min_gov=context.user_data['min_gov'], max_gov=context.user_data['max_gov'],
            min_law=context.user_data['min_law'], max_law=context.user_data['max_law'],
            min_tech=context.user_data['min_tech'], max_tech=context.user_data['max_tech']
        )

        if len(worlds) == 0:
            kb.no_world_found.reply_text(update)
            kb.ask_min.reply_text(update, params='Starport', keys=[['X', 'E', 'D'], ['C', 'B', 'A'], ['Ignore']])
            return State.MIN_STARPORT

        kb.choose_world.reply_text(update, params=context.user_data['adventure_sector'], keys=single_keys(worlds))

        return State.WORLD

    def _handle_world(self, update: Update, context: CallbackContext):
        if update.message.text not in api.worlds(context.user_data['adventure_sector']):
            update.message.reply_text('MMMMMM')
            return State.WORLD

        context.user_data['homeworld'] = update.message.text

        skills = self.service.homeworld_skills(context.user_data['adventure_sector'], context.user_data['homeworld'])

        context.user_data['initial_skills_left'] = 3 + context.user_data['modifiers']['EDU']
        context.user_data['homeworld_skills'] = skills

        kb.first_homeworld_skill.reply_text(update, keys=single_keys(skills))
        return State.HOMEWORLD_SKILL

    def _handle_homeworld_skill(self, update: Update, context: CallbackContext):
        update.message.reply_text('Bravoo')


def num_keys(start: int, end: int) -> List[List[str]]:
    kl = [str(i) for i in range(start, end + 1)]
    kl.append('Ignore')

    return [kl[i: i + 3] for i in range(0, len(kl), 3)]

def single_keys(l: List[str]) -> List[List[str]]:
    return [l[i: i + 1] for i in range(0, len(l), 1)]