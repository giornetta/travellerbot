from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from keyboards.keyboards import Keyboard

idle = Keyboard('Do you want to do something?',
                reply_markup=ReplyKeyboardMarkup([
                    ['Info', 'Inventory', 'Map']
                ], one_time_keyboard=False))

info = Keyboard('About what?',
                reply_markup=ReplyKeyboardMarkup([
                    ['World', 'Adventure', 'Myself']
                ], one_time_keyboard=True))

inventory = Keyboard('Do you want to use/throw an item?',
                     reply_markup=ReplyKeyboardMarkup([
                         ['Item1', 'Item2', '...', 'Nothing']
                     ], one_time_keyboard=True))

item = Keyboard('What do you want to do?',
                reply_markup=ReplyKeyboardMarkup([
                    ['Use', 'Throw', 'Nothing']
                ], one_time_keyboard=True))

item_error = Keyboard('No such item in your inventory')
throw = Keyboard('Item thrown')
use = Keyboard('Item used')
