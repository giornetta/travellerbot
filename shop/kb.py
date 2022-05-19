from telegram import ReplyKeyboardMarkup

from keyboards.keyboards import Keyboard

ask_cat = choice = Keyboard('What category of equipment do you want to buy',
                            reply_markup=ReplyKeyboardMarkup([
                                ['Cat1', 'Cat2', '...', 'Skip']
                            ]))  # TODO emoticon

ask_item = Keyboard('Pick the equipment you want to buy',
                    reply_markup=ReplyKeyboardMarkup([
                        ['Item1', 'Item2', '...', 'Skip']
                    ]))  # TODO emoticon

success = Keyboard('Successfully bought, your credits now are %s')  # TODO emoticon

no_money = Keyboard('Not enough money')

error_item = Keyboard('Invalid item')

error_cat = Keyboard('Invalid category')

ask = Keyboard('Do you want to buy something else?',
               reply_markup=ReplyKeyboardMarkup([
                   ['Yes', 'No']
               ]))

end = Keyboard('⚔ Are you ready to start your adventure?',
               reply_markup=ReplyKeyboardMarkup([
                   ['Yes!', 'Of course!', 'Sure!']
               ], one_time_keyboard=True))
