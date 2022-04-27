from enum import Enum
from typing import List

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, CallbackContext, Filters

from travellermap.api import TravellerMap


class State(Enum):
    MAX_POP = 1


class CharacterCreationConversation:
    traveller_map: TravellerMap

    def __init__(self, traveller_map: TravellerMap):
        self.traveller_map = traveller_map

    def handlers(self) -> List[ConversationHandler]:
        return [ConversationHandler(
            entry_points=[MessageHandler(Filters.regex('^([1-9]|10|Ignore)$'), self._handle_min_pop)],
            states={
                State.MAX_POP: [MessageHandler(Filters.regex('^([1-9]|10|Ignore)$'), self._handle_max_pop)]
            },
            fallbacks=[]
        )]

    def _handle_min_pop(self, update: Update, context: CallbackContext):
        update.message.reply_text('Yay!')
        return State.MAX_POP

    def _handle_max_pop(self, update: Update, context: CallbackContext):
        update.message.reply_text('Bruh.')
        return State.MAX_POP
