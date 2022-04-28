from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup

from keyboards.keyboards import Keyboard

adv_code = Keyboard('What\'s the code of the Adventure you\'d like to join?',
                    reply_markup=ReplyKeyboardRemove())

join_adventure = Keyboard('Joined Adventure "%s"')

create_char = Keyboard('Let\'s create a Character for this Adventure, choose a name:')

invalid_code = Keyboard('The provided code isn\'t valid, try again."')

title = Keyboard('Choose a title for the adventure you want to create:',
                 reply_markup=ReplyKeyboardRemove())

sector = Keyboard(
    'Do you want to choose a starting Sector for the Adventurers or do you want to generate one randomly?',
    reply_markup=ReplyKeyboardMarkup([
        ['Let me choose', 'Generate Random']
    ], one_time_keyboard=True))

sector_name = Keyboard('What\'s the name of the Sector?',
                       reply_markup=ReplyKeyboardRemove())

world = Keyboard('Do you want to choose a starting World for the Adventurers or do you want to generate one '
                 'randomly?',
                 reply_markup=ReplyKeyboardMarkup([
                     ['Let me choose', 'Generate Random']
                 ], one_time_keyboard=True))

no_sector = Keyboard('No such sector exists in this universe.',
                     reply_markup=ReplyKeyboardMarkup([
                         ['Choose another', 'Generate Random']
                     ], one_time_keyboard=True))

confirm_sector = Keyboard('Will the adventure be set in "%s"?',
                          reply_markup=ReplyKeyboardMarkup([
                              ['Accept', 'Generate another', 'Let me choose']
                          ], one_time_keyboard=True))

world_name = Keyboard('What\'s the name of the World?',
                      reply_markup=ReplyKeyboardRemove())

terms = Keyboard('How many terms will the adventurers spend working before having to retire? '
                 '(Default is 7, Infinite is any negative number)',
                 reply_markup=ReplyKeyboardRemove())

no_world = Keyboard('No such world exists in this universe.',
                    reply_markup=ReplyKeyboardMarkup([
                        ['Choose another', 'Generate Random']
                    ], one_time_keyboard=True))

confirm_world = Keyboard('Will the adventure begin in "%s"?',
                         reply_markup=ReplyKeyboardMarkup([
                             ['Accept', 'Generate another', 'Let me choose']
                         ], one_time_keyboard=True))

survival_roll = Keyboard('When a Survival Check is failed, will the Adventurer die?',
                         reply_markup=ReplyKeyboardMarkup([
                             ['Yes', 'No']
                         ], one_time_keyboard=True))

invalid_choice = Keyboard('Invalid choice, retry.')
