from os import environ
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

IS_THIS_LOCAL = "Pycharm" in str(Path.cwd())

BANK_QUEUE = "bank_queue"

RABBITMQ_URL = environ['RABBITMQ_URL']

TORTOISE_CONFIG = {
    "connections": {
        "bank": environ['BANK_PG_URL']
    },
    "apps": {
        "bank": {"models": ["models", "aerich.models"], "default_connection": "bank"}
    }
}
