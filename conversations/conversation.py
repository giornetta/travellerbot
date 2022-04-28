from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackContext, Filters

from adventure_setup.service import AdventureSetupService
from character_creation.bot import CharacterCreationConversation
from character_creation.service import CharacterCreator
from conversations.adventure_setup import SetupConversation
from conversations.state import ConversationState
from keyboards import keyboards


def handler(setup_controller: AdventureSetupService, character_creator: CharacterCreator):
    return ConversationHandler(
        entry_points=[CommandHandler('start', _handle_start)],
        states={
            ConversationState.ADVENTURE_SETUP: SetupConversation(setup_controller, character_creator).handlers(),
            ConversationState.REFEREE_IDLE: [MessageHandler(Filters.text, _handle_ref)],
            ConversationState.CHARACTER_CREATION: CharacterCreationConversation(character_creator).handlers()
        },
        fallbacks=[],
        name='conversation',
        persistent=True
    )


def _handle_start(update: Update, context: CallbackContext) -> ConversationState:
    keyboards.welcome.reply_text(update)
    return ConversationState.ADVENTURE_SETUP


def _handle_ref(update: Update, context: CallbackContext) -> ConversationState:
    update.message.reply_text(text='Executing command...')
    return ConversationState.REFEREE_IDLE

