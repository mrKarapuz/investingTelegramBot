import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
MYSQL_password = str(os.getenv("MYSQL_PASSWORD"))
MYSQL_login_database = str(os.getenv('MYSQL_LOGIN_DATABASE'))
MYSQL_port = str(os.getenv('MYSQL_PORT'))
admins = [
    
]

ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
