from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackContext, Filters

from adventure_setup.controller import SetupController
from conversations.adventure_setup import SetupConversation
from conversations.state import ConversationState
from keyboards import keyboards
from travellermap.api import TravellerMap


def handler(setup_controller: SetupController, traveller_map: TravellerMap):
    return ConversationHandler(
        entry_points=[CommandHandler('start', _handle_start)],
        states={
            ConversationState.ADVENTURE_SETUP: SetupConversation(setup_controller, traveller_map).handlers(),
            ConversationState.CHARACTER_CREATION: [MessageHandler(Filters.text, _handle_name)]
        },
        fallbacks=[],
        name='conversation',
        persistent=True
    )


def _handle_start(update: Update, context: CallbackContext) -> ConversationState:
    keyboards.welcome.reply_text(update)
    return ConversationState.ADVENTURE_SETUP


def _handle_name(update: Update, context: CallbackContext) -> ConversationState:
    keyboards.name.reply_text(update)

    return ConversationState.CHARACTER_CREATION
