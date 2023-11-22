from faststream.rabbit import RabbitQueue

bank_queue = RabbitQueue(name="bank_queue")  # , robust=False, durable=True)
