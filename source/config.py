from os import getenv, environ
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

IS_THIS_LOCAL = "Pycharm" in str(Path.cwd())
BANK_QUEUE = "test_queue" if IS_THIS_LOCAL else "bank_queue"
POSTGRES_URL = getenv('POSTGRES_URL') if IS_THIS_LOCAL else environ['POSTGRES_URL']
RABBITMQ_URL = getenv('RABBITMQ_URL')
AERICH_CONFIG = {
    "connections": {"default": getenv('POSTGRES_URL')},
    "apps": {
        "models": {
            "models": ["source.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
