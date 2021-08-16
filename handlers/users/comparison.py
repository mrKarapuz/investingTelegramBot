from loader import dp 
from aiogram import types
from keyboards.inline.choise_comparison import choise_inline_comparison
from keyboards.default import start_button, cancel_button
from tiker.functions_tiker import GeneraInformationOfCompany
from aiogram.dispatcher.storage import FSMContext
from states.states_comparison import Comparison
from middlewares.internationlization import _

sings = {
    'sector_of_company': _('Сектор'),
    'isin_of_company': _('МИН ценных бумаг'),
    'market_cap_of_company': _('Капитализация'),
    'count_shares_ofustanding_of_company': _('Количество акций'),
    'current_prise_share_now_of_company': _('Цена акции'),
    'profit_of_company_now': _('Общий доход'),
    'net_profit_of_company_now' : _('Чистая прибыль'),
    'total_assets_now': _('Активы'),
    'total_liab_now': _('Обязательства'),
    'dividends_of_company_now_per_year_in_dollar': _('Дивиденды в долларах'),
    'dividends_of_company_now_per_year_in_persent': _('Дивиденды в процентах'),
    'eps_of_company': _('Прибыль на акцию'),
    'pe_ratio_of_company': _('Цена\прибыль'),
}

@dp.callback_query_handler(text='cancel', state=[Comparison.enter_the_tickers, Comparison.enter_the_attribute])
async def cancel_operation(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(text=_('Отмена'), reply_markup=start_button)
    await state.finish()

@dp.message_handler(text=_('Назад \U0001F448'), state=[Comparison.enter_the_tickers, Comparison.enter_the_attribute])
async def cancel_operation(message: types.Message, state: FSMContext):
    await message.answer(text=_('Отмена'), reply_markup=start_button)
    await state.finish()

@dp.message_handler(text=_('Сравнить компании 🧐'))
async def enter_the_attribute(message: types.Message):
    await message.answer(text=_('По какому признаку сравнивать?'), reply_markup=choise_inline_comparison)
    await Comparison.enter_the_attribute.set()

@dp.callback_query_handler(state=Comparison.enter_the_attribute)
async def enter_the_tickers(call: types.CallbackQuery, state: FSMContext):
    global attribute_of_comparison, msg_id
    attribute_of_comparison = call.data
    await call.message.edit_reply_markup()
    await state.update_data(attribute = call.data)
    await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    msg = await call.message.answer(text=_('Выбранный атрибут: "{attr}" \nВведите тикеры компаний через пробел (в любом регистре)').format(attr=str(sings[attribute_of_comparison])), reply_markup=cancel_button)
    msg_id = msg.message_id
    await Comparison.enter_the_tickers.set()

@dp.message_handler(state=Comparison.enter_the_tickers)
async def enter_the_comparison(message: types.Message, state: FSMContext):
    await state.update_data(tickers = message.text)
    data = await state.get_data()
    attribute = data.get('attribute')
    tickers = data.get('tickers')
    errors_ticker = ''
    answer_user = _('Сравнение компаний по признаку: "{attr}"').format(attr=str(sings[attribute_of_comparison])) + '\n' 
    await dp.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    msg = await message.answer(text=_('Сбор информации...\nМожет продолжаться до 30 секунд'))
    for ticker in tickers.split(' '):
        ticker = str(ticker).upper()
        try:
            information_comparison = GeneraInformationOfCompany(ticker).__getattribute__(attribute)
        except KeyError:
            errors_ticker += ticker + ', '
            continue
        answer_user += ticker + ': ' + str(information_comparison) + '\n'
    await dp.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    await message.answer(text=answer_user, reply_markup=start_button)
    if len(errors_ticker) != 0:
        await message.answer(text=_('Ошибка, данных тикеров не существует: {errors_ticker}').format(errors_ticker=errors_ticker))
    await state.finish()
    