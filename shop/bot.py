from typing import List
from enum import Enum, auto

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext
from traveller import equipment as eq, queries as q

from shop import kb


class State(Enum):
    CHOICE = auto()


# TODO finish shop
def handlers(self) -> List[ConversationHandler]:
    return [ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Yes)$'), self._handle_start)],
        states={
            State.CHOICE: [MessageHandler(Filters.regex('^(Info|Inventory|Map)$'), self._handle_choice)],
        },
        fallbacks=[],
        map_to_parent={},
        name='shop',
        persistent=True,
    )]


def _handle_start(self, update: Update, context: CallbackContext) -> State:
    items = q.eq_name_from_id(list(range(len(eq.equipments))))
    kb.choice.reply_text(update, keys=items)
    return State.CHOICE
