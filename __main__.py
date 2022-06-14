import os
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

    print(f'{len(equipment.equipments)} items loaded!')
    print(f'{len(api.data)} sectors loaded!')

    print(f'Loaded cached user data for {len(userdata.user_data)} players!')

    conn = psycopg2.connect(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host='localhost',
        port=5432
    )

    print('Successfully connected to Database!')

#    with open('schema.sql') as f:
#        conn.cursor().execute(f.read())

    updater = Updater(
        token=config['TELEGRAM_TOKEN'],
        persistence=PicklePersistence(filename=config['CONV_PATH']),
        use_context=True,
    )

    conversation = handler(conn)
    updater.dispatcher.add_handler(conversation)

    updater.start_webhook(listen="0.0.0.0", port=int(config['PORT']), url_path=config['TELEGRAM_TOKEN'])
    updater.bot.setWebhook('https://travellerbot.herokuapp.com/' + config['TELEGRAM_TOKEN'])

    print('Bot started!')

    updater.idle()

    userdata.write_data(config['CACHE_PATH'])
