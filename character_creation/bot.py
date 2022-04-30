from enum import Enum
from typing import List, Callable

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, CallbackContext, Filters

from character_creation import kb
from travellermap.api import TravellerMap


class State(Enum):
    MAX_POP = 1
    MIN_STARPORT = 2
    MAX_STARPORT = 3
    MIN_SIZE = 4
    MAX_SIZE = 5
    MIN_ATM = 6
    MAX_SIZE = 7


params = {
    'starport': 'Starport',
    'size': 'Size',
    'atm': 'Atmosphere',
    'hydro': 'Hydrographics',
    'pop': 'Population',
    'gov': 'Government',
    'law': 'Law Level',
    'tech': 'Technology Level'
}

class CharacterCreationConversation:
    traveller_map: TravellerMap

    def __init__(self, traveller_map: TravellerMap):
        self.traveller_map = traveller_map

    def handlers(self) -> List[ConversationHandler]:
        return [ConversationHandler(
            entry_points=[MessageHandler(Filters.regex('^(X|E|D|C|B|A|Ignore)$'), self._handle_min_starport)],
            states={
                State.MAX_STARPORT: [MessageHandler(Filters.regex('^(X|E|D|C|B|A|Ignore)$'), self._handle_max_starport)],
                State.MIN_SIZE: [MessageHandler(Filters.regex('^([1-9]|10|Ignore)$'), self._handle_min('size', 10, 'atm', 15))],
                State.MAX_SIZE: [MessageHandler(Filters.regex('^([1-9]|10|Ignore)$'), self._handle_max('size', 10, 'atm', 15))],
                State.MIN_SIZE: [MessageHandler(Filters.regex('^([1-9]|10|Ignore)$'), self._handle_min('size', 10, 'atm', 15))],
                State.MAX_SIZE: [MessageHandler(Filters.regex('^([1-9]|10|Ignore)$'), self._handle_max('size', 10, 'atm', 15))],
                State.MIN_SIZE: [MessageHandler(Filters.regex('^([1-9]|10|Ignore)$'), self._handle_min('size', 10, 'atm', 15))],
                State.MAX_SIZE: [MessageHandler(Filters.regex('^([1-9]|10|Ignore)$'), self._handle_max('size', 10, 'atm', 15))],
            },
            fallbacks=[]
        )]

    def _handle_min_starport(self, update: Update, context: CallbackContext) -> State:
        if update.message.text == 'Ignore':
            context.user_data['min_starport'] = 'X'
            context.user_data['max_starport'] = 'A'

            kb.min_kb.reply_text(params='Size', keys=num_keys(0, 10))

            return State.MIN_SIZE

        context.user_data['min_starport'] = update.message.text

        vals = ['X', 'E', 'D', 'C', 'B', 'A', 'Ignore']
        kl = [vals[i] for i in range(vals.index(update.message.text), len(vals))]
        keys = [kl[i: i + 3] for i in range(0, len(kl), 3)]

        kb.ask_max.reply_text(params='Starport', keys=keys)

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

        kb.ask_min.reply_text(params='Size', keys=num_keys(0, 10))
        return State.MIN_SIZE

    def _handle_min(self, param: str, max_value: int, next_param: str, next_max: int) -> Callable[[Update, CallbackContext], State]:
        def min_cb(update: Update, context: CallbackContext) -> State:
            if update.message.text == 'Ignore':
                context.user_data[f'min_{param}'] = 0
                context.user_data[f'max_{param}'] = max_value

                kb.min_kb.reply_text(params=params[next_param], keys=num_keys(0, next_max))

                return State[f'MIN_{next_param.upper()}']

            val = int(update.message.text)
            context.user_data['min_size'] = val

            kb.max_kb.reply_text(params[param], keys=num_keys(val, max))

            return State[f'MAX_{param.upper()}']

        return min_cb


    def _handle_max(self, param: str, max_value: int, next_param: str, next_max: int) -> Callable[[Update, CallbackContext], State]:
        def max_cb(update: Update, context: CallbackContext) -> State:
            if update.message.text == 'Ignore':
                context.user_data[f'max_{param}'] = max_value
            else:
                val = int(update.message.text)
                context.user_data[f'max_{param}'] = val if val >= context.user_data[f'min_{param}'] else context.user_data[f'min_{param}']

            kb.min_kb.reply_text(params[next_param], keys=num_keys(0, next_max))
            return State[f'MIN_{next_param.upper()}']

        return max_cb


def num_keys(start: int, end: int) -> List[List[str]]:
    kl = [str(i) for i in range(start, end + 1)]
    kl.append('Ignore')

    return [kl[i: i + 3] for i in range(0, len(kl), 3)]