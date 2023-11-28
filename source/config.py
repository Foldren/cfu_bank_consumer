from os import getenv
from dotenv import load_dotenv
from faststream import Context

load_dotenv()


ContextBody = Context("message.decoded_body.data", cast=True)
POSTGRES_URL = getenv('POSTGRES_URL')
RABBITMQ_URL = getenv('RABBITMQ_URL')
PROXY6NET_PROXIES = {"socks5://": getenv('PROXY_HTTPS_URL')}
AERICH_CONFIG = {
    "connections": {"default": getenv('POSTGRES_URL')},
    "apps": {
        "models": {
            "models": ["source.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
