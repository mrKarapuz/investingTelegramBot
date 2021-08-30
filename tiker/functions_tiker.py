import yfinance as yf
from math import fabs
from functools import lru_cache, wraps
from datetime import datetime, timedelta
from middlewares.internationlization import _
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, FixedLocator, MultipleLocator, FormatStrFormatter, FixedFormatter, MaxNLocator
from matplotlib.gridspec import GridSpec


dict_periods={
    '1mo' : _('1 месяц'),
    '3mo' : _('3 месяца'),
    '6mo' : _('6 месяцев'),
    '1y' : _('1 год'),
    '2y' : _('2 года'),
    '5y' : _('5 лет'),
    '10y' : _('10 лет'),
    'max' : _('Максимальный')
}

time_lru = 82800

def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)
        return wrapped_func
    return wrapper_cache

def number_conversion(number):
    '''Показывает число в читаемом формате'''
    is_module = False
    try:
        if number < -9999:
            is_module = True
            number = int(fabs(number))
    except TypeError:
        return '0'
    if 999 < number < 1000000:
        number = str(float(str(number)[:-1]) / 100) + 'TH'
    elif 999999 < number < 1000000000:
        number = str(float(str(number)[:-4]) / 100) + 'M'
    elif 999999999 < number < 1000000000000:
        number =  str(float(str(number)[:-7]) / 100) + 'B'
    elif 999999999999 < number < 1000000000000000:
        number = str(float(str(number)[:-10]) / 100) + 'T'
    
    return number if is_module == False else '-' + str(number)

def formatOY(number, pos):
    '''Показывает число в читаемом формате для графика'''
    is_module = False
    try:
        if number < 0:
            is_module = True
            number = int(fabs(number))
    except TypeError:
        return 0
    if 9999 < number < 1000000:
        number = str(float(str(number)[:-3]) / 100) + 'TH'
        return number if is_module == False else '-' + str(float(number[:-1]) * 100.0) + 'TH'
    elif 999999 < number < 1000000000:
        number = str(float(str(number)[:-6]) / 100) + 'M'
        return number if is_module == False else '-' + str(float(number[:-1]) * 100.0) + 'M'
    elif 999999999 < number < 1000000000000:
        number =  str(float(str(number)[:-9]) / 100) + 'B'
        return number if is_module == False else '-' + str(float(number[:-1]) * 100.0) + 'B'
    elif 999999999999 < number < 1000000000000000:
        number = str(float(str(number)[:-12]) / 100) + 'T'
        return number if is_module == False else '-' + str(float(number[:-1]) * 100.0) + 'T'
    else:
        number = round(float(number), 1)
        return number if is_module == False else '-' + str(number)

@timed_lru_cache(time_lru)
def show_revenue_and_earnings(symbol):
    '''Расчет общей и чистой прибыли компании по годам
    Revenue = Общая прибыль компании
    Earnings = Общая чистая прибыль компании.
    :param symbol: Тикер компании'''
    symbol_company = yf.Ticker(symbol)
    short_name = symbol_company.info['shortName']
    value = ''
    fig = plt.figure(figsize=(8,4),facecolor='#e8e8e8')
    fig.suptitle(_('Расчет общего дохода и чистой прибыли\nкомпании по годам').format(short_name=short_name))
    gs=GridSpec(ncols=3, nrows=1, figure=fig)
    ax = fig.add_subplot(gs[0:2])
    w = 0.2
    x = []
    yrevenue = []
    yearning = []
    for elem in symbol_company.earnings.index:
        d = dict(symbol_company.earnings.loc[elem])
        x.append(elem)
        yrevenue.append(d['Revenue'])
        yearning.append(d['Earnings'])
        revenue = _('Общий доход: ')
        earning = _('Чистая прибыль: ')
        value += '*' + str(elem) + '\n' + revenue + str(number_conversion(d['Revenue'])) + '$\n' + earning + str(number_conversion(d['Earnings'])) + '$\n'
    yrevenue = np.array(yrevenue)
    yearning = np.array(yearning)
    x = np.array(x)
    ax.bar(x - w/2, yrevenue, width=w, label=_('Общий доход'))
    ax.bar(x + w/2, yearning, width=w, label=_('Чистая прибыль'))
    ax.xaxis.set_major_locator(MultipleLocator(base=1))
    ax.yaxis.set_major_locator(MaxNLocator(14))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(FuncFormatter(formatOY))
    ax.legend(bbox_to_anchor=(1.05, 1.0))
    plt.grid()
    plt.figtext(0.66, 0.1, value)
    save_dir = 'graphics/' + str(symbol) + '_revenue_and_earning.png'
    fig.savefig(save_dir)
    return save_dir

@timed_lru_cache(time_lru)
def show_quartal_revenue_and_earnings(symbol):
    '''Расчет общей и чистой прибыли\nкомпании по кварталам
    Revenue = Общая прибыль компании
    Earnings = Общая чистая прибыль компании.
    :param symbol: Тикер компании'''
    symbol_company = yf.Ticker(symbol)
    short_name = symbol_company.info['shortName']
    value = ''
    fig = plt.figure(figsize=(8,4),facecolor='#e8e8e8')
    fig.suptitle(_('Расчет общего дохода и чистой прибыли компании {short_name} по кварталам').format(short_name=short_name))
    gs=GridSpec(ncols=3, nrows=1, figure=fig)
    ax = fig.add_subplot(gs[0:2])
    w = 0.1
    x = []
    xplot = []
    yrevenue = []
    yearning = []
    for elem in symbol_company.quarterly_earnings.index:
        d = dict(symbol_company.quarterly_earnings.loc[elem])
        x.append(elem.replace('Q', ' квартал\n'))
        if int(elem[0]) % 2 != 0:
            xplot.append(float(elem[2:]))
        else:
            xplot.append(float(elem[2:]) + 0.5)
        yrevenue.append(d['Revenue'])
        yearning.append(d['Earnings'])
        revenue = _('Общий доход: ')
        earning = _('Чистая прибыль: ')
        value += '*' + str(elem).replace('Q', ' quartal ') + '\n' + revenue + str(number_conversion(d['Revenue'])) + '$\n' + earning + str(number_conversion(d['Earnings'])) + '$\n'
    yrevenue = np.array(yrevenue)
    yearning = np.array(yearning)
    xplot = np.array(xplot)
    ax.bar(xplot - w/2, yrevenue, width=w, label=_('Общий доход'))
    ax.bar(xplot + w/2, yearning, width=w, label=_('Чистая прибыль'))
    ax.xaxis.set_major_locator(FixedLocator(xplot))
    ax.yaxis.set_major_locator(MaxNLocator(14))
    ax.xaxis.set_major_formatter(FixedFormatter(x))
    ax.yaxis.set_major_formatter(FuncFormatter(formatOY))
    ax.legend(bbox_to_anchor=(1.5, 1.0))
    plt.grid()
    plt.figtext(0.66, 0.1, value)
    save_dir = 'graphics/' + str(symbol) + '_quartal_revenue_and_earning.png'
    fig.savefig(save_dir)
    return save_dir

@timed_lru_cache(time_lru)
def show_balance_sheet(symbol):
    '''Расчет общих активов, обязательств и акционерного капитала компании по годам
    Total Liab = Итого обязательства
    Total Stockholder Equity - Итого акционерный капитал
    Total Assets = Итого активы
    :param symbol: Тикер компании'''
    symbol_company = yf.Ticker(symbol)
    short_name = symbol_company.info['shortName']
    fig = plt.figure(figsize=(8,4),facecolor='#e8e8e8')
    fig.suptitle(_('Расчет общих активов, обязательств и акционерного капитала\nкомпании {short_name} по годам').format(short_name=short_name))
    gs=GridSpec(ncols=4, nrows=1, figure=fig)
    ax = fig.add_subplot(gs[0:3])
    w = 0.2
    value = ''
    x = []
    yassets = []
    yliab = []
    ystockholder = []
    total_assets = _('Aктивы: ')
    total_liab = _('Пассивы: ')
    total_stockholder = _('Капитал: ')
    for elem in symbol_company.balance_sheet.columns:
        x.append(int(str(elem)[:4]))
        d = {}
        value+= '*' + str(elem)[:4] + '\n'
        for e in symbol_company.balance_sheet.index:
            if e == 'Total Assets':
                d['total_assets'] = symbol_company.balance_sheet.get(elem)[e] if str(symbol_company.balance_sheet.get(elem)[e]) != 'nan' else 0
                yassets.append(d['total_assets'])
            if e == 'Total Liab':
                d['total_liab'] = symbol_company.balance_sheet.get(elem)[e] if str(symbol_company.balance_sheet.get(elem)[e]) != 'nan' else 0
                yliab.append(d['total_liab'])
            if e == 'Total Stockholder Equity':
                d['total_stockholder_equity'] = symbol_company.balance_sheet.get(elem)[e] if str(symbol_company.balance_sheet.get(elem)[e]) != 'nan' else 0
                ystockholder.append(d['total_stockholder_equity'])
        value += total_assets + str(number_conversion(int(d['total_assets']))) + '$\n' + total_liab + str(number_conversion(int(d['total_liab']))) + '$\n' + total_stockholder + str(number_conversion(int(d['total_stockholder_equity']))) + '$\n'
    x = np.array(x)
    yassets = np.array(yassets)
    yliab = np.array(yliab)
    ystockholder = np.array(ystockholder)
    ax.bar(x - w*0.999, yassets, width=w, label=_('Активы'))
    ax.bar(x + w*0.001, yliab, width=w, label=_('Пассивы'))
    ax.bar(x + w*0.999, ystockholder, width=w, label=_('Капитал'))
    ax.xaxis.set_major_locator(MultipleLocator(base=1))
    ax.yaxis.set_major_locator(MaxNLocator(14))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(FuncFormatter(formatOY))
    ax.legend(bbox_to_anchor=(1.05, 1.025))
    plt.grid()
    plt.figtext(0.735, 0.02, value, fontsize=9)
    save_dir = 'graphics/' + str(symbol) + '_balance_sheet.png'
    fig.savefig(save_dir)
    return save_dir

@timed_lru_cache(time_lru)
def show_quartal_balance_sheet(symbol):
    '''Расчет общих активов, обязательств и акционерного капитала компании по кварталам
    Total Liab = Итого обязательства
    Total Stockholder Equity - Итого акционерный капитал
    Total Assets = Итого активы
    :param symbol: Тикер компании'''
    symbol_company = yf.Ticker(symbol)
    short_name = symbol_company.info['shortName']
    fig = plt.figure(figsize=(8,4),facecolor='#e8e8e8')
    fig.suptitle(_('Расчет общих активов, обязательств и акционерного капитала\nкомпании {short_name} по кварталам').format(short_name=short_name))
    gs=GridSpec(ncols=4, nrows=1, figure=fig)
    ax = fig.add_subplot(gs[0:3])
    w = 0.1
    value = ''
    x = []
    xplot = []
    yassets = []
    yliab = []
    ystockholder = []
    total_assets = _('Aктивы: ')
    total_liab = _('Пассивы: ')
    total_stockholder = _('Капитал: ')
    p = 0
    for elem in symbol_company.quarterly_balancesheet.columns:
        x.append(str(elem)[:10].replace('-', '.'))
        if p != int(str(elem)[:4]):
            xplot.append(float(str(elem)[:4]) + 0.5)
            p = int(str(elem)[:4])
        else:
            xplot.append(float(str(elem)[:4]))
            p = 0
        d = {}
        value+= '*' + str(elem)[:10].replace('-', '.') + '\n'
        for e in symbol_company.quarterly_balancesheet.index:
            if e == 'Total Assets':
                d['total_assets'] = symbol_company.quarterly_balancesheet.get(elem)[e] if str(symbol_company.quarterly_balancesheet.get(elem)[e]) != 'nan' else 0
                yassets.append(d['total_assets'])
            if e == 'Total Liab':
                d['total_liab'] = symbol_company.quarterly_balancesheet.get(elem)[e] if str(symbol_company.quarterly_balancesheet.get(elem)[e]) != 'nan' else 0
                yliab.append(d['total_liab'])
            if e == 'Total Stockholder Equity':
                d['total_stockholder_equity'] = symbol_company.quarterly_balancesheet.get(elem)[e] if str(symbol_company.quarterly_balancesheet.get(elem)[e]) != 'nan' else 0
                ystockholder.append(d['total_stockholder_equity'])
        value += total_assets + str(number_conversion(int(d['total_assets']))) + '$\n' + total_liab + str(number_conversion(int(d['total_liab']))) + '$\n' + total_stockholder + str(number_conversion(int(d['total_stockholder_equity']))) + '$\n'
    xplot = np.array(xplot)
    yassets = np.array(yassets)
    yliab = np.array(yliab)
    ystockholder = np.array(ystockholder)
    ax.bar(xplot - w*0.999, yassets, width=w, label=_('Активы'))
    ax.bar(xplot + w*0.001, yliab, width=w, label=_('Пассивы'))
    ax.bar(xplot + w*0.999, ystockholder, width=w, label=_('Капитал'))
    ax.xaxis.set_major_locator(FixedLocator(xplot))
    ax.yaxis.set_major_locator(MaxNLocator(14))
    ax.xaxis.set_major_formatter(FixedFormatter(x))
    ax.yaxis.set_major_formatter(FuncFormatter(formatOY))
    ax.legend(bbox_to_anchor=(1.32, 1.025))
    plt.grid()
    plt.figtext(0.735, 0.02, value, fontsize=9)
    save_dir = 'graphics/' + str(symbol) + '_quartal_balance_sheet.png'
    fig.savefig(save_dir)
    return save_dir

@timed_lru_cache(time_lru)
def show_history_dividends(symbol):
    '''Расчет истории дивидендов компании по кварталам
        :param symbol: Тикер компании'''
    symbol_company = yf.Ticker(symbol)
    short_name = symbol_company.info['shortName']
    dict_of_history_dividends = {}  
    value = ''
    for elem in symbol_company.dividends.keys():
        dict_of_history_dividends[str(elem)[:10]] = symbol_company.dividends[elem]
    for key in dict_of_history_dividends.keys():
        value += str(key).replace('-', '.') + ' -> ' + str(dict_of_history_dividends[key]) + '$\n'
    if bool(dict_of_history_dividends) is True:
        fig = plt.figure(figsize=(8,4),facecolor='#e8e8e8')
        fig.suptitle(_('История дивидендов компании {short_name} по кварталам').format(short_name=short_name))
        ax = fig.add_subplot()
        symbol_company.dividends.plot(kind='line')
        ax.set_xlabel(None)
        ax.yaxis.set_major_locator(MaxNLocator(16))
        ax.xaxis.set_major_locator(MaxNLocator(12))
        plt.grid()
        save_dir = 'graphics/' + str(symbol) + '_history_dividends.png'
        fig.savefig(save_dir)
        return (save_dir, value)
    else:
        return (None,_('Компания "{short_name}" не выплачивала дивидендов').format(short_name=short_name))

@timed_lru_cache(time_lru)
def show_history_splits(symbol):
    '''Расчет истории сплитов компании по датам
        :param symbol: Тикер компании'''
    symbol_company = yf.Ticker(symbol)
    short_name = symbol_company.info['shortName']
    global dict_of_history_splits
    dict_of_history_splits = {}
    value = ''
    for elem in symbol_company.splits.keys():
        dict_of_history_splits[str(elem)[0:10]] = symbol_company.splits[elem]
    for key in dict_of_history_splits.keys():
        value += str(elem)[0:10].replace('-', '.') + ' -> ' + str(dict_of_history_splits[key]) + ';\n'
    return value if bool(dict_of_history_splits) is True else _('Компания "{short_name}" не проводила сплитов').format(short_name=short_name)

@timed_lru_cache(time_lru)
def show_comparison_history_prise(symbol, period):
    if symbol.count(' ') > 9:
        return _('Можно выбрать не более 10 компаний')
    elif symbol.count(' ') == 0:
        fig = plt.figure(figsize=(8,6),facecolor='#e8e8e8')
        ax = fig.add_subplot()
        fig.suptitle(_('График изменения цены акции за период: {period}').format(period=dict_periods[period]))
        yf.Ticker(symbol).history(period=period).get('Close').plot(kind='line', label=symbol.upper())
    else:
        ax = yf.download(symbol, period=period).get('Close').plot(kind='line', figsize=(8,4))
        ax.set_title(_('График изменения цен акций за период: {period}').format(period=dict_periods[period]))
    ax.yaxis.set_major_locator(MaxNLocator(16)) 
    ax.set_xlabel(None)
    ax.legend(loc='upper left')
    plt.grid()
    save_dir = 'graphics/' + str(symbol)[:-10:-1] + '_comparison_hp.png'
    plt.savefig(save_dir)
    return save_dir


@timed_lru_cache(time_lru)
class GeneraInformationOfCompany:
    def __init__(self, symbol):
        self.symbol = symbol
        symbol_company = yf.Ticker(symbol)
        object_of_company_info = symbol_company.info
        try:
            self.long_name_of_company = object_of_company_info['longName'] #Полное название компании
        except:
            self.long_name_of_company = 'N/A'
        try:
            self.description_of_company = object_of_company_info['longBusinessSummary'] #Описание компании
        except KeyError or TypeError:
            self.description_of_company = 'N/A'
        self.ticker_of_company = object_of_company_info['symbol'] #Тикер компании
        try:
            self.sector_of_company = object_of_company_info['sector'] #Сектор компании
        except KeyError or TypeError:
            self.sector_of_company = 'N/A'
        self.isin_of_company = symbol_company.isin #Международный идентификационный номер ценных бумаг
        try:
            self.website_of_company = object_of_company_info['website'] #Вебсайт компании
        except KeyError or TypeError:
            self.website_of_company = 'N/A'
        try:
            self.logo_url_of_company = object_of_company_info['logo_url'] #Ссылка на лого компании
        except KeyError or TypeError:
            self.logo_url_of_company = 'N/A'
        try:
            self.market_cap_of_company = object_of_company_info['marketCap'] #Рыночная капитализация компании
        except KeyError or TypeError:
            self.market_cap_of_company = 0
        try:
            self.count_shares_ofustanding_of_company = object_of_company_info['sharesOutstanding'] #Количество обращаемых акций компании
        except KeyError or TypeError:
            self.count_shares_ofustanding_of_company = 0
        self.current_prise_share_now_of_company = round((object_of_company_info['currentPrice']), 2) #Текущая цена акции компании с двумя числами после запятой
        try:
            self.profit_of_company_now = object_of_company_info['totalRevenue'] #Текущий общий доход компании
        except KeyError or TypeError:
            self.profit_of_company_now = 0
        try:
            self.net_profit_of_company_now = object_of_company_info['netIncomeToCommon'] #Текущая чистая прибыль компании
        except KeyError or TypeError:
            self.net_profit_of_company_now = 0
        try:
            self.total_assets_now = int(symbol_company.balance_sheet.get(symbol_company.balance_sheet.columns[0])['Total Assets']) #Итого активы компании
        except KeyError or TypeError:
            self.total_assets_now = 0
        try:
            self.total_liab_now = int(symbol_company.balance_sheet.get(symbol_company.balance_sheet.columns[0])['Total Liab']) #Итого обязательства компании
        except KeyError or TypeError:
            self.total_liab_now = 0
        try:
            self.total_stockholder_equity_now = int(symbol_company.balance_sheet.get(symbol_company.balance_sheet.columns[0])['Total Stockholder Equity']) #Итого акционерный капитал компании
        except KeyError or TypeError:
            self.total_stockholder_equity_now = 0
        self.dividends_of_company_now_per_year_in_dollar = object_of_company_info['dividendRate'] #Дивиденды в долларах данной компании за год 
        self.dividends_of_company_now_per_year_in_dollar = 'N/A' if self.dividends_of_company_now_per_year_in_dollar == None else self.dividends_of_company_now_per_year_in_dollar
        self.dividends_of_company_now_per_year_in_persent = round(self.dividends_of_company_now_per_year_in_dollar*100.0/float(self.current_prise_share_now_of_company), 2) if self.dividends_of_company_now_per_year_in_dollar != 'N/A' else 'N/A'#Дивиденды в процентах данной компании за год 
        try:
            self.eps_of_company = object_of_company_info['trailingEps'] #Текущая прибыль на акцию компании с одним числом после запятой
            self.eps_of_company = round(self.eps_of_company, 1) if self.eps_of_company != None else 'N/A'
        except KeyError or TypeError:
            self.eps_of_company = 'N/A'
        try:
            self.pe_ratio_of_company = object_of_company_info['trailingPE'] #Текущее соотношение "Цена\прибыль" с одним числом после запятой
            self.pe_ratio_of_company = round(self.pe_ratio_of_company, 1) if self.pe_ratio_of_company != None else 'N/A'
        except KeyError or TypeError:
            self.pe_ratio_of_company = 'N/A'

    def return_all_general_information(self):
        name  = _('Полное название: ') + self.long_name_of_company + '\n'
        ticker = _('Тикер: ') + self.ticker_of_company + '\n'
        sector = _('Сектор: ') +  str(self.sector_of_company) + '\n'
        min_paper = _('МИН ценных бумаг: ') + str(self.isin_of_company) + '\n'
        website = _('Вебсайт: ') + self.website_of_company + '\n'
        capitalization = _('Капитализация: ') + str(number_conversion(self.market_cap_of_company)) + '$' + '\n'
        count_shares = _('Количество акций: ') + str(number_conversion(self.count_shares_ofustanding_of_company)) + '\n'
        prise = _('Цена акции: ') + str(number_conversion(self.current_prise_share_now_of_company)) + '$' + '\n'
        profit = _('Общий доход: ') + str(number_conversion(self.profit_of_company_now)) + '$' + '\n'
        net_profit = _('Чистая прибыль: ') + str(number_conversion(self.net_profit_of_company_now)) + '$' + '\n'
        assets = _('Активы: ') + str(number_conversion(self.total_assets_now)) + '$' + '\n'
        liab = _('Обязательства: ') + str(number_conversion(self.total_liab_now)) + '$' + '\n'
        stockholder = _('Акционерный капитал: ') + str(number_conversion(self.total_stockholder_equity_now)) + '$' + '\n'
        dividends_per_dollar = _('Дивиденды в долларах: ') + str(self.dividends_of_company_now_per_year_in_dollar) + '\n'
        dividends_per_percent = _('Дивиденды в процентах: ') + str(self.dividends_of_company_now_per_year_in_persent) + '\n'
        eps = _('Прибыль на акцию: ') + str(self.eps_of_company) + '\n'
        pe = _('Цена\прибыль: ') + str(self.pe_ratio_of_company)
        value = name + ticker + sector + min_paper + website + capitalization + count_shares + prise + profit +  net_profit + assets + liab + stockholder + dividends_per_dollar + dividends_per_percent + eps + pe
        return value