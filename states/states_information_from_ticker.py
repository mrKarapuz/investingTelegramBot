from aiogram.dispatcher.filters.state import State, StatesGroup

class InformationFromTicker(StatesGroup):
    enter_the_ticker = State()