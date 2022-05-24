from telegram import ReplyKeyboardMarkup

from keyboards.keyboards import Keyboard

ask_cat = choice = Keyboard('✨ What category of equipment do you want to buy?',
                            reply_markup=ReplyKeyboardMarkup([
                                ['Cat1', 'Cat2', '...', 'Skip']
                            ]))  # TODO emoticon

ask_item = Keyboard('✨ What equipment do you want to buy?',
                    reply_markup=ReplyKeyboardMarkup([
                        ['Item1', 'Item2', '...', 'Skip']
                    ]))  # TODO emoticon

success = Keyboard('💰 Deal! You now have %sCr!')  # TODO emoticon

no_money = Keyboard('❌ You don\'t have enough money to buy that!')

error_item = Keyboard('❌ Invalid item, please try again.')

error_cat = Keyboard('❌ Invalid category, please try again.')

ask = Keyboard('💰 Do you want to buy something else?',
               reply_markup=ReplyKeyboardMarkup([
                   ['Yes', 'No']
               ]))

error_shop = Keyboard('❌ The shop is closed now!')
