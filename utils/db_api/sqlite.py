import mysql.connector

class Database:
    @property
    def connection(self):
        return mysql.connector.connect(host="colt.cityhost.com.ua",  
                        port=3306,
                        user="chd11fa3e1_konov",        
                        password="",
                        db="chd11fa3e1_konov",)

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

    def select_all_users(self):
        sql = 'SELECT * FROM `investing_users`'
        return self.execute(sql, fetchall=True)

    def select_user_language(self, id):
        sql = f'SELECT user_language FROM `investing_users` WHERE id = "{id}"'
        return self.execute(sql=sql, fetchone=True)

    def update_user_language(self, id, language):
        sql = f"UPDATE `investing_users` SET `user_language`='{language}' WHERE id = {id}"
        return self.execute(sql=sql, fetchone=True)