from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup

from keyboards.keyboards import Keyboard

scene_name = Keyboard('What\'s the name of the scene')

next_npc = Keyboard('Do you want to add an NPC?',
                    reply_markup=ReplyKeyboardMarkup([
                        ['Add', 'End']
                    ], one_time_keyboard=True))

ch_gen = Keyboard('How do you want to generate characteristics?',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Manually', 'Random']
                  ], one_time_keyboard=True))

ch_manual_gen = Keyboard('Insert the stats separated by spaces: STR DEX END INT EDU SOC.',
                         reply_markup=ReplyKeyboardRemove())

ch_random_gen = Keyboard('%s %s %s %s %s %s?',
                         reply_markup=ReplyKeyboardMarkup([
                             ['Accept', 'Generate Again', 'Let me choose']
                         ], one_time_keyboard=True))

career = Keyboard('What career did they take?',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Agent', 'Barbarian', '...']
                  ], one_time_keyboard=True))

rank = Keyboard('What\'s their rank?',
                reply_markup=ReplyKeyboardMarkup([
                    ['1', '2', '...']
                ], one_time_keyboard=True))

armor = Keyboard('Pick an armor:',
                 reply_markup=ReplyKeyboardMarkup([
                     ['A1', 'A2', '...']
                 ], one_time_keyboard=True))

weapon = Keyboard('Pick a weapon:',
                  reply_markup=ReplyKeyboardMarkup([
                      ['W1', 'W2', '...']
                  ], one_time_keyboard=True))

name = Keyboard('What\'s their name?',
                reply_markup=ReplyKeyboardRemove())

ally = Keyboard('Are they an ally or an enemy:',
                reply_markup=ReplyKeyboardMarkup([
                    ['Ally', 'Enemy']
                ], one_time_keyboard=True))
