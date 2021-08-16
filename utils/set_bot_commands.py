from aiogram import types
from middlewares.internationlization import _

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", _("Начать диалог")),
        types.BotCommand("help", _("Помощь")),
    ])
