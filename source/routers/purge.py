from faststream.rabbit import RabbitRouter

router = RabbitRouter()


# @router.subscriber(queue=bank_queue)
# async def purge_messages():
#     pass
