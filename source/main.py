from asyncio import run
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from taskiq_faststream import BrokerWrapper
from tortoise import run_async
from config import RABBITMQ_URL
from init_db import init_db
from router import manage_banks

broker = RabbitBroker(RABBITMQ_URL)
app = FastStream(broker)
taskiq_broker = BrokerWrapper(broker)

broker.include_router(manage_banks.router)


async def main():
    await app.run()


if __name__ == "__main__":
    run_async(init_db())
    run(main())
