
import mysql.connector
import yahoo_fin.stock_info as yfs
from time import strftime

class Database:
    @property
    def connection(self):
        return mysql.connector.connect(host="colt.cityhost.com.ua",  
                        port='3306',
                        user='chd11fa3e1_konov',         
                        password='pp1813kk0278',
                        db='chd11fa3e1_konov',)

    def execute(self, sql, parameters = tuple(), fetchone=False, fetchall=False, commit=False): 
        connection = self.connection
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data
    
    def add_user(self, first_name, last_name, user_name, id, user_language):
        sql = 'INSERT INTO `investing_users`(`first_name`, `last_name`, `user_name`, `id`, `user_language`) VALUES (%s, %s, %s, %s, %s)'
        parameters = (first_name, last_name, user_name, id, user_language)
        self.execute(sql, parameters=parameters, commit=True)

    def select_user_language(self, id):
        sql = f'SELECT user_language FROM `investing_users` WHERE id = "{id}"'
        return self.execute(sql=sql, fetchone=True)

    def update_user_language(self, id, language):
        sql = f"UPDATE `investing_users` SET `user_language`='{language}' WHERE id = {id}"
        return self.execute(sql=sql, fetchone=True)

    def add_tickers(self, GeneraInformationOfCompany):
        dow = yfs.tickers_dow()
        sp = yfs.tickers_sp500()
        sp.extend(dow)
        list_of_company = sorted(list(set(sp)))
        for elem in list_of_company:
            company = GeneraInformationOfCompany(elem)
            name = company.long_name_of_company if company.long_name_of_company != None else 'N/A'
            date = strftime('%d.%m.%Y\n%H.%M.%S')
            ticker = company.ticker_of_company
            index_company = ''
            if elem.upper() in dow:
                index_company+='DOW '
            if elem.upper() in sp:
                index_company+='SP500 '
            sector = company.sector_of_company
            capitalization = company.market_cap_of_company if company.market_cap_of_company != None else 'N/A'
            count_shares = company.count_shares_ofustanding_of_company if company.count_shares_ofustanding_of_company != None else 'N/A'
            prise = company.current_prise_share_now_of_company
            profit = company.profit_of_company_now if company.profit_of_company_now != None else 'N/A'
            net_profit = company.net_profit_of_company_now
            assets = company.total_assets_now
            liab = company.total_liab_now
            stockholder = company.total_stockholder_equity_now
            dividends_per_dollar = company.dividends_of_company_now_per_year_in_dollar
            dividends_per_percent = company.dividends_of_company_now_per_year_in_persent
            eps = company.eps_of_company
            pe = company.pe_ratio_of_company
            sql = "INSERT INTO `companies` (`name`, `date`, `ticker`, `index_company`, `sector`, `capitalizacion`, `count_shares`, `prise`, `profit`, `net_profit`, `assets`, `liab`, `stockholder`, `dividends_per_dollar`, `dividends_per_percent`, `eps`, `pe`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            param = (name, date, ticker, index_company, sector, capitalization, count_shares, prise, profit, net_profit, assets, liab, stockholder, dividends_per_dollar, dividends_per_percent, eps, pe)
            try:
                self.execute(sql = sql, parameters=param)
                print(f'Успешно занесено в базу данных: {elem}')
            except:
                sql = f"UPDATE `companies` SET `name`='{name}', `date`='{date}', `ticker`='{ticker}',`index_company`='{index_company}',`sector`='{sector}',`capitalizacion`='{capitalization}',`count_shares`='{count_shares}',`prise`='{prise}',`profit`='{profit}',`net_profit`='{net_profit}',`assets`='{assets}',`liab`='{liab}',`stockholder`='{stockholder}',`dividends_per_dollar`='{dividends_per_dollar}',`dividends_per_percent`='{dividends_per_percent}',`eps`='{eps}',`pe`='{pe}' WHERE ticker='{elem}'"
                try:
                    self.execute(sql)
                    print(f'Успешно обновлено в базе данных: {elem}')
                except:
                    print(f'Ошибка, в базу данных не было занесено: {elem}')
                    continue
        return 'База данных обновлена'

    def select_all_users(self):
        sql = 'SELECT * FROM `investing_users`'
        return self.execute(sql, fetchall=True)

    def select_len_companies(self):
        sql = "SELECT COUNT(*) FROM `companies`"
        return self.execute(sql, fetchone=True)

    def select_sectors(self, sql):
        return self.execute(sql=sql, fetchall=True)

    def select_tickers(self, attributes, add_sql=''):
        sql_select = 'ticker, sector, '
        for attr in attributes:
            sql_select += attr + ', '
        sql = f"SELECT {sql_select[:-2]}  FROM `companies` WHERE" + add_sql
        return self.execute(sql=sql, parameters=(), fetchall=True)

