from os import environ
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

IS_THIS_LOCAL = "Pycharm" in str(Path.cwd())

BANK_QUEUE = "bank_queue"

RABBITMQ_URL = environ['RABBITMQ_URL']

TORTOISE_CONFIG = {
    "connections": {
        "telegram": environ['TG_PG_URL'],
        "bank": environ['BANK_PG_URL']
    },
    "apps": {
        "telegram": {"models": ["db_models.telegram"], "default_connection": "telegram"},
        "bank": {"models": ["db_models.bank"], "default_connection": "bank"}
    }
}

# Не редактируемые категории
STATIC_CATEGORIES = [
    "Зарплата", "Аренда", "Упаковка"
]