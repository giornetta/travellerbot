import telegram
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup

from keyboards.keyboards import Keyboard

# Join adventure

adv_code = Keyboard('✨ Perfect! What\'s the *code* of the Adventure you\'d like to join?', reply_markup=ReplyKeyboardRemove())

join_adventure = Keyboard('✅ Successfully joined Adventure _"%s"_!')

create_char = Keyboard('🧑‍🚀 You don\'t have any alive characters in this adventure, let\'s create one!')

invalid_code = Keyboard('❌ That code isn\'t valid, please try again.')

# Create adventure

title = Keyboard('📖 Choose a *title* for the adventure you want to create:', reply_markup=ReplyKeyboardRemove())

invalid_title = Keyboard('❌ That title isn\'t valid, please try again.')

sector = Keyboard(
    '🌌 Do you want to choose a starting *Sector* or generate one randomly?',
    reply_markup=ReplyKeyboardMarkup([
        ['Let me choose', 'Generate Random']
    ], one_time_keyboard=True))

sector_name = Keyboard('🌌 What\'s the name of the *Sector*?', reply_markup=ReplyKeyboardRemove())

confirm_sector = Keyboard('🌌 Will the starting *Sector* be _%s_?',
                          reply_markup=ReplyKeyboardMarkup([
                              ['Accept', 'Generate another', 'Let me choose']
                          ], one_time_keyboard=True))

no_sector = Keyboard('❌ That sector doesn\'t exist in this universe!',
                     reply_markup=ReplyKeyboardMarkup([
                         ['Choose another', 'Generate Random']
                     ], one_time_keyboard=True))

world = Keyboard('🪐 Do you want to choose a starting *World* or generate one randomly?',
                 reply_markup=ReplyKeyboardMarkup([
                     ['Let me choose', 'Generate Random']
                 ], one_time_keyboard=True))

world_name = Keyboard('🪐 What\'s the name of the *World*?', reply_markup=ReplyKeyboardRemove())

confirm_world = Keyboard('🪐 Will the starting *World* be _%s_?',
                         reply_markup=ReplyKeyboardMarkup([
                             ['Accept', 'Generate another', 'Let me choose']
                         ], one_time_keyboard=True))

no_world = Keyboard('❌ There\'s no such world in this sector!',
                    reply_markup=ReplyKeyboardMarkup([
                        ['Choose another', 'Generate Random']
                    ], one_time_keyboard=True))

terms = Keyboard('🔨 How many *terms* will the adventurers spend working before having to retire? '
                 '_(Default is 7, Infinite is any negative number)_',
                 reply_markup=ReplyKeyboardRemove())

invalid_choice = Keyboard('❌ That\'s not a valid number, retry!')

survival_roll = Keyboard('💀 When a *Survival Check* is failed, will the adventurers instantly die?',
                         reply_markup=ReplyKeyboardMarkup([
                             ['Yes', 'No']
                         ], one_time_keyboard=True))

adventure_created = Keyboard('✅ Successfully created Adventure <b><code>%s</code></b>! '
                             'Share this code with your friends to let them join! ',
                             reply_markup=ReplyKeyboardRemove(), parse_mode=telegram.ParseMode.HTML)
