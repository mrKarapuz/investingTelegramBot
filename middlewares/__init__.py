from re import L
from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .internationlization import i18n

def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(i18n)