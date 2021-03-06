from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup

from keyboards.keyboards import Keyboard

scene_already_exists = Keyboard('ā You already created a scene with that name, choose another one.')

end = Keyboard('ā Scene created correctly')

next_npc = Keyboard('š§āš Do you want to add an NPC?',
                    reply_markup=ReplyKeyboardMarkup([
                        ['Add', 'End']
                    ], one_time_keyboard=True))

ch_gen = Keyboard('āØ How do you want to generate characteristics?',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Manually', 'Random']
                  ], one_time_keyboard=True))

ch_manual_gen = Keyboard('āØ Insert the stats separated by spaces: STR DEX END INT EDU SOC. *(They must be >= 1)*',
                         reply_markup=ReplyKeyboardRemove())

invalid_stats = Keyboard('ā Invalid stats, please retry!')

ch_random_gen = Keyboard('Are these okay?\nšŖ *STR*: %s\nš *END*: %s\nš”ļø *DEX*: %s\nš§  *INT*: %s\nš *EDU*: %s\nš *SOC*: %s',
                         reply_markup=ReplyKeyboardMarkup([
                             ['Accept', 'Generate Again', 'Let me choose']
                         ], one_time_keyboard=True))

career = Keyboard('šØ What\'s their career?',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Agent', 'Barbarian', '...']
                  ], one_time_keyboard=True))

rank = Keyboard('ā¬ļø What\'s their rank?',
                reply_markup=ReplyKeyboardMarkup([
                    ['1', '2', '3'], ['4', '5', '6'], ['0']
                ], one_time_keyboard=True))

armor = Keyboard('š¦ŗ Pick an armor:',
                 reply_markup=ReplyKeyboardMarkup([
                     ['A1', 'A2', '...']
                 ], one_time_keyboard=True))

weapon = Keyboard('āļø Pick a weapon:',
                  reply_markup=ReplyKeyboardMarkup([
                      ['W1', 'W2', '...']
                  ], one_time_keyboard=True))

name = Keyboard('š What\'s their name?',
                reply_markup=ReplyKeyboardRemove())

name_too_long = Keyboard('ā That name is too long, sorry. Retry.')

ally = Keyboard('š¢ Are they an ally or an enemy?',
                reply_markup=ReplyKeyboardMarkup([
                    ['Ally', 'Enemy']
                ], one_time_keyboard=True))
