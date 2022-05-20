from psycopg2.extensions import connection
from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, CallbackContext

from adventure_setup.service import AdventureSetupService
from cache.userdata import user_data, UserData
from character_creation.bot import CharacterCreationConversation
from player_idle.bot import PlayerIdleConversation
from player_idle.service import PlayerIdle
from character_creation.service import CharacterCreator
from adventure_setup.bot import SetupConversation
from bot.state import ConversationState
from keyboards import keyboards
from referee.bot import RefereeCommandsConversation
from referee.referee_commands import RefereeCommands
from referee.scene_creation.bot import SceneCreationConversation
from referee.scene_creation.service import SceneCreationService


def handler(conn: connection):

    character_creator = CharacterCreator(conn)
    setup_controller = AdventureSetupService(conn)

    referee_commands = RefereeCommands(conn)
    scene_creator = SceneCreationService(conn)

    player_idle = PlayerIdle(conn)

    return ConversationHandler(
        entry_points=[CommandHandler('start', _handle_start)],
        states={
            ConversationState.ADVENTURE_SETUP: SetupConversation(setup_controller, character_creator).handlers(),
            ConversationState.REFEREE_IDLE: RefereeCommandsConversation(referee_commands, scene_creator).handlers(),
            ConversationState.CHARACTER_CREATION: CharacterCreationConversation(character_creator).handlers(),
            ConversationState.SCENE_CREATION: SceneCreationConversation(conn).handlers(),
            ConversationState.PLAYER_IDLE: PlayerIdleConversation(player_idle).handlers(),
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
