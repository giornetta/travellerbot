from enum import Enum
from typing import List

from telegram import Update
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext

from adventure_setup.service import AdventureSetupService
from cache.userdata import user_data
from character_creation.bot import start_character_creation
from character_creation.service import CharacterCreator
from bot.state import ConversationState
from adventure_setup import kb
from traveller.adventure import Adventure
from travellermap import api


class State(Enum):
    CODE = 0
    TITLE = 1
    SECTOR = 2
    WORLD = 3
    TERMS = 4
    SURVIVAL = 5
    END = 6
    END_REF = 7
    END_IDLE = 8


class SetupConversation:
    service: AdventureSetupService
    character_creator: CharacterCreator

    def __init__(self, service: AdventureSetupService, character_creator: CharacterCreator):
        self.service = service
        self.character_creator = character_creator

    def handlers(self) -> List[ConversationHandler]:
        return [
            ConversationHandler(
                entry_points=[MessageHandler(Filters.regex('^(Create)$'), self._ask_adventure_title)],
                states={
                    State.TITLE: [MessageHandler(Filters.text, self._handle_adventure_title)],
                    State.SECTOR: [
                        MessageHandler(Filters.regex('^(Let me choose|Choose another)$'), self._ask_sector),
                        MessageHandler(Filters.regex('^(Generate Random|Generate another)$'),
                                       self._handle_random_sector),
                        MessageHandler(Filters.regex('^(Accept)$'), self._handle_accept_random_sector),
                        MessageHandler(Filters.text, self._handle_sector)
                    ],
                    State.WORLD: [
                        MessageHandler(Filters.regex('^(Let me choose|Choose another)$'), self._ask_world),
                        MessageHandler(Filters.regex('^(Generate Random|Generate another)$'),
                                       self._handle_random_world),
                        MessageHandler(Filters.regex('^(Accept)$'), self._handle_accept_random_world),
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
                entry_points=[MessageHandler(Filters.regex('^(Join)$'), self._ask_adventure_code)],
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
                persistent=True,
            )
        ]

    def _ask_adventure_code(self, update: Update, context: CallbackContext) -> State:
        kb.adv_code.reply_text(update)
        return State.CODE

    def _handle_adventure_code(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        adventure_id = update.message.text.upper()

        adventure = self.service.join_adventure(user_id, adventure_id)
        if adventure:
            # Create a new adventure to store the information
            user_data[user_id].adventure = adventure

            kb.join_adventure.reply_text(update, adventure.title)

            if user_id == adventure.referee_id:
                return State.END_REF
            else:
                if self.character_creator.alive_character_exists(user_id, adventure.id):
                    return State.END_IDLE
                else:
                    kb.create_char.reply_text(update)
                    start_character_creation(update)
                    return State.END
        else:
            update.message.reply_text('The provided code isn\'t valid, try again.')
            return State.CODE

    def _ask_adventure_title(self, update: Update, context: CallbackContext) -> State:
        kb.title.reply_text(update)
        return State.TITLE

    def _handle_adventure_title(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        if len(update.message.text) > 64:  # TODO better validation
            kb.invalid_title.reply_text(update)
            return State.TITLE

        user_data[user_id].adventure = Adventure()
        user_data[user_id].adventure.title = update.message.text

        kb.sector.reply_text(update)
        return State.SECTOR

    def _ask_sector(self, update: Update, context: CallbackContext) -> State:
        kb.sector_name.reply_text(update)
        return State.SECTOR

    def _handle_sector(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        sector = update.message.text.title()

        if sector in api.sectors():
            user_data[user_id].adventure.sector = sector
            kb.world.reply_text(update)
            return State.WORLD
        else:
            kb.no_sector.reply_text(update)
            return State.SECTOR

    def _handle_random_sector(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        sector = api.random_sector()

        user_data[user_id].adventure.sector = sector
        kb.confirm_sector.reply_text(update, params=sector)

        return State.SECTOR

    def _handle_accept_random_sector(self, update: Update, context: CallbackContext) -> State:
        kb.world.reply_text(update)
        return State.WORLD

    def _ask_world(self, update: Update, context: CallbackContext) -> State:
        kb.world_name.reply_text(update)
        return State.WORLD

    def _handle_world(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        world = update.message.text.title()

        if world in api.world_names(user_data[user_id].adventure.sector):
            user_data[user_id].adventure.world = world
            kb.terms.reply_text(update)
            return State.TERMS
        else:
            kb.no_world.reply_text(update)
            return State.WORLD

    def _handle_random_world(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        world = api.random_world(user_data[user_id].adventure.sector)

        user_data[user_id].adventure.world = world.name
        kb.confirm_world.reply_text(update, params=world.name)

        return State.WORLD

    def _handle_accept_random_world(self, update: Update, context: CallbackContext) -> State:
        kb.terms.reply_text(update)
        return State.TERMS

    def _handle_terms(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        try:
            terms = int(update.message.text)
            user_data[user_id].adventure.terms = terms
            kb.survival_roll.reply_text(update)
            return State.SURVIVAL
        except ValueError:
            kb.invalid_choice.reply_text(update)
            return State.TERMS

    def _handle_survival(self, update: Update, context: CallbackContext) -> State:
        user_id = update.message.from_user.id
        if update.message.text == "Yes" or "No":
            user_data[user_id].adventure.survival_kills = update.message.text == "Yes"

            adv_id = self.service.create_adventure(user_id, user_data[user_id].adventure)
            user_data[user_id].adventure.id = adv_id

            kb.adventure_created.reply_text(update, params=adv_id)
            
            return State.END
