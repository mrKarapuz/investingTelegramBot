from aiogram.types import ReplyKeyboardMarkup
from aiogram.types.reply_keyboard import KeyboardButton
from middlewares.internationlization import _

start_button = ReplyKeyboardMarkup(
    keyboard=[
         [
             KeyboardButton(text=_('Информация о компании 🤓'))
         ],
         [
             KeyboardButton(text=_('Сравнить компании 🧐'))
         ],
         [
             KeyboardButton(text=_('Изменить язык ✍️'))
         ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

cancel_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_('Назад \U0001F448'))
        ]
    ],
    resize_keyboard=True
)

language_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Русский 🇷🇺')
        ],
        [
            KeyboardButton(text='Українська 🇺🇦')
        ],
        [
            KeyboardButton(text='English 🇺🇸')
        ]
    ],
    resize_keyboard=True
)

language_buttons_continue = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_('Продолжить 🏳'))
        ],
        [
            KeyboardButton(text=_('Изменить язык ✍️'))
        ]
    ],
    resize_keyboard=True
)