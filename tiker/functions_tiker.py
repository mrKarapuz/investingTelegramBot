import yfinance as yf
from math import fabs
from functools import lru_cache, wraps
from datetime import datetime, timedelta
from middlewares.internationlization import _

time_lru = 600

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
		if number < 0:
			is_module = True
			number = int(fabs(number))
	except TypeError:
		return 0
	if 999 < number < 1000000:
		number = str(float(str(number)[:-1]) / 100) + 'TH'
	elif 999999 < number < 1000000000:
		number = str(float(str(number)[:-4]) / 100) + 'M'
	elif 999999999 < number < 1000000000000:
		number =  str(float(str(number)[:-7]) / 100) + 'B'
	elif 999999999999 < number < 1000000000000000:
		number = str(float(str(number)[:-10]) / 100) + 'T'
	return number if is_module == False else '-' + number

@timed_lru_cache(time_lru)
def do_dict_revenue_and_earnings(symbol):
	'''Расчет общей и чистой прибыли компании по годам
	Revenue = Общая прибыль компании
	Earnings = Общая чистая прибыль компании.
	:param symbol: Тикер компании'''
	symbol_company = yf.Ticker(symbol)
	global dict_of_revenue_and_earnings
	dict_of_revenue_and_earnings = {}
	value = ''
	for elem in symbol_company.earnings.index:
		d = dict(symbol_company.earnings.loc[elem])
		revenue = _('Общий доход: ')
		earning =  _('Чистая прибыль: ')
		value += '*' + str(elem) + '\n' + revenue + str(number_conversion(d['Revenue'])) + '$\n' + earning + str(number_conversion(d['Earnings'])) + '$\n'
		dict_of_revenue_and_earnings[str(elem)] = d
	return value

@timed_lru_cache(time_lru)
def do_dict_quarterly_revenue_and_earnings(symbol):
	'''Расчет общей и чистой прибыли компании по кварталам
	Revenue = Общая прибыль компании
	Earnings = Общая чистая прибыль компании.
	:param symbol: Тикер компании'''
	symbol_company = yf.Ticker(symbol)
	global dict_of_quarterly_revenue_and_earnings
	dict_of_quarterly_revenue_and_earnings = {}
	value = ''
	revenue = _('Общий доход: ')
	earning =  _('Чистая прибыль: ') 
	for elem in symbol_company.quarterly_earnings.index:
		d = dict(symbol_company.quarterly_earnings.loc[elem])
		value += '*' + str(elem).replace('Q', ' quartal ') + '\n' + revenue + str(number_conversion(d['Revenue'])) + '$\n' + earning + str(number_conversion(d['Earnings'])) + '$\n'
		dict_of_quarterly_revenue_and_earnings[str(elem)] = d
	return value

@timed_lru_cache(time_lru)
def do_dict_balance_sheet(symbol):
	'''Расчет общих активов, обязательств и акционерного капитала компании по годам
	Total Liab = Итого обязательства
	Total Stockholder Equity - Итого акционерный капитал
	Total Assets = Итого активы
	:param symbol: Тикер компании'''
	symbol_company = yf.Ticker(symbol)
	global dict_of_balance_sheet
	dict_of_balance_sheet = {}
	value = ''
	total_assets = _('Aктивы: ')
	total_liab = _('Пассивы: ')
	total_stockholder = _('Капитал: ')
	for elem in symbol_company.balance_sheet.columns:
		d = {}
		value+= '*' + str(elem)[:4] + '\n'
		for e in symbol_company.balance_sheet.index:
			if e == 'Total Assets':
				d['total_assets'] = symbol_company.balance_sheet.get(elem)[e] if str(symbol_company.balance_sheet.get(elem)[e]) != 'nan' else 0
			if e == 'Total Liab':
				d['total_liab'] = symbol_company.balance_sheet.get(elem)[e] if str(symbol_company.balance_sheet.get(elem)[e]) != 'nan' else 0
			if e == 'Total Stockholder Equity':
				d['total_stockholder_equity'] = symbol_company.balance_sheet.get(elem)[e] if str(symbol_company.balance_sheet.get(elem)[e]) != 'nan' else 0
		value += total_assets + str(number_conversion(int(d['total_assets']))) + '$\n' + total_liab + str(number_conversion(int(d['total_liab']))) + '$\n' + total_stockholder + str(number_conversion(int(d['total_stockholder_equity']))) + '$\n'
		dict_of_balance_sheet[str(elem)[:4]] = d
	return value

@timed_lru_cache(time_lru)
def do_dict_quarterly_balance_sheet(symbol):
	'''Расчет общих активов, обязательств и акционерного капитала компании по кварталам
	Total Liab = Итого обязательства
	Total Stockholder Equity - Итого акционерный капитал
	Total Assets = Итого активы
	:param symbol: Тикер компании'''
	symbol_company = yf.Ticker(symbol)
	global dict_quarterly_balance_sheet
	dict_quarterly_balance_sheet = {}
	value = ''
	total_assets = _('Aктивы: ')
	total_liab = _('Пассивы: ')
	total_stockholder = _('Капитал: ')
	for elem in symbol_company.quarterly_balancesheet.columns:
		d = {}
		value+= '*' + str(elem)[:10].replace('-', '.') + '\n'
		for e in symbol_company.quarterly_balancesheet.index:
			if e == 'Total Assets':
				d['total_assets'] = symbol_company.quarterly_balancesheet.get(elem)[e] if str(symbol_company.quarterly_balancesheet.get(elem)[e]) != 'nan' else 0
			if e == 'Total Liab':
				d['total_liab'] = symbol_company.quarterly_balancesheet.get(elem)[e] if str(symbol_company.quarterly_balancesheet.get(elem)[e]) != 'nan' else 0
			if e == 'Total Stockholder Equity':
				d['total_stockholder_equity'] = symbol_company.quarterly_balancesheet.get(elem)[e] if str(symbol_company.quarterly_balancesheet.get(elem)[e]) != 'nan' else 0
		value += total_assets + str(number_conversion(int(d['total_assets']))) + '$\n' + total_liab + str(number_conversion(int(d['total_liab']))) + '$\n' + total_stockholder + str(number_conversion(int(d['total_stockholder_equity'])))  + '$\n'
		dict_quarterly_balance_sheet[str(elem)[:4]] = d
	return value

@timed_lru_cache(time_lru)
def do_dict_history_dividends(symbol):
	'''Расчет истории дивидендов компании по кварталам
		:param symbol: Тикер компании'''
	symbol_company = yf.Ticker(symbol)
	short_name = symbol_company.info['shortName']
	global dict_of_history_dividends
	dict_of_history_dividends = {}
	value = ''
	for elem in symbol_company.dividends.keys():
		dict_of_history_dividends[str(elem)[:10]] = symbol_company.dividends[elem]
	for key in dict_of_history_dividends.keys():
		value += str(key).replace('-', '.') + ' -> ' + str(dict_of_history_dividends[key]) + '$\n'
	return value if bool(dict_of_history_dividends) is True else _('Компания "{short_name}" не выплачивала дивидендов').format(short_name=short_name)

@timed_lru_cache(time_lru)
def do_dict_history_splits(symbol):
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
class GeneraInformationOfCompany:
	def __init__(self, symbol):
		self.symbol = symbol
		symbol_company = yf.Ticker(symbol)
		object_of_company_info = symbol_company.info
		self.long_name_of_company = object_of_company_info['longName'] #Полное название компании
		self.description_of_company = object_of_company_info['longBusinessSummary'] #Описание компании
		self.ticker_of_company = object_of_company_info['symbol'] #Тикер компании
		self.sector_of_company = object_of_company_info['sector'] #Сектор компании
		self.isin_of_company = symbol_company.isin #Международный идентификационный номер ценных бумаг
		self.website_of_company = object_of_company_info['website'] #Вебсайт компании
		self.logo_url_of_company = object_of_company_info['logo_url'] #Ссылка на лого компании
		self.market_cap_of_company = number_conversion(object_of_company_info['marketCap']) #Рыночная капитализация компании
		self.count_shares_ofustanding_of_company = number_conversion(object_of_company_info['sharesOutstanding']) #Количество обращаемых акций компании
		self.current_prise_share_now_of_company = round((object_of_company_info['currentPrice']), 2) #Текущая цена акции компании с двумя числами после запятой
		self.profit_of_company_now = number_conversion(object_of_company_info['totalRevenue']) #Текущий общий доход компании
		self.net_profit_of_company_now = number_conversion(object_of_company_info['netIncomeToCommon']) #Текущая чистая прибыль компании
		self.total_assets_now = number_conversion(int(symbol_company.balance_sheet.get(symbol_company.balance_sheet.columns[0])['Total Assets'])) #Итого активы компании
		self.total_liab_now = number_conversion(int(symbol_company.balance_sheet.get(symbol_company.balance_sheet.columns[0])['Total Liab'])) #Итого обязательства компании
		self.total_stockholder_equity_now = number_conversion(int(symbol_company.balance_sheet.get(symbol_company.balance_sheet.columns[0])['Total Stockholder Equity'])) #Итого акционерный капитал компании
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
		capitalization = _('Капитализация: ') + str(self.market_cap_of_company) + '$' + '\n'
		count_shares = _('Количество акций: ') + str(self.count_shares_ofustanding_of_company) + '\n'
		prise = _('Цена акции: ') + str(self.current_prise_share_now_of_company) + '$' + '\n'
		profit = _('Общий доход: ') + str(self.profit_of_company_now) + '$' + '\n'
		net_profit = _('Чистая прибыль: ') + str(self.net_profit_of_company_now) + '$' + '\n'
		assets = _('Активы: ') + str(self.total_assets_now) + '$' + '\n'
		liab = _('Обязательства: ') + str(self.total_liab_now) + '$' + '\n'
		stockholder = _('Акционерный капитал: ') + str(self.total_stockholder_equity_now) + '$' + '\n'
		dividends_per_dollar = _('Дивиденды в долларах: ') + str(self.dividends_of_company_now_per_year_in_dollar) + '\n'
		dividends_per_percent = _('Дивиденды в процентах: ') + str(self.dividends_of_company_now_per_year_in_persent) + '\n'
		eps = _('Прибыль на акцию: ') + str(self.eps_of_company) + '\n'
		pe = _('Цена\прибыль: ') + str(self.pe_ratio_of_company)
		value = name + ticker + sector + min_paper + website + capitalization + count_shares + prise + profit +  net_profit + assets + liab + stockholder + dividends_per_dollar + dividends_per_percent + eps + pe
		return value


