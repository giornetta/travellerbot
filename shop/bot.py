from typing import List
from enum import Enum, auto

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

import player_idle.kb
from bot.state import ConversationState
from keyboards.keyboards import single_keys
from shop.service import Shop
from traveller import equipment as eq, queries as q, world

from shop import kb


class State(Enum):
    SHOP = auto()
    CHOICECATEGORY = auto()
    CHOICEITEM = auto()
    END = auto()


class ShopConversation:
    service: Shop

    def __init__(self, service: Shop):
        self.service = service

    def handlers(self) -> List[ConversationHandler]:
        return [ConversationHandler(
            entry_points=[MessageHandler(Filters.regex('^(Yes|No)$'), self._handle_shop)],
            states={
                State.CHOICECATEGORY: [MessageHandler(Filters.text, self._handle_cat)],
                State.CHOICEITEM: [MessageHandler(Filters.text, self._handle_item)],
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
            player_idle.kb.idle.reply_text(update)
            return State.END

        keys = self.service.categories_from_shop(update.message.from_user.id)
        if len(keys) == 0:
            kb.error_shop.reply_text(update)
            player_idle.kb.idle.reply_text(update)
            return State.END
        keys.append('Skip')
        kb.ask_cat.reply_text(update, keys=single_keys(keys))

        return State.CHOICECATEGORY

    def _handle_cat(self, update: Update, context: CallbackContext) -> State:
        message = update.message.text.title()
        if message == 'Skip':
            player_idle.kb.idle.reply_text(update)
            return State.END

        if message not in self.service.categories_from_shop(update.message.from_user.id):
            kb.error_cat.reply_text(update)
            kb.ask.reply_text(update)
            return State.SHOP

        tl = self.service.tl(update.message.from_user.id)
        if tl is None:
            tl = world.Attribute.TECH.max

        char_creds = self.service.character_credits(update.message.from_user.id)

        keys = []
        cat = message.upper().replace(' ', '_')
        for e in eq.equipments:
            if isinstance(eq.equipments[e], eq.categories[cat]):
                try:
                    if eq.equipments[e].technology_level <= tl and char_creds >= eq.equipments[e].cost:
                        if cat in ['SOFTWARE', 'COMPUTER']:
                            keys.append(
                                f'{eq.equipments[e].name}:{eq.equipments[e].technology_level} - {eq.equipments[e].cost}Cr')
                        elif cat in ['RANGED_AMMUNITION', 'HEAVY_WEAPON_AMMUNITION']:
                            keys.append(f'{eq.equipments[e].name}:Ammo - {eq.equipments[e].cost}Cr')
                        else:
                            keys.append(f'{eq.equipments[e].name} - {eq.equipments[e].cost}Cr')
                except ValueError:
                    kb.error_item.reply_text(update)
                    kb.ask.reply_text(update)
                    return State.SHOP
        keys.append("Skip")
        kb.ask_item.reply_text(update, keys=single_keys(keys))
        return State.CHOICEITEM

    def _handle_item(self, update: Update, context: CallbackContext) -> State:
        item = update.message.text
        if item.title() == 'Skip':
            player_idle.kb.idle.reply_text(update)
            return State.END
        try:
            bought, credits_remaining = self.service.add(
                update.message.from_user.id, eq.get_equipment_by_name(item.split(" - ", 2)[0]))
            if bought:
                kb.success.reply_text(update, params=credits_remaining)
                kb.ask.reply_text(update)
                return State.SHOP
            else:
                kb.no_money.reply(update)
                kb.ask.reply_text(update)
                return State.SHOP
        except AttributeError:
            kb.error_item.reply_text(update)
            kb.ask.reply_text(update)
            return State.SHOP
