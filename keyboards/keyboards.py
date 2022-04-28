import json
from typing import Optional, Callable, Tuple, List
from telegram import ReplyKeyboardMarkup, ReplyMarkup, Update, ReplyKeyboardRemove


class Keyboard:
    text: str
    reply_markup: Optional[ReplyMarkup]

    def __init__(self, text: str, reply_markup: Optional[ReplyMarkup] = None):
        self.text = text
        self.reply_markup = reply_markup

    def reply_text(self, update: Update, params: Optional[Tuple] = None, keys: Optional[List[List[str]]] = None):
        text = self.text % params if params else self.text
        reply_markup = ReplyKeyboardMarkup(keys, one_time_keyboard=True) if keys else self.reply_markup
        update.message.reply_text(self.text, reply_markup=self.reply_markup)

welcome = Keyboard(
    'Welcome to Traveller, do you want to create or join an Adventure?',
    reply_markup=ReplyKeyboardMarkup([
        ['Create', 'Join']
    ], one_time_keyboard=True)
)
