from telegram import ReplyKeyboardMarkup

from keyboards.keyboards import Keyboard

idle = Keyboard('📝 Do you want to do something?',
                reply_markup=ReplyKeyboardMarkup([
                    ['Info'], ['Inventory'], ['Map'], ['Skill Check'], ['Shop'], ['Exit']
                ], one_time_keyboard=False))

info = Keyboard('📝 About what?',
                reply_markup=ReplyKeyboardMarkup([
                    ['World', 'Adventure', 'Scenes', 'Myself']
                ], one_time_keyboard=True))

inventory = Keyboard('🔨 Do you want to use/throw an item?',
                     reply_markup=ReplyKeyboardMarkup([
                         ['Item1', 'Item2', '...', 'Nothing']
                     ], one_time_keyboard=True))

item = Keyboard('🔨 What do you want to do?',
                reply_markup=ReplyKeyboardMarkup([
                    ['Use', 'Throw', 'Nothing']
                ], one_time_keyboard=True))

item_error = Keyboard('❌ No such item in your inventory')
throw = Keyboard('❌ Item thrown')
use = Keyboard('🔨 Item used')

skill_check = Keyboard('✨ Which *Skill* do you want to roll on?')

difficulty = Keyboard('How difficult will the roll be?', reply_markup=ReplyKeyboardMarkup([
    ['Simple', 'Easy', 'Routine'],
    ['Average', 'Difficult'],
    ['Very Difficult', 'Formidable']
], one_time_keyboard=True))

skill_check_success = Keyboard('✅ *%s*! %s!')

skill_check_fail = Keyboard('❌ *%s*! %s!')

ask_shop = Keyboard('💰 Do you want to buy something?',
                    reply_markup=ReplyKeyboardMarkup([
                        ['Yes'], ['No']
                    ]))
