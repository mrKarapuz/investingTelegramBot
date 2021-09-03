from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from middlewares.internationlization import _




xls_select_company = InlineKeyboardMarkup(row_width=1,
inline_keyboard=[
    [InlineKeyboardButton(
        text=_('Загрузить EXCEL таблицу ⬇'),
        callback_data='download_table',)
    ],
    [InlineKeyboardButton(
        text=_('Главная страница ↩'),
        callback_data='main_table',)
    ],
])

inline_cancel_button = InlineKeyboardMarkup(row_width=1,
inline_keyboard=[
    [InlineKeyboardButton(
            text=_('Назад \U0001F448'),
            callback_data='cancel')
    ],

])