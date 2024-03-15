from faststream.rabbit import RabbitRouter
from money import Money
from components.requests.payment_account import CreatePaymentAccountRequest, ClosePaymentAccountRequest, \
    AccountBalancesRequest, GetPaymentAccountsRequest, DeletePaymentAccountsRequest
from components.responses.children import CBalanceResponse, CAccountBalanceResponse, CPaymentAccountResponse
from components.responses.payment_account import ClosePaymentAccountResponse, AccountBalancesResponse, \
    CreatePaymentAccountResponse, GetPaymentAccountsResponse, DeletePaymentAccountsResponse
from db_models.bank import UserBank, PaymentAccount
from decorators import consumer
from queues import bank_queue

router = RabbitRouter()


@consumer(router=router, queue=bank_queue, pattern='bank.create-user-payment-account',
          request=CreatePaymentAccountRequest)
async def create_payment_account(request: CreatePaymentAccountRequest):
    user_bank = await UserBank.filter(id=request.bankID, user_id=request.userID).all()

    if user_bank:
        await PaymentAccount.create(
            legal_entity_id=request.legalEntityID,
            user_bank_id=request.bankID,
            number=request.paymentAccountNumber
        )

        pa_bank = await UserBank.filter(id=request.bankID).select_related("support_bank").first()

        return CreatePaymentAccountResponse(
            supportedBankLogoUrl=pa_bank.support_bank.logo_url,
            bankID=pa_bank.id,
            paymentAccountNumber=request.paymentAccountNumber
        )
    else:
        raise Exception("This bank does not belong to the user!")


@consumer(router=router, queue=bank_queue, pattern="bank.close-user-bank-account", request=ClosePaymentAccountRequest)
async def close_payment_account(request: ClosePaymentAccountRequest):
    pa = await PaymentAccount.filter(id=request.paymentAccountID, user_bank__user_id=request.userID,
                                     user_bank_id=request.bankID).first()
    pa.status = 0
    await pa.save()

    return ClosePaymentAccountResponse(id=request.paymentAccountID)


@consumer(router=router, queue=bank_queue, pattern="bank.get-user-account-balances", request=AccountBalancesRequest)
async def get_user_account_balances(request: AccountBalancesRequest):
    selected_pa = await PaymentAccount \
        .filter(user_bank__user_id=request.userID, legal_entity_id__in=request.legalEntities) \
        .select_related("user_bank__support_bank")

    # Пробегаемся по счетам и складываем балансы для каждого банка -----------------------------------------------------
    list_bank_balances = {}
    for pa in selected_pa:
        pa_sup_bank_name = pa.user_bank.support_bank.name.split(".")[0]
        if pa_sup_bank_name not in list_bank_balances:
            list_bank_balances[pa_sup_bank_name] = Money(amount=pa.balance, currency="RUB")
        else:
            list_bank_balances[pa_sup_bank_name] = list_bank_balances[pa_sup_bank_name] + Money(amount=pa.balance,
                                                                                                currency="RUB")

    list_d_balances = []
    for bank, balance in list_bank_balances.items():
        d_balance = CBalanceResponse(balance=balance.amount, currency="RUB")
        list_d_balances.append(CAccountBalanceResponse(bank=bank, balance=d_balance))

    return AccountBalancesResponse(balances=list_d_balances)


@consumer(router=router, queue=bank_queue, pattern="bank.get-user-payment-accounts", request=GetPaymentAccountsRequest)
async def get_payment_accounts(request: GetPaymentAccountsRequest):
    p_accounts = await PaymentAccount \
        .filter(user_bank_id=request.bankID, user_bank__user_id=request.userID) \
        .select_related("user_bank__support_bank") \
        .all()

    list_p_accounts = []
    for pa in p_accounts:
        list_p_accounts.append(CPaymentAccountResponse(id=pa.id, paymentAccountNumber=pa.number, status=pa.status,
                                                       legalEntityID=pa.legal_entity_id,
                                                       supportedBankLogo=pa.user_bank.support_bank.logo_url))

    return GetPaymentAccountsResponse(paymentAccounts=list_p_accounts)


@consumer(router=router, queue=bank_queue, pattern="bank.delete-user-payment-accounts",
          request=DeletePaymentAccountsRequest)
async def delete_payment_accounts(request: DeletePaymentAccountsRequest):
    p_accounts = await PaymentAccount.filter(id__in=request.paymentAccountsID, user_bank_id=request.bankID,
                                             user_bank__user_id=request.userID).all()
    for pa in p_accounts:
        await pa.delete()

    return DeletePaymentAccountsResponse(paymentAccountsID=request.paymentAccountsID)
