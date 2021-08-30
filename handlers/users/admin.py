from aiogram import types
from loader import dp, db
from filters import IsAdmin
from aiogram.dispatcher.filters import Command
from tiker.functions_tiker import GeneraInformationOfCompany

@dp.message_handler(Command('admin'), IsAdmin())
async def update_basa(message: types.Message):
    await message.answer(text='/update_basa - Обновить базу данных\n/select_users - Показать всех пользователей')

@dp.message_handler(Command('select_users'), IsAdmin())
async def start_admin(message: types.Message):
    await message.answer(text='Все пользователи: \n')
    text = ''
    for elem in db.select_all_users():
        for e in elem:
            text += str(e) + ', '
        text += '\n'
    await message.answer(text = text)

@dp.message_handler(Command('update_basa'), IsAdmin())
async def update_basa(message: types.Message):
    await message.answer(text='Обновление базы данных...\nhttps://colt.cityhost.com.ua/phpmyadmin/index.php?route=/sql&server=1&db=chd11fa3e1_konov&table=companies&pos=0\nhttps://v2.d-f.pw/app/application/2005')
    text = db.add_tickers(GeneraInformationOfCompany)
    await message.answer(text=text)