from faststream.rabbit import RabbitRouter
from config import ContextBody
from decorators import consumer
from models import SupportBank, UserBank, PaymentAccount
from components.requests.manage_banks import CreateBankRequest, UpdateUserBankRequest, DeleteUserBankRequest, GetUserBankRequest, \
    CloseBankAccountRequest, ExpensesRequest
from components.responses.manage_banks import SupportedBankResponse, DSupportedBank, CreateBankResponse, UpdateUserBankResponse, \
    DeleteUserBankResponse, DBank, GetUserBankResponse, CloseBankAccountResponse
from queues import bank_queue

router = RabbitRouter()


# @routers.subscriber(queue=bank_queue)
# async def purge_messages():
#     pass


@consumer(router=router, queue=bank_queue, pattern="bank.get-supported-banks")
async def get_supported_banks():
    support_banks = await SupportBank.all()
    data_list = []

    for bank in support_banks:
        data_list.append(DSupportedBank(id=bank.id, name=bank.name, url=bank.logo_url))

    return SupportedBankResponse(banks=data_list)


@consumer(router=router, queue=bank_queue, pattern="bank.create-user-bank", request=CreateBankRequest)
async def create_user_bank(request: CreateBankRequest):
    created_bank = await UserBank.create(
        user_id=request.userID,
        support_bank_id=request.bankID,
        name=request.name,
        token=request.token.encode(),
    )

    support_bank = await created_bank.support_bank

    return CreateBankResponse(
        id=created_bank.id,
        name=created_bank.name,
        bankID=support_bank.id,
        bankUrl=support_bank.logo_url
    )


@consumer(router=router, queue=bank_queue, pattern="bank.update-user-bank", request=UpdateUserBankRequest)
async def update_user_bank(request: UpdateUserBankRequest):
    user_bank = await UserBank.filter(id=request.id, user_id=request.userID).first()
    support_bank = await user_bank.support_bank

    if request.name:
        user_bank.name = request.name
    if request.token:
        user_bank.token = request.token.encode()

    await user_bank.save()
    await user_bank.refresh_from_db()

    return UpdateUserBankResponse(
        id=user_bank.id,
        name=user_bank.name,
        bankID=support_bank.id,
        bankUrl=support_bank.logo_url
    )


@consumer(router=router, queue=bank_queue, pattern="bank.delete-user-bank", request=DeleteUserBankRequest)
async def delete_user_bank(request: DeleteUserBankRequest = ContextBody):
    await UserBank.filter(id=request.bankID, user_id=request.userID).delete()

    return DeleteUserBankResponse(id=request.bankID)


@consumer(router=router, queue=bank_queue, pattern="bank.get-user-banks", request=GetUserBankRequest)
async def get_user_banks(request: GetUserBankRequest = ContextBody):
    user_banks = await UserBank.filter(user_id=request.userID).select_related("support_bank")
    data_list = []

    for bank in user_banks:
        data_list.append(
            DBank(id=bank.id, name=bank.name, bankID=bank.support_bank.id, token=bank.token.decode('utf-8')))

    return GetUserBankResponse(banks=data_list)


@consumer(router=router, queue=bank_queue, pattern="bank.close-user-bank-account", request=CloseBankAccountRequest)
async def close_user_bank_account(request: CloseBankAccountRequest = ContextBody):
    pa = await PaymentAccount.filter(id=request.paymentAccountID, user_bank__user_id=request.userID).first()
    pa.status = 0
    await pa.save()

    return CloseBankAccountResponse(id=request.paymentAccountID)


@consumer(router=router, queue=bank_queue, pattern="bank.get-user-expenses")
async def get_user_expenses(request: ExpensesRequest = ContextBody):
    return 'Get user expenses handler is working!'


@consumer(router=router, queue=bank_queue, pattern="bank.get-user-account-balances")
async def get_user_account_balances():
    return 'Get user account balances handler is working!'


@consumer(router=router, queue=bank_queue, pattern="bank.get-user-cash-balances-on-hand")
async def get_user_cash_balances_on_hand():
    return 'Get user cash balances on hand handler is working!'
