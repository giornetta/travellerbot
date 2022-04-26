import dotenv
import psycopg2
from telegram.ext import Updater, PicklePersistence

from adventure_setup.controller import SetupController
from conversations.conversation import handler

from travellermap.api import TravellerMap

JOINING_ADVENTURE, CREATING_ADVENTURE = map(chr, range(2))

if __name__ == '__main__':
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

    conversation = handler(SetupController(conn), api)
    dispatcher.add_handler(conversation)

    updater.start_polling()
    updater.idle()