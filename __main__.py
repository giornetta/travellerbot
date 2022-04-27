import dotenv
from telegram.ext import Updater, PicklePersistence

from adventure_setup.controller import SetupController
from conversations.conversation import handler

from travellermap.api import TravellerMap
import traveller.equipment as equipment

JOINING_ADVENTURE, CREATING_ADVENTURE = map(chr, range(2))

if __name__ == '__main__':
    equipment.load_equipment()
    api = TravellerMap('data/map.json')

    config = dotenv.dotenv_values()

    updater = Updater(
        token=config['TELEGRAM_TOKEN'],
        use_context=True,
        persistence=PicklePersistence(filename='data/conversations.pickle')
    )
    dispatcher = updater.dispatcher

    conversation = handler(SetupController(), api)
    dispatcher.add_handler(conversation)

    updater.start_polling()
    updater.idle()

    api.write_data()
