from dataclasses import asdict
from json import dumps
from faststream import Context
from faststream.rabbit import RabbitRouter
from decorators import rpc_exception
from models import SupportBank, UserBank, PaymentAccount
from request.manage_banks import CreateBankRequest, UpdateUserBankRequest, DeleteUserBankRequest, GetUserBankRequest, \
    CloseBankAccountRequest, ExpensesRequest
from response.manage_banks import SupportedBankResponse, DSupportedBank, CreateBankResponse, UpdateUserBankResponse, \
    DeleteUserBankResponse, DBank, GetUserBankResponse, CloseBankAccountResponse
from response.rpc import RpcResponse, RpcError
from source.queues import bank_queue

router = RabbitRouter()


@rpc_exception
@router.publisher(queue=bank_queue, reply_to="amq.rabbitmq.reply-to")
@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.get-supported-banks")
async def get_supported_banks(response: RpcResponse):
    support_banks = await SupportBank.all()
    data_list = []

    for bank in support_banks:
        data_list.append(DSupportedBank(id=bank.id, name=bank.name, url=bank.logo_url))

    response.data = SupportedBankResponse(banks=data_list)


@rpc_exception
@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.create-user-bank")
async def create_user_bank(response: RpcResponse,
                           request: CreateBankRequest = Context("message.decoded_body.data", cast=True)):
    created_bank = await UserBank.create(
        user_id=request.userID,
        support_bank_id=request.bankID,
        name=request.name,
        token=request.token.encode(),
    )

    support_bank = await created_bank.support_bank

    response.data = CreateBankResponse(
        id=created_bank.id,
        name=created_bank.name,
        bankID=support_bank.id,
        bankUrl=support_bank.logo_url
    )


@rpc_exception
@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.update-user-bank")
async def update_user_bank(response: RpcResponse,
                           request: UpdateUserBankRequest = Context("message.decoded_body.data", cast=True)):
    user_bank = await UserBank.filter(id=request.id, user_id=request.userID).first()
    support_bank = await user_bank.support_bank

    if request.name:
        user_bank.name = request.name
    if request.token:
        user_bank.token = request.token.encode()

    await user_bank.save()
    await user_bank.refresh_from_db()

    response.data = UpdateUserBankResponse(
        id=user_bank.id,
        name=user_bank.name,
        bankID=support_bank.id,
        bankUrl=support_bank.logo_url
    )


@rpc_exception
@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.delete-user-bank")
async def delete_user_bank(response: RpcResponse,
                           request: DeleteUserBankRequest = Context("message.decoded_body.data", cast=True)):
    await UserBank.filter(id=request.bankID, user_id=request.userID).delete()

    response.data = DeleteUserBankResponse(id=request.bankID)


@rpc_exception
@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.get-user-banks")
async def get_user_banks(response: RpcResponse,
                         request: GetUserBankRequest = Context("message.decoded_body.data", cast=True)):
    user_banks = await UserBank.filter(user_id=request.userID).select_related("support_bank")
    data_list = []

    for bank in user_banks:
        data_list.append(
            DBank(id=bank.id, name=bank.name, bankID=bank.support_bank.id, token=bank.token.decode('utf-8')))

    response.data = GetUserBankResponse(banks=data_list)


@rpc_exception
@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "c")
async def close_user_bank_account(response: RpcResponse,
                                  request: CloseBankAccountRequest = Context("message.decoded_body.data", cast=True)):
    pa = await PaymentAccount.filter(id=request.paymentAccountID, user_bank__user_id=request.userID).first()
    pa.status = 0
    await pa.save()

    response.data = CloseBankAccountResponse(id=request.paymentAccountID)


@rpc_exception
@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.get-user-expenses")
async def get_user_expenses(response: RpcResponse,
                            request: ExpensesRequest = Context("message.decoded_body.data", cast=True)):
    return 'Get user expenses handler is working!'


@router.subscriber(queue=bank_queue, filter=lambda msg: msg.decoded_body['pattern'] == "bank.get-user-account-balances")
async def get_user_account_balances():
    return 'Get user account balances handler is working!'


@router.subscriber(queue=bank_queue,
                   filter=lambda msg: msg.decoded_body['pattern'] == "bank.get-user-cash-balances-on-hand")
async def get_user_cash_balances_on_hand():
    return 'Get user cash balances on hand handler is working!'
