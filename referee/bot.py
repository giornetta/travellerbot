
from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler

from referee.referee_commands import RefereeCommands
from traveller.world import *


class RefereeCommandsConversation:
    service: RefereeCommands

    def __init__(self, service: RefereeCommands):
        self.service = service

    def handlers(self) -> List[ConversationHandler]:
        return [ConversationHandler(
            entry_points=[
                CommandHandler('info', self._handle_info),
                CommandHandler('set', self._handle_command),
                CommandHandler('shop', self._handle_command),
                CommandHandler('rest', self._handle_command),
                CommandHandler('combat', self._handle_command),
                CommandHandler('travel', self._handle_command),
                CommandHandler('age', self._handle_command),
                CommandHandler('scene', self._handle_command),
                CommandHandler('exit', self._handle_command)
            ],
            states={},
            fallbacks=[]
        )]

    def _handle_command(self, update: Update, context: CallbackContext):
        check, text = self.service.cp.execute(update.message.text, update.message.from_user.id)
        update.message.reply_text(text)

    def _handle_info(self, update: Update, context: CallbackContext):
        check, text = self.service.cp.execute(update.message.text, update.message.from_user.id)
        if text[:4] == 'http':
            update.message.reply_photo(text)
        else:
            update.message.reply_text(text)
