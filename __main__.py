import dotenv
import psycopg2
from telegram.ext import Updater, PicklePersistence

from cache import userdata
from adventure_setup.service import AdventureSetupService
from character_creation.service import CharacterCreator
from bot.conversation import handler

from travellermap import api
from traveller import equipment


if __name__ == '__main__':
    config = dotenv.dotenv_values()

    # Load global data
    equipment.load_equipment(config['EQUIP_PATH'])
    api.load_map(config['MAP_PATH'])
    userdata.load_data(config['CACHE_PATH'])

    conn = psycopg2.connect(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host='127.0.0.1',
        port=5432
    )

    updater = Updater(
        token=config['TELEGRAM_TOKEN'],
        persistence=PicklePersistence(filename=config['CONV_PATH']),
        use_context=False,
    )
    character_creator = CharacterCreator(conn)
    setup_controller = AdventureSetupService(conn)

    conversation = handler(setup_controller, character_creator)
    updater.dispatcher.add_handler(conversation)

    updater.start_polling()
    updater.idle()

    userdata.write_data(config['CACHE_PATH'])
