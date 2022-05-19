from telegram import ReplyKeyboardMarkup

from keyboards.keyboards import Keyboard

choice = Keyboard('Pick the equipment you want to buy',
                  reply_markup=ReplyKeyboardMarkup([
                      ['Item1', 'Item2', '...', 'Skip']
                  ]))  # TODO emoticon

error_item = Keyboard('No such item exists')

ask = Keyboard('Do you want to buy something else?',
               reply_markup=ReplyKeyboardMarkup([
                   ['Yes', 'No']
               ]))

end = Keyboard('⚔ Are you ready to start your adventure?',
                    reply_markup=ReplyKeyboardMarkup([
                        ['Yes!', 'Of course!', 'Sure!']
                    ], one_time_keyboard=True))