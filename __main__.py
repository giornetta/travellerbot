import dotenv
import psycopg2
from telegram.ext import Updater, PicklePersistence

from adventure_setup.service import SetupController
from character_creation.service import CharacterCreator
from conversations.conversation import handler

from travellermap.api import TravellerMap
import traveller.equipment as equipment

JOINING_ADVENTURE, CREATING_ADVENTURE = map(chr, range(2))

if __name__ == '__main__':
    equipment.load_equipment('data/equipment.json')
    api = TravellerMap('data/map.json')

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
        use_context=True,
        persistence=PicklePersistence(filename='data/conversations.pickle')
    )
    dispatcher = updater.dispatcher

    character_creator = CharacterCreator(conn, api)
    setup_controller = SetupController(conn, character_creator)

    conversation = handler(setup_controller, character_creator, api)
    dispatcher.add_handler(conversation)

    updater.start_polling()
    updater.idle()