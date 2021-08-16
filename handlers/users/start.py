

from aiogram import types
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from keyboards.default import start_button, language_buttons
from loader import dp, db
from middlewares.internationlization import _
import mysql.connector

@dp.message_handler(text=['/start', _('Продолжить 🏳')])
async def bot_start(message: types.Message):
    try:
        language = db.select_user_language(message.from_user.id)
    except:
        print('Не удалось подключиться к бд')
        language = None
    if language is not None:
        smile = '\U0001F92B'
        paragraf = '\n'
        await message.answer(text=_("Привет, {name}! Я помогу тебе инвестировать {smile} {paragraf} /help - Получить справку", locale=language[0]).format(name = message.from_user.full_name, smile=smile, paragraf=paragraf), reply_markup=start_button)
    else:
        await message.answer(text=_('Выберите язык'), reply_markup=language_buttons)

@dp.message_handler(text=_("Изменить язык ✍️"))
async def chose_language(message: types.Message):
    await message.answer(text=_('Выберите язык'), reply_markup=language_buttons)

@dp.message_handler(text=['Русский 🇷🇺', 'Українська 🇺🇦', 'English 🇺🇸'])
async def enter_language(message: types.Message):
    if message.text == 'Русский 🇷🇺':
        user_language = 'ru'
    elif message.text == 'Українська 🇺🇦':
        user_language = 'uk'
    else: 
        user_language = 'en'
    try:
        db.add_user(first_name=str(message.from_user.first_name), 
                last_name=str(message.from_user.last_name),
                user_name=str(message.from_user.username),
                id=int(message.from_user.id),
                user_language=str(user_language))
    except mysql.connector.errors.IntegrityError:
        db.update_user_language(id=message.from_user.id, language=user_language)
    await message.answer(_('Вы выбрали русский язык, для продолжения нажмите сюда:\n/start', locale=user_language), reply_markup=ReplyKeyboardRemove())
