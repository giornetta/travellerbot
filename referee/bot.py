import telegram
from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler

from referee.referee_commands import RefereeCommands
from referee.scene_creation.bot import SceneCreationConversation
from referee.scene_creation.service import SceneCreationService
from referee.state import RefereeState
from traveller.world import *


class RefereeCommandsConversation:
    service: RefereeCommands
    scene_creator: SceneCreationService

    def __init__(self, commands: RefereeCommands, scene_creator: SceneCreationService):
        self.service = commands
        self.scene_creator = scene_creator

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
            CommandHandler('exit', self._handle_command),
            CommandHandler('starship', self._handle_command)
        ]

        return [ConversationHandler(
            entry_points=commands,
            states={
                RefereeState.COMMANDS: commands,
                RefereeState.SCENE: SceneCreationConversation(self.scene_creator).handlers()
            },
            fallbacks=[]
        )]

    def _handle_command(self, update: Update, context: CallbackContext) -> RefereeState:
        check, text = self.service.cp.execute(update.message.text, update.message.from_user.id)
        update.message.reply_text(text, parse_mode=telegram.ParseMode.MARKDOWN)
        return RefereeState.COMMANDS

    def _handle_info(self, update: Update, context: CallbackContext) -> RefereeState:
        check, text = self.service.cp.execute(update.message.text, update.message.from_user.id)
        if text[:4] == 'http':
            update.message.reply_photo(text)
        else:
            update.message.reply_text(text, parse_mode=telegram.ParseMode.HTML)
        return RefereeState.COMMANDS

    def _handle_scene(self, update: Update, context: CallbackContext) -> RefereeState:
        is_new = update.message.text.split(' ', 2)[1]
        if is_new == 'new':
            check, text = self.service.cp.execute(update.message.text, update.message.from_user.id)
            update.message.reply_text(text)
            return RefereeState.SCENE
        check, text = self.service.cp.execute(update.message.text, update.message.from_user.id)
        update.message.reply_text(text)
        return RefereeState.COMMANDS
