
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import reply_keyboard
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from loader import dp, db
from aiogram import types
from keyboards.default import start_button
from middlewares.internationlization import _
from states import SelectCompanies


dict_select_company = {
    'Капитализация ' : {'selected': False, 'name': 'capitalizacion'},
    'Кол-во акций ': {'selected': False, 'name': 'count_shares'},
    'Цена акции ': {'selected': False, 'name': 'prise'},
    'Общий доход ': {'selected': False, 'name': 'profit'},
    'Чистая прибыль ': {'selected': False, 'name': 'net_profit'},
    'Активы ': {'selected': False, 'name': 'assets'},
    'Обязательства ': {'selected': False, 'name': 'liab'},
    'Капитал ': {'selected': False, 'name': 'stockholder'},
    'Дивиденды ($) ': {'selected': False, 'name': 'dividends_per_dollar'},
    'Дивиденды (%) ': {'selected': False, 'name': 'dividends_per_percent'},
    'Прибыль на акцию ': {'selected': False, 'name': 'eps'},
    'Цена\прибыль ': {'selected': False, 'name': 'pe'}}
    
def do_inline_select_company(board):
    kb = InlineKeyboardMarkup()
    for key, data in board.items():
        kb.row(
            InlineKeyboardButton(text = f"{key} {'✅' if data['selected'] else '❌'}", callback_data=data['name'])
        ),
        
    kb.row(
        InlineKeyboardButton(
            text=_('Продолжить 🆗'),
            callback_data='continue'
        ),
        InlineKeyboardButton(
            text=_('Назад \U0001F448'),
            callback_data='cancel'
        )
    )
    return kb



@dp.callback_query_handler(text='cancel', state = [SelectCompanies.enter_the_sign, SelectCompanies.chose_the_sign])
async def cancel_select(call: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('msg_id'):
        await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get('msg_id'))
    await call.message.answer(text=_('Отмена'), reply_markup=start_button)
    await state.finish()

@dp.callback_query_handler(text='continue', state = [SelectCompanies.enter_the_sign, SelectCompanies.chose_the_sign])
async def continue_select(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get('msg_id'))
    attrbut = []
    attrbut_text = ''
    for key, value in data.get('keybord').items():
        if value['selected']:
            attrbut.append(value['name'])
            attrbut_text+=key + '\n'
    await state.update_data(attrbut=attrbut)    
    add_sql = ''
    if len(attrbut) != 0:
        await call.message.answer(text=f'Введите значение от и до для данных атрибутов через запятую в формате:\n\n"20-" - от 20 до maximum \n"-1000" - от minimum до 1000\n"20-1000" - от 20 до 1000\n Последовательность:\n{attrbut_text}')
    else:
        await call.message.answer(text='Вы не выбрали ни одного признака для сравнения', reply_markup=start_button)
        await state.finish()
        return 0
    # for elem in attrbut_text.split('\n')[:-1]:
        
    await SelectCompanies.enter_numbers.set()

@dp.message_handler(state = SelectCompanies.enter_numbers)
async def enter_numbers(message: types.Message, state: FSMContext):
    data = await state.get_data()
    attrbut = data.get('attrbut')
    add_sql = ''
    numbers = message.text.replace(' ', '').split(',')
    if len(attrbut) != len(numbers):
        await SelectCompanies.enter_the_sign.set()
        await message.answer(text='Количество выбранных для сравнения атрибутов не соответсвует количеству введенных чисел\nПожалуйста еще раз сделайте ваш выбор', reply_markup=do_inline_select_company(data.get('keybord')))
    else:
        await message.answer(text='Соответствует, продолажаем')
        for elem in attrbut: 
            if bool(numbers[0]):
                FROM = numbers[0][:numbers[0].find('-')]
                TO = numbers[0][numbers[0].find('-') + 1:] 
                if FROM and TO:
                    add_sql += f" {elem} BETWEEN {FROM} AND {TO} AND"
                elif bool(FROM)!=False:
                    add_sql += f" {elem} > {FROM} AND"
                elif bool(TO)!=0:
                    add_sql += f" {elem} < {TO} AND"
                numbers.pop(0)
                continue
        add_sql = add_sql[:-4]
        ansver = db.select_tickers(attributes=attrbut, add_sql=add_sql)
        print(ansver)
        


@dp.message_handler(text='Подобрать компании 🤑')
async def select_sign(message: types.Message, state: FSMContext):
    await SelectCompanies.enter_the_sign.set()
    await state.update_data(keybord = dict_select_company)
    data = await state.get_data()
    keybord = data.get('keybord')
    msg = await message.answer(_('Выберите признаки на которых будет основываться подбор'), reply_markup=do_inline_select_company(keybord))
    await state.update_data(msg_id = msg.message_id)
    
    
@dp.callback_query_handler(state=[SelectCompanies.enter_the_sign, SelectCompanies.chose_the_sign])
async def select_interval(call: types.CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    keybord = data.get('keybord')
    for key, value in keybord.items():
        if value['name'] == call.data:
            if value['selected'] == False:
                value['selected'] = True
            else:
                value['selected'] = False
    await state.update_data(keybord=keybord)
    await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=data.get('msg_id'))
    msg = await call.message.answer(text=call.message.text, reply_markup=do_inline_select_company(keybord))
    await state.update_data(msg_id = msg.message_id)
    await SelectCompanies.chose_the_sign.set()
