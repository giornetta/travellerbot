from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, ConversationHandler


COMBAT = 1

class CombatConversation:
    def handlers(self) -> List[ConversationHandler]:
        return [ConversationHandler(
            entry_points=[CallbackQueryHandler(self._handle_join)],
            states={
                COMBAT: [CallbackQueryHandler(self._handle_join)],
            },
            fallbacks=[],
            per_message=True,
        )]

    def _handle_join(self, update: Update, context: CallbackContext):
        update.callback_query.message.delete()

        update.effective_user.send_message(
            'Is this working?',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('Yeah!', callback_data='WORKED')]
            ])
        )

        return COMBAT