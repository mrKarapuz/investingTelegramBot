from loader import dp
from aiogram import types
from keyboards.default import start_button, cancel_button
from keyboards.default import choise
from googletrans import Translator
from tiker.functions_tiker import *
from aiogram.dispatcher.storage import FSMContext
from states.states_information_from_ticker import InformationFromTicker
from middlewares.internationlization import _


@dp.message_handler(text=_('Информация о компании 🤓'))
async def enter_the_ticker(message: types.Message):
    await message.answer(text=_('Введите тикер: \U0001F3AB'), reply_markup=cancel_button)
    await InformationFromTicker.enter_the_ticker.set()

@dp.message_handler(text=_('Назад \U0001F448'), state=InformationFromTicker.enter_the_ticker)
async def cancel_operation(message: types.Message, state: FSMContext):
    await message.answer(text=_('Отмена'), reply_markup=start_button)
    await state.finish()

@dp.message_handler(text=_('Прибыль(год) 🍬'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    await message.answer(text=do_dict_revenue_and_earnings(ticker))
    

@dp.message_handler(text=_('Прибыль(квартал) 🍭'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    await message.answer(text=do_dict_quarterly_revenue_and_earnings(ticker))
    
@dp.message_handler(text=_('Баланс(год) 💰'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    await message.answer(text=do_dict_balance_sheet(ticker))

@dp.message_handler(text=_('Баланс(квартал) \U0001F4B8'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    await message.answer(text=do_dict_quarterly_balance_sheet(ticker))

@dp.message_handler(text=_('Дивиденды 💵'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    await message.answer(text=do_dict_history_dividends(ticker))

@dp.message_handler(text=_('Сплиты ✂'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    await message.answer(text=do_dict_history_splits(ticker))

@dp.message_handler(text=_('Описание \U0000270F'), state=InformationFromTicker.enter_the_ticker)
async def return_detalied_about_company(message: types.Message, state: FSMContext, locale):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    translator = Translator()
    english = GeneraInformationOfCompany(ticker).description_of_company
    if locale == 'en':
        anwser_user = english
    elif locale == 'uk':
        anwser_user = translator.translate(english, dest='uk').text
    else: 
        anwser_user = translator.translate(english, dest='ru').text
    await message.answer(text=anwser_user)

@dp.message_handler(text=_('Лого 🖼'), state=InformationFromTicker.enter_the_ticker)
async def return_logo_company(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    await dp.bot.send_photo(chat_id=message.chat.id, photo=GeneraInformationOfCompany(ticker).logo_url_of_company)

@dp.message_handler(state=InformationFromTicker.enter_the_ticker)
async def return_all_general_informaion(message: types.Message, state: FSMContext):
    msg = await message.answer(text=_('Пожалуйста, подождите...'))
    await state.update_data(ticker = message.text)
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    try:
        answer_user = GeneraInformationOfCompany(ticker).return_all_general_information()
        await dp.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        await message.answer(text=answer_user + '\n', disable_web_page_preview=True, reply_markup=choise)
    except KeyError:
        await message.answer(text=_('Ошибка, проверьте правильность тикера и попробуйте еще раз \nТикер — краткое название в биржевой информации котируемых инструментов: \nApple: AAPL\nGeneral Electric: GE'))
        return 0