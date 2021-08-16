
from aiogram.dispatcher.filters.state import State, StatesGroup

class Comparison(StatesGroup):
    enter_the_attribute = State()
    enter_the_tickers = State()