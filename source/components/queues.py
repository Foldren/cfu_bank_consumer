from faststream.rabbit import RabbitQueue
from config import BANK_QUEUE


bank_queue = RabbitQueue(name=BANK_QUEUE)  # , robust=False, durable=True)
