from aiogram import Dispatcher
from loader import dp
from .admin_filter import IsAdmin

dp.filters_factory.bind(IsAdmin)


def setup(dp: Dispatcher):
    pass
