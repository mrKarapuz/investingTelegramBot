from loader import dp 
from aiogram import types
from aiogram.types import InputFile
from keyboards.inline.choise_comparison import choise_inline_comparison, choise_inline_date_for_stockprise
from keyboards.default import start_button, cancel_button
from tiker.functions_tiker import GeneraInformationOfCompany, show_comparison_history_prise
from aiogram.dispatcher.storage import FSMContext
from states.states_comparison import Comparison
from middlewares.internationlization import _
from tiker.functions_tiker import number_conversion, formatOY
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, MaxNLocator
from matplotlib.gridspec import GridSpec
import yahoo_fin.stock_info as yfs

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
    'total_stockholder_equity_now': _('Акционерный капитал'),
    'dividends_of_company_now_per_year_in_dollar': _('Дивиденды в $ (квартал)'),
    'dividends_of_company_now_per_year_in_persent': _('Дивиденды в % (квартал)'),
    'eps_of_company': _('Прибыль на акцию'),
    'pe_ratio_of_company': _('Цена\прибыль'),
}

def return_comparison_graphics(x, y, attribute, answer_user, listx):
    if 30 > str(tickers).count(' ') > 15:
        fig = plt.figure(figsize=(8,8),facecolor='#e8e8e8')
    elif str(tickers).count(' ') > 30:
        fig = plt.figure(figsize=(8,12),facecolor='#e8e8e8') 
    else:
        fig = plt.figure(figsize=(8,4),facecolor='#e8e8e8')
    gs=GridSpec(ncols=9, nrows=1, figure=fig)
    x = np.array(listx)
    y = np.array(y)
    ax = fig.add_subplot(gs[0:8])
    ax.barh(x, y, label=_('Сравнение компаний по признаку: ') + sings[attribute])
    ax.xaxis.set_major_formatter(FuncFormatter(formatOY))
    ax.xaxis.set_major_locator(MaxNLocator(10))
    ax.legend(bbox_to_anchor=(0.95, 1.12))
    plt.figtext(0.85, 0.1, answer_user)
    plt.grid()
    save_dir = 'graphics/' + str(tickers)[:-10:-1] + attribute + '.png'
    fig.savefig(save_dir)
    return {'ansver_user' : answer_user, 'save_dir' : save_dir}

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
    await message.answer(text=_('Данные состоянием на утро сегодняшнего дня\nПо какому признаку сравнивать?'), reply_markup=choise_inline_comparison)
    await Comparison.enter_the_attribute.set()

@dp.callback_query_handler(state=Comparison.enter_the_attribute)
async def enter_the_tickers(call: types.CallbackQuery, state: FSMContext):
    global attribute_of_comparison, msg_id
    attribute_of_comparison = call.data
    await call.message.edit_reply_markup()
    await state.update_data(attribute = call.data)
    await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    msg = await call.message.answer(text=_('Выбранный атрибут: "{attr}" \nВведите тикеры компаний через пробел (в любом регистре)\nДля формирования наглядного сравнения выберите не более 50 (10 если сравниваете по цене акции) компаний').format(attr=str(sings[attribute_of_comparison])), reply_markup=cancel_button)
    msg_id = msg.message_id
    await Comparison.enter_the_tickers.set()

@dp.message_handler(state=Comparison.enter_the_tickers)
async def enter_the_comparison(message: types.Message, state: FSMContext):
    global tickers, xprise
    await state.update_data(tickers = message.text)
    data = await state.get_data()
    attribute = data.get('attribute')
    tickers = data.get('tickers')
    if str(tickers).count(' ') > 50:
        await message.answer(text=_('Для формирования наглядного сравнения выберите не более 50 компаний'))
    answer_user=''
    errors_ticker = ''
    await dp.bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    msg = await message.answer(text=_('Сбор информации...\nПроцесс может занять несколько минут'))
    x = []
    y = []
    if attribute == 'current_prise_share_now_of_company':
        xprise = []
        for elem in list(str(tickers).upper().split(' ')):
            try:
                prise = round(yfs.get_live_price(elem), 1)
                y.append(prise)
                xprise.append(elem)
                answer_user += elem + ': ' + str(prise) + '\n'
            except AssertionError:
                errors_ticker += elem + ', '
                continue
        result = return_comparison_graphics(x, y, attribute=attribute, answer_user=answer_user, listx=xprise)
        await dp.bot.send_photo(chat_id=message.chat.id, photo=InputFile(result['save_dir']), reply_markup=start_button)
        if str(tickers).count(' ') > 10:
            await message.answer(text=_('Для формирования наглядного графика выберите не более 10 компаний'))
        else:
            await message.answer(text=_('Выберите период для формирования графика изменения цены акции'), reply_markup=choise_inline_date_for_stockprise)
    elif attribute == 'sector_of_company' or attribute == 'isin_of_company':
        for ticker in tickers.split(' '):
            ticker = str(ticker).upper()
            try:
                information_comparison = GeneraInformationOfCompany(ticker).__getattribute__(attribute)
            except KeyError:
                errors_ticker += ticker + ', '
                continue
            answer_user += ticker + ': ' + str(information_comparison) + '\n'
        if bool(answer_user) == True:
            await message.answer(text=answer_user, reply_markup=start_button)
    else:
        for ticker in tickers.split(' '):
            ticker = str(ticker).upper()
            try:
                information_comparison = GeneraInformationOfCompany(ticker).__getattribute__(attribute)
                if information_comparison == 'N/A':
                    y.append(0)
                else: y.append(information_comparison)
                x.append(ticker)
            except KeyError:
                errors_ticker += ticker + ', '
                continue
            answer_user += ticker + ': ' + str(number_conversion(information_comparison)) + '\n'
        result = return_comparison_graphics(x, y, attribute=attribute, answer_user=answer_user, listx=x)
        await dp.bot.send_photo(chat_id=message.chat.id, photo=InputFile(result['save_dir']), reply_markup=start_button)

    await dp.bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
    if len(errors_ticker) != 0:
        await message.answer(text=_('Ошибка, данных тикеров не существует: {errors_ticker}').format(errors_ticker=errors_ticker), reply_markup=start_button)
    await state.finish()
        
@dp.callback_query_handler()
async def return_revenue_information(call: types.CallbackQuery):
    await call.answer(text=_('Формируем график...'))
    photopath = InputFile(show_comparison_history_prise(symbol=' '.join(xprise), period=call.data))
    await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await dp.bot.send_photo(chat_id=call.message.chat.id, photo=photopath)