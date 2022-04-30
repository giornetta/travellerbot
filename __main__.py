import dotenv
import psycopg2
from telegram.ext import Updater, PicklePersistence, ContextTypes

from adventure_setup.service import AdventureSetupService
from bot.context import Context, UserData
from character_creation.service import CharacterCreator
from bot.conversation import handler

from travellermap import api
import traveller.equipment as equipment

JOINING_ADVENTURE, CREATING_ADVENTURE = map(chr, range(2))

if __name__ == '__main__':
    # Load global data
    equipment.load_equipment('data/equipment.json')
    api.load_map('data/map.json')

    config = dotenv.dotenv_values()

    conn = psycopg2.connect(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host='127.0.0.1',
        port=5432
    )

    updater = Updater(
        token=config['TELEGRAM_TOKEN'],
        # use_context=True,
        persistence=PicklePersistence(filename='data/conversations.pickle'),
        context_types=ContextTypes(context=Context, user_data=UserData)
    )
    dispatcher = updater.dispatcher

    character_creator = CharacterCreator(conn)
    setup_controller = AdventureSetupService(conn)

    conversation = handler(setup_controller, character_creator)
    dispatcher.add_handler(conversation)

    updater.start_polling()
    updater.idle()
