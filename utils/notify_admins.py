import logging
from aiogram import Dispatcher
from keyboards.default import start_button
from data.config import admins

async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "/update_basa_nasdaq - Обновить базу данных NASDAQ\n/update_basa_dow_sp - Обновить базу данных DOW, SP\n/select_users - Показать всех пользователей')", reply_markup=start_button)
        except Exception as err:
            logging.exception(err)
