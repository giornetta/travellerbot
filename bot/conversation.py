from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackContext

from adventure_setup.service import AdventureSetupService
from cache.userdata import user_data, UserData
from character_creation.bot import CharacterCreationConversation
from character_creation.service import CharacterCreator
from adventure_setup.bot import SetupConversation
from bot.state import ConversationState
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

    user_id = update.message.from_user.id
    if not user_data.get(user_id):
        user_data[user_id] = UserData()

    return ConversationState.ADVENTURE_SETUP


def _handle_ref(update: Update, context: CallbackContext) -> ConversationState:
    update.message.reply_text(text='Executing command...')
    return ConversationState.REFEREE_IDLE
