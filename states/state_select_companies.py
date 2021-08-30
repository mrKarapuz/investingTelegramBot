from aiogram.dispatcher.filters.state import State, StatesGroup

class SelectCompanies(StatesGroup):
    enter_the_sign = State()
    chose_the_sign = State()
    enter_numbers = State()