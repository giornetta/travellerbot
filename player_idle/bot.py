from enum import Enum, auto
from typing import List

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

from player_idle import kb
from player_idle.service import PlayerIdle
from cache.userdata import user_data, UserData


class State(Enum):
    IDLE = auto()
    INVENTORY = auto()
    INFO = auto()
    ITEM = auto()


class PlayerIdleConversation:
    service: PlayerIdle

    def __init__(self, service: PlayerIdle):
        self.service = service

    def handlers(self) -> List[ConversationHandler]:
        return [ConversationHandler(
            entry_points=[MessageHandler(Filters.text, self._handle_created)],
            states={
                State.IDLE: [MessageHandler(Filters.regex('^(Info|Inventory|Map)$'), self._handle_idle)],
                State.INFO: [MessageHandler(Filters.regex('^(World|Adventure|Myself)$'), self._handle_info)],
                State.ITEM: [MessageHandler(Filters.regex('^[Use|Throw|Nothing]'), self._handle_item)],
                State.INVENTORY: [MessageHandler(Filters.text, self._handle_inventory)]
            },
            fallbacks=[],
            map_to_parent={},
            name='create_character',
            persistent=True,
        )]

    def _handle_created(self, update: Update, context: CallbackContext) -> State:
        kb.idle.reply_text(update)
        return State.IDLE

    def _handle_idle(self, update: Update, context: CallbackContext) -> State:
        text = update.message.text
        if text == 'Info':
            kb.info.reply_text(update)
            return State.INFO
        elif text == 'Inventory':
            kb.inventory.reply_text(update, keys=self.service.get_items(update.message.from_user.id))
            return State.INVENTORY
        elif text == 'Map':
            url = self.service.info_map(update.message.from_user.id)
            update.message.reply_photo(url)
            kb.idle.reply_text(update)
            return State.IDLE

    def _handle_info(self, update: Update, context: CallbackContext) -> State:
        text = update.message.text
        if text == 'World':
            update.message.reply_text(self.service.info_world(update.message.from_user.id))
            kb.idle.reply_text(update)
            return State.IDLE
        elif text == 'Adventure':
            update.message.reply_text(self.service.info_adventure(update.message.from_user.id))
            kb.idle.reply_text(update)
            return State.IDLE
        elif text == 'Myself':
            update.message.reply_text(self.service.info_myself(update.message.from_user.id))
            kb.idle.reply_text(update)
            return State.IDLE

    def _handle_inventory(self, update: Update, context: CallbackContext) -> State:
        if update.message.text == 'Nothing':
            kb.idle.reply_text(update)
            return State.IDLE
        item, e = self.service.is_item(update.message.text)
        if item:
            user_data[update.message.from_user.id] = UserData()
            user_data[update.message.from_user.id].item = update.message.text
            user_data[update.message.from_user.id].item_id = e
            kb.item.reply_text(update)
            return State.ITEM
        kb.item_error.reply_text(update)
        kb.idle.reply_text(update)
        return State.IDLE

    def _handle_item(self, update: Update, context: CallbackContext) -> State:
        item_id = user_data[update.message.from_user.id].item_id
        text = update.message.text
        if text == 'Nothing':
            kb.idle.reply_text(update)
            return State.IDLE
        if text == 'Use':
            self.service.remove_item(update.message.from_user.id, item_id)
            kb.idle.reply_text(update)
            kb.use.reply_text(update)
            return State.IDLE
        if text == 'Throw':
            self.service.remove_item(update.message.from_user.id, item_id)
            kb.idle.reply_text(update)
            kb.throw.reply_text(update)
            return State.IDLE
