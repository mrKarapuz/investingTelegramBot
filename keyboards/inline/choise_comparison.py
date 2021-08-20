from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from middlewares.internationlization import _

choise_inline_comparison = InlineKeyboardMarkup(row_width=1,
inline_keyboard=[
    [
        InlineKeyboardButton(
            text=_('Сектор \U0001F310'),
            callback_data='sector_of_company',
        ),
        InlineKeyboardButton(
            text=_('МИН \U0001F522'),
            callback_data='isin_of_company'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Капитализация \U0001F4B0'),
            callback_data='market_cap_of_company'
        ),
        InlineKeyboardButton(
            text=_('Кол-во акций \U0001F504'),
            callback_data='count_shares_ofustanding_of_company'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Цена акции \U0001F4C8'),
            callback_data='current_prise_share_now_of_company'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Общий доход \U0001F4B5'),
            callback_data='profit_of_company_now'
        ), 
        InlineKeyboardButton(
            text=_('Чистая прибыль \U0001F4B8'),
            callback_data='net_profit_of_company_now'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Активы \U0001F9FE'),
            callback_data='total_assets_now'
        ), 
        InlineKeyboardButton(
            text=_('Обязательства \U0001F9FE'),
            callback_data='total_liab_now'
        ),
        InlineKeyboardButton(
            text=_('Капитал \U0001F4BC'),
            callback_data='total_stockholder_equity_now'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Дивиденды ($)'),
            callback_data='dividends_of_company_now_per_year_in_dollar'
        ),
        InlineKeyboardButton(
            text=_('Дивиденды (%)'),
            callback_data='dividends_of_company_now_per_year_in_persent'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Прибыль на акцию \U0001F4DD'),
            callback_data='eps_of_company'
        ), 
        InlineKeyboardButton(
            text=_('Цена\прибыль \U0001F50E'),
            callback_data='pe_ratio_of_company'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Назад \U0001F448'),
            callback_data='cancel'
        )
    ],
])

choise_inline_date_for_stockprise = InlineKeyboardMarkup(row_width=1,
inline_keyboard=[
    [
        InlineKeyboardButton(
            text=_('1 месяц'),
            callback_data='1mo'
        ),
        InlineKeyboardButton(
            text=_('3 месяца'),
            callback_data='3mo'
        ),
        InlineKeyboardButton(
            text='6 месяцев',
            callback_data='6mo'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('1 год'),
            callback_data='1y'
        ),
        InlineKeyboardButton(
            text=_('2 года'),
            callback_data='2y'
        ),
        InlineKeyboardButton(
            text=_('5 лет'),
            callback_data='5y'
        ),
        InlineKeyboardButton(
            text=_('10 лет'),
            callback_data='10y'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Максимум'),
            callback_data='max'
        )
    ],
])