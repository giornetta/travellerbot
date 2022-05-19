from typing import List
from enum import Enum, auto

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

from bot.state import ConversationState
from keyboards.keyboards import single_keys
from shop.service import Shop
from traveller import equipment as eq, queries as q

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
            kb.end.reply_text(update)
            return State.END
        keys = self.service.categories_from_shop(update.message.from_user.id)
        kb.ask_cat.reply_text(update, keys=single_keys(keys))
        return State.CHOICECATEGORY

    def _handle_cat(self, update: Update, context: CallbackContext) -> State:
        message = update.message.text.upper()
        split = message.split(':', 2)
        if split[0].title() not in self.service.categories_from_shop(update.message.from_user.id):
            kb.error_cat.reply_text(update)
            kb.ask.reply_text(update)
            return State.SHOP
        else:
            keys = []
            for e in eq.equipments:
                if isinstance(eq.equipments[e], eq.categories[split[0]]):
                    try:
                        if eq.equipments[e].technology_level <= int(split[1]) if len(split) > 1 else True:
                            if split[0] in ['SOFTWARE', 'COMPUTER']:
                                keys.append(
                                    f'{eq.equipments[e].name}:{eq.equipments[e].technology_level}')
                            elif split[0] in ['RANGED_AMMUNITION', 'HEAVY_WEAPON_AMMUNITION']:
                                keys.append(f'{eq.equipments[e].name}:Ammo')
                            else:
                                keys.append(f'{eq.equipments[e].name} - {eq.equipments[e].cost}Cr')
                    except ValueError:
                        kb.error_item.reply_text(update)
                        kb.ask.reply_text(update)
                        return State.SHOP
            kb.ask_item.reply_text(update, keys=single_keys(keys))
            return State.CHOICEITEM

    def _handle_item(self, update: Update, context: CallbackContext) -> State:
        item = update.message.text
        try:
            print(item)
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
