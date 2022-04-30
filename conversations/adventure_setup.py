from enum import Enum
from typing import List

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

import character_creation
from adventure_setup import kb
from adventure_setup.service import SetupController
from character_creation.service import CharacterCreator
from conversations.state import ConversationState
from character_creation import kb
from travellermap.api import TravellerMap


class State(Enum):
    CODE = 0
    NAME = 1
    SECTOR = 2
    WORLD = 3
    TERMS = 4
    SURVIVAL = 5
    END = 6
    END_REF = 7
    END_IDLE = 8


class SetupConversation:
    controller: SetupController
    character_creator: CharacterCreator
    traveller_map: TravellerMap

    def __init__(self, controller: SetupController, character_creator: CharacterCreator, traveller_map: TravellerMap):
        self.controller = controller
        self.character_creator = character_creator
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
                    State.SURVIVAL: [MessageHandler(Filters.regex('^(Yes|No)$'), self._handle_survival)]
                },
                fallbacks=[],
                map_to_parent={
                    State.END: ConversationState.REFEREE_IDLE
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
                    State.END: ConversationState.CHARACTER_CREATION,
                    State.END_REF: ConversationState.REFEREE_IDLE,
                    State.END_IDLE: ConversationState.PLAYER_IDLE,
                },
                name='join_adventure',
                persistent=True
            )
        ]

    def _ask_adventure_code(self, update: Update, context: CallbackContext) -> State:
        kb.adv_code.reply_text(update)
        return State.CODE

    def _handle_adventure_code(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        adventure_id = update.message.text

        res = self.controller.join_adventure(user_id, adventure_id)
        if res:
            adventure_name, is_ref = res
            kb.join_adventure(adventure_name)
            if is_ref:
                return State.END_REF
            else:
                if self.character_creator.alive_character_exists(user_id, adventure_id):
                    return State.END_IDLE
                else:
                    kb.create_char.reply_text()

                    chars = CharacterCreator.roll()
                    context.user_data['characteristics'] = chars
                    update.message.reply_text(f'STR: {chars["STR"]}\nDEX: {chars["DEX"]}')

                    character_creation.kb.characteristics.reply_text(
                        update, 
                        params=(chars['STR'], chars['END'], chars['DEX'], chars['INT'], chars['EDU'], chars['SOC'])
                    )

                    sector = self.character_creator.sector(adventure_id)
                    character_creation.kb.world(sector)

                    character_creation.kb.ask_min.reply_text(
                        update, params='Starport',
                        keys=[['X', 'E', 'D'], ['C', 'B', 'A'], ['Ignore']]
                    )
                    return State.END
        else:
            update.message.reply_text('The provided code isn\'t valid, try again.')
            return State.CODE

    def _ask_adventure_name(self, update: Update, context: CallbackContext) -> State:
        kb.title.reply_text(update)
        return State.NAME

    def _handle_adventure_name(self, update: Update, context: CallbackContext) -> State:
        # TODO check if valid
        context.user_data["adventure_name"] = update.message.text
        kb.sector.reply_text(update)
        return State.SECTOR

    def _ask_sector(self, update: Update, context: CallbackContext) -> State:
        kb.sector_name.reply_text(update)
        return State.SECTOR

    def _handle_sector(self, update: Update, context: CallbackContext) -> State:
        sector = update.message.text.title()

        if sector in self.traveller_map.sectors:
            context.user_data['adventure_sector'] = sector
            kb.world.reply_text(update)
            return State.WORLD
        else:
            kb.no_sector.reply_text(update)
            return State.SECTOR

    def _handle_random_sector(self, update: Update, context: CallbackContext) -> State:
        sector = self.traveller_map.random_sector()

        context.user_data['adventure_sector'] = sector
        kb.confirm_sector.reply_text(update, sector)

        return State.SECTOR

    def _handle_accept_random_sector(self, update: Update, context: CallbackContext) -> State:
        kb.world.reply_text(update)
        return State.WORLD

    def _ask_world(self, update: Update, context: CallbackContext) -> State:
        kb.world_name.reply_text(update)
        return State.WORLD

    def _handle_world(self, update: Update, context: CallbackContext) -> State:
        world = update.message.text.title()

        if world in self.traveller_map.worlds(context.user_data["adventure_sector"]):
            context.user_data["adventure_world"] = world
            kb.terms.reply_text(update)
            return State.TERMS
        else:
            kb.no_world.reply_text(update)
            return State.WORLD

    def _handle_random_world(self, update: Update, context: CallbackContext) -> State:
        world = self.traveller_map.random_world(context.user_data["adventure_sector"])

        context.user_data["adventure_world"] = world
        kb.confirm_world.reply_text(update, world)

        return State.WORLD

    def _handle_accept_random_world(self, update: Update, context: CallbackContext) -> State:
        kb.terms.reply_text(update)
        return State.TERMS

    def _handle_terms(self, update: Update, context: CallbackContext) -> State:
        try:
            terms = int(update.message.text)
            context.user_data["adventure_terms"] = terms
            kb.survival_roll.reply_text(update)
            return State.SURVIVAL
        except ValueError:
            kb.invalid_choice.reply_text(update)
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

            kb.adventure_created.reply_text(params=code)
            
            return State.END
