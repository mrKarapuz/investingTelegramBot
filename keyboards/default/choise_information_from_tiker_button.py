from aiogram.types import ReplyKeyboardMarkup
from aiogram.types.reply_keyboard import KeyboardButton
from middlewares.internationlization import _

choise = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_('Прибыль(год) 🍬')),
            KeyboardButton(text=_('Прибыль(квартал) 🍭')),
        ],
         [
            KeyboardButton(text=_('Баланс(год) 💰')),
            KeyboardButton(text=_('Баланс(квартал) \U0001F4B8')),
        ],
        [
            KeyboardButton(text=_('Дивиденды 💵')),
            KeyboardButton(text=_('Сплиты ✂')),
            KeyboardButton(text=_('Описание \U0000270F')),
        ],
        [
            KeyboardButton(text=_('Назад \U0001F448')),
        ]
    ],
    resize_keyboard=True 
)
