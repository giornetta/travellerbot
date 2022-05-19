from typing import List
from enum import Enum, auto

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

from bot.state import ConversationState
from shop.service import Shop
from traveller import equipment as eq, queries as q

from shop import kb


class State(Enum):
    SHOP = auto()
    CHOICE = auto()
    END = auto()


class ShopConversation:
    service: Shop

    def __init__(self, service: Shop):
        self.service = service

    def handlers(self) -> List[ConversationHandler]:
        return [ConversationHandler(
            entry_points=[MessageHandler(Filters.regex('^(Yes|No)$'), self._handle_shop)],
            states={
                State.CHOICE: [MessageHandler(Filters.text, self._handle_choice)],
                State.SHOP: [MessageHandler(Filters.regex('^(Yes|No)$'), self._handle_shop)]
            },
            fallbacks=[],
            map_to_parent={
                State.END: ConversationState.PLAYER_IDLE
            },
            name='shop',
            persistent=True,
        )]

    def _handle_shop(self, update: Update, context: CallbackContext) -> State:
        if update.message.text == 'No':
            self.service.set_created(update.message.from_user.id)
            kb.end.reply_text(update)
            return State.END
        items = self.service.items_from_shop(update.message.from_user.id)
        kb.choice.reply_text(update, keys=items)
        return State.CHOICE

    def _handle_choice(self, update: Update, context: CallbackContext) -> State:
        found, eq_id = q.is_item(update.message.text)
        if not found:
            kb.error_item.reply_text(update)
            kb.ask.reply_text(update)
            return State.SHOP
