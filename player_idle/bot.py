import re
from enum import Enum, auto
from typing import List

import telegram
from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

import keyboards.keyboards
from bot.state import ConversationState
from keyboards.keyboards import single_keys
from player_idle import kb
from player_idle.service import PlayerIdle
from cache.userdata import user_data, UserData
from traveller import skill


class State(Enum):
    IDLE = auto()
    INVENTORY = auto()
    INFO = auto()
    ITEM = auto()
    SKILL_CHECK = auto()
    DIFFICULTY = auto()
    SHOP = auto()
    EXIT = auto()


class PlayerIdleConversation:
    service: PlayerIdle

    def __init__(self, service: PlayerIdle):
        self.service = service

    def handlers(self) -> List[ConversationHandler]:
        return [ConversationHandler(
            entry_points=[MessageHandler(Filters.text, self._handle_created)],
            states={
                State.IDLE: [
                    MessageHandler(Filters.regex('^(Info|Inventory|Map|Skill Check|Shop|Exit)$'), self._handle_idle)],
                State.INFO: [MessageHandler(Filters.regex('^(World|Adventure|Myself|Scenes)$'), self._handle_info)],
                State.ITEM: [MessageHandler(Filters.regex('^(Use|Throw|Nothing)'), self._handle_item)],
                State.INVENTORY: [MessageHandler(Filters.text, self._handle_inventory)],
                State.SKILL_CHECK: [MessageHandler(Filters.text, self._handle_skill)],
                State.DIFFICULTY: [
                    MessageHandler(Filters.regex('^(Easy|Simple|Routine|Average|Difficult|Very Difficult|Formidable)$'),
                                   self._handle_difficulty)]
            },
            fallbacks=[],
            map_to_parent={
                State.SHOP: ConversationState.SHOP,
                State.EXIT: ConversationState.ADVENTURE_SETUP
            },
            name='player_idle',
            persistent=True,
        )]

    def _handle_created(self, update: Update, context: CallbackContext) -> State:
        if re.match('^(Info|Inventory|Map|Skill Check|Shop|Exit)$', update.message.text):
            return self._handle_idle(update, context)

        kb.idle.reply_text(update)
        return State.IDLE

    def _handle_idle(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        text = update.message.text

        if text == 'Info':
            kb.info.reply_text(update)
            return State.INFO
        elif text == 'Inventory':
            kb.inventory.reply_text(update, keys=self.service.get_items(user_id))
            return State.INVENTORY
        elif text == 'Map':
            url = self.service.info_map(user_id)
            update.message.reply_photo(url)
            kb.idle.reply_text(update)
            return State.IDLE
        elif text == 'Skill Check':
            skillset = self.service.skill_levels(user_id)
            kb.skill_check.reply_text(update, keys=single_keys(skillset))
            return State.SKILL_CHECK
        elif text == 'Shop':
            kb.ask_shop.reply_text(update)
            return State.SHOP
        elif text == 'Exit':
            keyboards.keyboards.welcome.reply_text(update)
            return State.EXIT

    def _handle_info(self, update: Update, context: CallbackContext) -> State:
        text = update.message.text
        if text == 'World':
            update.message.reply_text(self.service.info_world(update.message.from_user.id),
                                      parse_mode=telegram.ParseMode.HTML)
        elif text == 'Adventure':
            update.message.reply_text(self.service.info_adventure(update.message.from_user.id),
                                      parse_mode=telegram.ParseMode.HTML)
        elif text == 'Myself':
            update.message.reply_text(self.service.info_myself(update.message.from_user.id),
                                      parse_mode=telegram.ParseMode.HTML)
        elif text == 'Scenes':
            update.message.reply_text(self.service.info_scene(update.message.from_user.id),
                                      parse_mode=telegram.ParseMode.HTML)
        kb.idle.reply_text(update)

        return State.IDLE

    def _handle_inventory(self, update: Update, context: CallbackContext) -> State:
        if update.message.text == 'Nothing':
            kb.idle.reply_text(update)
            return State.IDLE
        item, e = self.service.is_item(update.message.text.replace(" ", ""))
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

    def _handle_skill(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id

        if update.message.text not in self.service.skill_levels(user_id):
            return State.SKILL_CHECK

        user_data[user_id].skill = update.message.text

        kb.difficulty.reply_text(update)
        return State.DIFFICULTY

    def _handle_difficulty(self, update: Update, context: CallbackContext) -> State:
        user = user_data[update.message.from_user.id]

        result, msg = skill.check(user.skill, update.message.text)
        if result >= 8:
            kb.skill_check_success.reply_text(update, params=(result, msg))
        else:
            kb.skill_check_fail.reply_text(update, params=(result, msg))

        kb.idle.reply_text(update)
        return State.IDLE
