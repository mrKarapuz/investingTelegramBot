from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from loader import dp 
from aiogram.dispatcher.filters import Command
from states import Test
import states


@dp.message_handler(Command('test'))
async def enter_test(message: types.Message):
    await message.answer('Вы начали тестирование\n'
                        'Какую стратегию инвестирования вы предпочитаете?\n')

    await Test.Q1.set()

@dp.message_handler(state = Test.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1 = answer)
    await message.answer('Акции каких компаний вы предпочитаете?')
    await Test.Q2.set()


@dp.message_handler(state = Test.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2 = answer)
    data = await state.get_data()
    answer1 = data.get('answer1')
    answer2 = data.get('answer2')

    await message.answer('Спасибо за ваши ответы')
    await message.answer(answer1)
    await message.answer(answer2    )   
    await state.finish()