from enum import Enum
from typing import List

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

from adventure_setup.controller import SetupController
from conversations.state import ConversationState
from keyboards import keyboards
from travellermap.api import TravellerMap


class State(Enum):
    CODE = 0
    NAME = 1
    SECTOR = 2
    WORLD = 3
    TERMS = 4
    SURVIVAL = 5
    END = 6


class SetupConversation:
    controller: SetupController
    traveller_map: TravellerMap

    def __init__(self, controller: SetupController, traveller_map: TravellerMap):
        self.controller = controller
        self.traveller_map = traveller_map

    def handlers(self) -> List[ConversationHandler]:
        return [
            ConversationHandler(
                entry_points=[MessageHandler(Filters.text('Create'), self._ask_adventure_name)],
                states={
                    State.NAME: [MessageHandler(Filters.text, self._handle_adventure_name)],
                    State.SECTOR: [
                        MessageHandler(Filters.regex('^(Let me choose|Choose another)$'), self._ask_sector),
                        MessageHandler(Filters.regex('^(Generate Random|Generate another)$'),
                                       self._handle_random_sector),
                        MessageHandler(Filters.text('Accept'), self._handle_accept_random_sector),
                        MessageHandler(Filters.text, self._handle_sector)
                    ],
                    State.WORLD: [
                        MessageHandler(Filters.regex('^(Let me choose|Choose another)$'), self._ask_world),
                        MessageHandler(Filters.regex('^(Generate Random|Generate another)$'),
                                       self._handle_random_world),
                        MessageHandler(Filters.text('Accept'), self._handle_accept_random_world),
                        MessageHandler(Filters.text, self._handle_world)
                    ],
                    State.TERMS: [MessageHandler(Filters.text, self._handle_terms)],
                    State.SURVIVAL: [MessageHandler(Filters.text, self._handle_survival)]
                },
                fallbacks=[],
                map_to_parent={
                    State.END: ConversationState.ADVENTURE_SETUP  # TODO Change
                },
                name='create_adventure',
                persistent=True
            ),
            ConversationHandler(
                entry_points=[MessageHandler(Filters.text('Join'), self._ask_adventure_code)],
                states={
                    State.CODE: [MessageHandler(Filters.text, self._handle_adventure_code)]
                },
                fallbacks=[],
                map_to_parent={
                    State.END: ConversationState.CHARACTER_CREATION
                },
                name='join_adventure',
                persistent=True
            )
        ]

    def _ask_adventure_code(self, update: Update, context: CallbackContext) -> State:
        keyboards.adv_code.reply_text(update)
        return State.CODE

    def _handle_adventure_code(self, update: Update, context: CallbackContext) -> State:
        adventure = self.controller.join_adventure(update.message.from_user.id, update.message.text)
        if adventure:
            keyboards.join_adventure.reply_text(update, adventure)
            keyboards.create_char.reply_text(update)
            return State.END
        else:
            keyboards.invalid_code.reply_text(update)
            return State.CODE

    def _ask_adventure_name(self, update: Update, context: CallbackContext) -> State:
        keyboards.adv_name.reply_text(update)
        return State.NAME

    def _handle_adventure_name(self, update: Update, context: CallbackContext) -> State:
        # TODO check if valid
        context.user_data["adventure_name"] = update.message.text
        keyboards.sector.reply_text(update)
        return State.SECTOR

    def _ask_sector(self, update: Update, context: CallbackContext) -> State:
        keyboards.sector_name.reply_text(update)
        return State.SECTOR

    def _handle_sector(self, update: Update, context: CallbackContext) -> State:
        sector = update.message.text.title()

        if sector in self.traveller_map.sectors:
            context.user_data['adventure_sector'] = sector
            keyboards.world.reply_text(update)
            return State.WORLD
        else:
            keyboards.no_sector.reply_text(update)
            return State.SECTOR

    def _handle_random_sector(self, update: Update, context: CallbackContext) -> State:
        sector = self.traveller_map.random_sector()

        context.user_data['adventure_sector'] = sector
        keyboards.confirm_sector.reply_text(update, sector)

        return State.SECTOR

    def _handle_accept_random_sector(self, update: Update, context: CallbackContext) -> State:
        keyboards.world.reply_text(update)
        return State.WORLD

    def _ask_world(self, update: Update, context: CallbackContext) -> State:
        keyboards.world_name.reply_text(update)
        return State.WORLD

    def _handle_world(self, update: Update, context: CallbackContext) -> State:
        world = update.message.text.title()

        if world in self.traveller_map.worlds(context.user_data["adventure_sector"]):
            context.user_data["adventure_world"] = world
            keyboards.terms.reply_text(update)
            return State.TERMS
        else:
            keyboards.no_world.reply_text(update)
            return State.WORLD

    def _handle_random_world(self, update: Update, context: CallbackContext) -> State:
        world = self.traveller_map.random_world(context.user_data["adventure_sector"])

        context.user_data["adventure_world"] = world
        keyboards.confirm_world.reply_text(update,world)

        return State.WORLD

    def _handle_accept_random_world(self, update: Update, context: CallbackContext) -> State:
        keyboards.terms.reply_text(update)
        return State.TERMS

    def _handle_terms(self, update: Update, context: CallbackContext) -> State:
        try:
            terms = int(update.message.text)
            context.user_data["adventure_terms"] = terms
            keyboards.survival_roll.reply_text(update)
            return State.SURVIVAL
        except ValueError:
            keyboards.invalid_choice.reply_text(update)
            return State.TERMS

    def _handle_survival(self, update: Update, context: CallbackContext) -> State:
        if update.message.text == "Yes" or "No":
            context.user_data["adventure_survival"] = update.message.text == "Yes"

            code = self.controller.create_adventure(
                update.message.from_user.id,
                context.user_data["adventure_name"],
                context.user_data["adventure_sector"],
                context.user_data["adventure_world"],
                context.user_data["adventure_terms"],
                context.user_data["adventure_survival"]
            )

            update.message.reply_text(
                text=f'Created Adventure #<code>{code}</code>!',
                parse_mode='html',
                reply_markup=ReplyKeyboardRemove()
            )
            return State.END
