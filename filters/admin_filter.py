from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import admins

class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        self.admin_id = message.from_user.id
        return True if self.admin_id in admins else False