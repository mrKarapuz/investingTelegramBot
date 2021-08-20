from aiogram.types import InputFile
from loader import dp
from aiogram import types
from keyboards.default import start_button, cancel_button, choise
from keyboards.inline import choise_inline_date_for_stockprise
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
    msg = await message.answer(text=_('Формируем график...'))
    photopath = InputFile(show_revenue_and_earnings(ticker))
    await dp.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    await dp.bot.send_photo(chat_id=message.chat.id, photo=photopath)
    
@dp.message_handler(text=_('Прибыль(квартал) 🍭'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    msg = await message.answer(text=_('Формируем график...'))
    photopath = InputFile(show_quartal_revenue_and_earnings(ticker))
    await dp.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    await dp.bot.send_photo(chat_id=message.chat.id, photo=photopath)
    
@dp.message_handler(text=_('Баланс(год) 💰'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    msg = await message.answer(text=_('Формируем график...'))
    photopath = InputFile(show_balance_sheet(ticker))
    await dp.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    await dp.bot.send_photo(chat_id=message.chat.id, photo=photopath)

@dp.message_handler(text=_('Баланс(квартал) \U0001F4B8'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    msg = await message.answer(text=_('Формируем график...'))
    photopath = InputFile(show_quartal_balance_sheet(ticker))
    await dp.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    await dp.bot.send_photo(chat_id=message.chat.id, photo=photopath)

@dp.message_handler(text=_('Дивиденды 💵'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    msg = await message.answer(text=_('Пожалуйста подождите...'))
    data_from_func = show_history_dividends(ticker)
    photopath = False
    try:
        photopath = InputFile(data_from_func[0])
    except TypeError:
        pass
    await dp.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    await message.answer(text=data_from_func[1])
    if photopath:
        await dp.bot.send_photo(chat_id=message.chat.id, photo=photopath)
    
@dp.message_handler(text=_('Сплиты ✂'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    msg = await message.answer(text=_('Пожалуйста подождите...'))
    await message.answer(text=show_history_splits(ticker))
    await dp.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)

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

@dp.message_handler(text=_('График цены акции \U0001F4C8'), state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(message: types.Message, state: FSMContext):
    await message.answer(text=_('Выберите период'), reply_markup=choise_inline_date_for_stockprise)

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

@dp.callback_query_handler(state=InformationFromTicker.enter_the_ticker)
async def return_revenue_information(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    ticker = str(data.get('ticker')).upper()
    await call.answer(text=_('Формируем график...'))
    photopath = InputFile(show_comparison_history_prise(symbol=ticker, period=call.data))
    await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await dp.bot.send_photo(chat_id=call.message.chat.id, photo=photopath)