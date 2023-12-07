from faststream.rabbit import RabbitRouter
from components.requests.manage_banks import CreateBankRequest, UpdateUserBankRequest, DeleteUserBanksRequest, \
    GetUserBanksRequest
from components.responses.children import DSupportedBankResponse, DBankResponse, DPaymentAccountResponse
from components.responses.manage_banks import GetSupportedBanksResponse, CreateUserBankResponse, UpdateUserBankResponse, \
    DeleteUserBanksResponse, GetUserBanksResponse
from decorators import consumer
from models import SupportBank, UserBank, PaymentAccount
from queues import bank_queue

router = RabbitRouter()


# @router.subscriber(queue=bank_queue)
# async def purge_messages():
#     pass


@consumer(router=router, queue=bank_queue, pattern="bank.get-supported-banks")
async def get_supported_banks():
    support_banks = await SupportBank.all()
    list_banks = []

    for bank in support_banks:
        list_banks.append(DSupportedBankResponse(id=bank.id, name=bank.name, url=bank.logo_url))

    return GetSupportedBanksResponse(banks=list_banks)


@consumer(router=router, queue=bank_queue, pattern="bank.create-user-bank", request=CreateBankRequest)
async def create_user_bank(request: CreateBankRequest):
    created_bank = await UserBank.create(user_id=request.userID, support_bank_id=request.bankID, name=request.name,
                                         token=request.token.encode())
    bank_p_accounts_n = request.paymentAccountsNumber
    support_bank = await created_bank.support_bank
    list_p_accounts_response = None

    # Если в запросе есть расчетные счета
    if bank_p_accounts_n is not None:
        list_p_accounts_obj = []
        for pa_n in bank_p_accounts_n:
            list_p_accounts_obj.append(
                PaymentAccount(legal_entity_id=request.legalEntityID, user_bank_id=created_bank.id, number=pa_n)
            )

        # Создаем расчетные счета
        await PaymentAccount.bulk_create(list_p_accounts_obj, ignore_conflicts=True)
        created_p_accounts = await PaymentAccount.filter(user_bank_id=created_bank.id)

        # Формируем из них респонсы
        list_p_accounts_response = []
        for pa in created_p_accounts:
            list_p_accounts_response.append(
                DPaymentAccountResponse(id=pa.id, paymentAccountNumber=pa.number, status=pa.status,
                                        legalEntityID=request.legalEntityID)
            )

    return CreateUserBankResponse(id=created_bank.id, name=created_bank.name, bankID=support_bank.id,
                                  bankUrl=support_bank.logo_url, paymentAccounts=list_p_accounts_response)


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


@consumer(router=router, queue=bank_queue, pattern="bank.delete-user-banks", request=DeleteUserBanksRequest)
async def delete_user_banks(request: DeleteUserBanksRequest):
    await UserBank.filter(id__in=request.banksID, user_id=request.userID).delete()

    return DeleteUserBanksResponse(banksID=request.banksID)


@consumer(router=router, queue=bank_queue, pattern="bank.get-user-banks", request=GetUserBanksRequest)
async def get_user_banks(request: GetUserBanksRequest):
    user_banks = await UserBank.filter(user_id=request.userID).prefetch_related("support_bank",
                                                                                "payment_accounts").all()
    list_banks = []

    for bank in user_banks:
        list_payment_accounts = []
        for pa in bank.payment_accounts:
            list_payment_accounts.append(DPaymentAccountResponse(id=pa.id, paymentAccountNumber=pa.number,
                                                                 status=pa.status, legalEntityID=pa.legal_entity_id))

        list_banks.append(
            DBankResponse(
                id=bank.id,
                name=bank.name,
                bankID=bank.support_bank.id,
                supportBankName=bank.support_bank.name,
                token=bank.token.decode('utf-8'),
                paymentAccounts=list_payment_accounts
            )
        )

    return GetUserBanksResponse(banks=list_banks)


@consumer(router=router, queue=bank_queue, pattern="bank.get-user-expenses")
async def get_user_expenses():
    return 'Get user expenses handler is working!'


@consumer(router=router, queue=bank_queue, pattern="bank.get-user-cash-balances-on-hand")
async def get_user_cash_balances_on_hand():
    return 'Get user cash balances on hand handler is working!'
