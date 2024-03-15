from faststream.rabbit import RabbitRouter
from queues import bank_queue

router = RabbitRouter()


# @router.subscriber(queue=bank_queue)
# async def purge_messages():
#     pass
