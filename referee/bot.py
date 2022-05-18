import telegram
from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler

from bot.state import ConversationState
from referee.referee_commands import RefereeCommands
from traveller.world import *


class State(Enum):
    COMMANDS = 0
    SCENE = 1


class RefereeCommandsConversation:
    service: RefereeCommands

    def __init__(self, service: RefereeCommands):
        self.service = service

    def handlers(self) -> List[ConversationHandler]:
        commands = [
            CommandHandler('info', self._handle_info),
            CommandHandler('set', self._handle_command),
            CommandHandler('shop', self._handle_command),
            CommandHandler('rest', self._handle_command),
            CommandHandler('combat', self._handle_command),
            CommandHandler('travel', self._handle_command),
            CommandHandler('age', self._handle_command),
            CommandHandler('scene', self._handle_scene),
            CommandHandler('exit', self._handle_command)
        ]
        return [ConversationHandler(
            entry_points=commands,
            states={
                State.COMMANDS: commands
            },
            map_to_parent={
                State.SCENE: ConversationState.SCENE_CREATION
            },
            fallbacks=[]
        )]

    def _handle_command(self, update: Update, context: CallbackContext) -> State:
        check, text = self.service.cp.execute(update.message.text, update.message.from_user.id)
        update.message.reply_text(text, parse_mode=telegram.ParseMode.MARKDOWN)
        return State.COMMANDS

    def _handle_info(self, update: Update, context: CallbackContext) -> State:
        check, text = self.service.cp.execute(update.message.text, update.message.from_user.id)
        if text[:4] == 'http':
            update.message.reply_photo(text)
        else:
            update.message.reply_text(text, parse_mode=telegram.ParseMode.HTML)
        return State.COMMANDS

    def _handle_scene(self, update: Update, context: CallbackContext) -> State:
        is_new = update.message.text.split(' ', 2)[1]
        if is_new == 'new':
            check, text = self.service.cp.execute(update.message.text, update.message.from_user.id)
            update.message.reply_text(text)
            return State.SCENE
        check, text = self.service.cp.execute(update.message.text, update.message.from_user.id)
        update.message.reply_text(text)
        return State.COMMANDS
