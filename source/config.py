from os import environ
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

IS_THIS_LOCAL = "Pycharm" in str(Path.cwd())

BANK_QUEUE = "bank_queue"

RABBITMQ_URL = environ['RABBITMQ_URL']

TORTOISE_CONFIG = {
    "connections": {
        "bank": environ['BANK_PG_URL'],
        "telegram": environ['TG_PG_URL']
    },
    "apps": {
        "bank": {"models": ["db_models.bank", "aerich.models"], "default_connection": "bank"},
        "telegram": {"models": ["db_models.telegram"], "default_connection": "telegram"}
    }
}

# Не редактируемые категории
STATIC_CATEGORIES = ["Зарплата", "Аренда", "Упаковка"]

PROXY6NET_PROXIES = {"socks5://": environ['PROXY_HTTPS_URL']}

BANKS_INDEXES = ["tinkoff", "module", "tochka"]

SECRET_KEY = environ['SECRET_KEY']
