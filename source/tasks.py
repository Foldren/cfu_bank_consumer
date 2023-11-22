from faststream.rabbit import RabbitRouter
from main import taskiq_broker

router = RabbitRouter()


# Планируем таску на 04:00 по обновлению банков каждый день
@taskiq_broker.task(schedule=[{"cron": "*/1 * * * *"}])
async def reload_banks_operations():
    print('Get supported banks handler is working!')
