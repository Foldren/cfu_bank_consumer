from os import getenv
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = getenv('POSTGRES_URL')
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