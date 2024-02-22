from os import environ
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

IS_THIS_LOCAL = "Pycharm" in str(Path.cwd())

BANK_QUEUE = "bank_queue"

RABBITMQ_URL = environ['RABBITMQ_URL']

TORTOISE_CONFIG = {
    "connections": {
        "default": environ['PG_URL']
    },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default"
        }
    }
}
