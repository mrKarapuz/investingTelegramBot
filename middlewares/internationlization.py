
from pathlib import Path
from aiogram import types
from typing import Tuple, Any
from loader import db, dp
from aiogram.contrib.middlewares.i18n import I18nMiddleware

I18N_DOMAIN = 'mybot'
BASE_DIR = (Path(__file__).parent).parent
LOCALES_DIR = BASE_DIR / 'locales'

class Localization(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        user: types.User = types.User.get_current()
        *_, data = args
        if db.select_user_language(user.id) is None:
            language = data['locale'] = 'en'
        else: 
            language = data['locale'] = db.select_user_language(user.id)[0]
        return language

i18n = Localization(I18N_DOMAIN, LOCALES_DIR)
_ = i18n.lazy_gettext