from typing import Optional, Tuple, List

import telegram
from telegram import ReplyKeyboardMarkup, ReplyMarkup, Update


class Keyboard:
    text: str
    reply_markup: Optional[ReplyMarkup]
    parse_mode: Optional[str]

    def __init__(self, text: str, reply_markup: Optional[ReplyMarkup] = None, parse_mode: Optional[str] = None):
        self.text = text
        self.reply_markup = reply_markup
        self.parse_mode = parse_mode

    def reply_text(self, update: Update, params: Optional[Tuple] = None, keys: Optional[List[List[str]]] = None):
        text = self.text % params if params else self.text
        reply_markup = ReplyKeyboardMarkup(keys, one_time_keyboard=True) if keys else self.reply_markup
        update.message.reply_text(text, reply_markup=reply_markup, parse_mode=self.parse_mode)


welcome = Keyboard(
    '🚀 Welcome to Traveller! Do you want to *create* or *join* an Adventure?',
    reply_markup=ReplyKeyboardMarkup([
        ['Create', 'Join']
    ], one_time_keyboard=True),
    parse_mode=telegram.ParseMode.MARKDOWN
)
