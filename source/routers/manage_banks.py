from faststream.rabbit import RabbitRouter
from source.queues import bank_queue

router = RabbitRouter()


@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.get-supported-banks")
async def get_supported_banks():
    return 'Get supported banks handler is working!'


@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.create-user-bank")
async def create_user_bank():
    return 'Create user bank handler is working!'


@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.update-user-bank")
async def update_user_bank():
    return 'Update user bank handler is working!'


@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.delete-user-bank")
async def delete_user_bank():
    return 'Delete user bank handler is working!'


@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.get-user-banks")
async def get_user_banks():
    return 'Get user banks handler is working!'


@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.get-user-expenses")
async def get_user_expenses():
    return 'Get user expenses handler is working!'


@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.get-user-account-balances")
async def get_user_account_balances():
    return 'Get user account balances handler is working!'


@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.get-user-cash-balances-on-hand")
async def get_user_cash_balances_on_hand():
    return 'Get user cash balances on hand handler is working!'


@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.close-user-bank-account")
async def close_user_bank_account():
    return 'Close user bank handler is working!'
