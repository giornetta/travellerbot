import dotenv
import psycopg2
from telegram.ext import Updater, PicklePersistence

from cache import userdata
from bot.conversation import handler

from travellermap import api
from traveller import equipment


if __name__ == '__main__':
    config = dotenv.dotenv_values()

    # Load global data
    equipment.load_equipment(config['EQUIP_PATH'])
    api.load_map(config['MAP_PATH'])
    userdata.load_data(config['CACHE_PATH'])

    for k, v in userdata.user_data.items():
        print(str(k) + ': ' + v)

    conn = psycopg2.connect(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host='localhost',
        port=5432
    )

    updater = Updater(
        token=config['TELEGRAM_TOKEN'],
        persistence=PicklePersistence(filename=config['CONV_PATH']),
        use_context=True,
    )

    conversation = handler(conn)
    updater.dispatcher.add_handler(conversation)

    updater.start_polling()
    updater.idle()

    userdata.write_data(config['CACHE_PATH'])
