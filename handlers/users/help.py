from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit
from middlewares.internationlization import _


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer(text=_('/start - Начать диалог\n/help - Получить справку\nИнформация о компании: Введите тикер и получите базовую информацию о компании, также, нажав нужную кнопку, можно узнать подробную информацию по нужному критерию\n\nСравнить компании: Выберите признак сравнения, введите тикеры нужных компаний и получите наглядное стравнение\n\nОБНОВЛЕНИЯ ПРОИСХОДЯТ КАЖДЫЕ 10 мин\n\nВаши пожелания и предложения - https://t.me/mr_karapuz'))
