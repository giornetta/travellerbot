import os
import dotenv
import psycopg2
from telegram.ext import Updater, PicklePersistence

from cache import userdata
from bot.conversation import handler

from travellermap import api
from traveller import equipment


if __name__ == '__main__':
    dotenv.load_dotenv()

    # Load global data
    equipment.load_equipment(os.environ['EQUIP_PATH'])
    api.load_map(os.environ['MAP_PATH'])
    userdata.load_data(os.environ['CACHE_PATH'])

    print(f'{len(equipment.equipments)} items loaded!')
    print(f'{len(api.data)} sectors loaded!')

    print(f'Loaded cached user data for {len(userdata.user_data)} players!')

    conn = psycopg2.connect(os.environ['DATABASE_URL'])

    print('Successfully connected to Database!')

    updater = Updater(
        token=os.environ['TELEGRAM_TOKEN'],
        persistence=PicklePersistence(filename=os.environ['CONV_PATH']),
        use_context=True,
    )

    conversation = handler(conn)
    updater.dispatcher.add_handler(conversation)

    updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', '8443')),
        url_path=os.environ['TELEGRAM_TOKEN'],
        webhook_url='https://travellerbot.herokuapp.com/' + os.environ['TELEGRAM_TOKEN']
    )

    print('Bot started!')

    updater.idle()

    userdata.write_data(os.environ['CACHE_PATH'])
