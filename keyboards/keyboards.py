import json
from typing import Optional, Callable, Tuple
from telegram import ReplyKeyboardMarkup, ReplyMarkup, Update, ReplyKeyboardRemove


class Keyboard:
    text: str
    reply_markup: Optional[ReplyMarkup]

    def __init__(self, text: str, reply_markup: Optional[ReplyMarkup] = None):
        self.text = text
        self.reply_markup = reply_markup

    def reply_text(self, update: Update):
        update.message.reply_text(self.text, reply_markup=self.reply_markup)


class FKeyboard(Keyboard):
    def reply_text(self, update: Update, param: Tuple):
        update.message.reply_text(self.text % param, reply_markup=self.reply_markup, )


welcome = Keyboard(
    'Welcome to Traveller, do you want to create or join an Adventure?',
    reply_markup=ReplyKeyboardMarkup([
        ['Create', 'Join']
    ], one_time_keyboard=True)
)
