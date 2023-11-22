from environs import Env

env = Env()
env.read_env('.env')

POSTGRES_URL = env('POSTGRES_URL')
RABBITMQ_URL = env('RABBITMQ_URL')
AERICH_CONFIG = {
    "connections": {"default": env('POSTGRES_URL')},
    "apps": {
        "models": {
            "models": ["source.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}