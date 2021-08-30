import logging
from aiogram import Dispatcher
from data.config import admins

async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот Запущен и готов к работе \n/update_basa - Обновить базу данных\n/select_users - Показать всех пользователей")
        except Exception as err:
            logging.exception(err)
