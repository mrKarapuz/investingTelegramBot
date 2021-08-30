from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from middlewares.internationlization import _





choise_sign_select_company = InlineKeyboardMarkup(row_width=1,
inline_keyboard=[
    [
        InlineKeyboardButton(
            text=_('Капитализация ❌'),
            callback_data='market_cap_of_company'
        ),
        InlineKeyboardButton(
            text=_('Кол-во акций ❌'),
            callback_data='count_shares_ofustanding_of_company'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Цена акции ❌'),
            callback_data='current_prise_share_now_of_company'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Общий доход ❌'),
            callback_data='profit_of_company_now'
        ), 
        InlineKeyboardButton(
            text=_('Чистая прибыль ❌'),
            callback_data='net_profit_of_company_now'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Активы ❌'),
            callback_data='total_assets_now'
        ), 
        InlineKeyboardButton(
            text=_('Обязательства ❌'),
            callback_data='total_liab_now'
        ),
        InlineKeyboardButton(
            text=_('Капитал ❌'),
            callback_data='total_stockholder_equity_now'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Дивиденды ($) ❌'),
            callback_data='dividends_of_company_now_per_year_in_dollar'
        ),
        InlineKeyboardButton(
            text=_('Дивиденды (%) ❌'),
            callback_data='dividends_of_company_now_per_year_in_persent'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Прибыль на акцию ❌'),
            callback_data='eps_of_company'
        ), 
        InlineKeyboardButton(
            text=_('Цена\прибыль ❌'),
            callback_data='pe_ratio_of_company'
        )
    ],
    [
        InlineKeyboardButton(
            text=_('Продолжить 🆗'),
            callback_data='continue'
        ),
        InlineKeyboardButton(
            text=_('Назад \U0001F448'),
            callback_data='cancel'
        )
    ],
])