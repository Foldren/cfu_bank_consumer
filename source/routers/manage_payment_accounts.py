from faststream.rabbit import RabbitRouter
from money import Money

from components.requests.manage_payment_accounts import UserAddCurrentAccountRequest, CloseBankAccountRequest, \
    AccountBalancesRequest
from components.responses.children import DBalanceResponse, DAccountBalanceResponse
from components.responses.manage_payment_accounts import CloseBankAccountResponse, AccountBalancesResponse
from decorators import consumer
from models import PaymentAccount, UserBank
from queues import bank_queue

router = RabbitRouter()


@consumer(router=router, queue=bank_queue, pattern='bank.user-add-current-account',
          request=UserAddCurrentAccountRequest)
async def create_user_payment_accounts(request: UserAddCurrentAccountRequest):
    user_bank = await UserBank.filter(id=request.userBankId, user_id=request.userId).first()

    list_new_pa = []
    for number in request.currentAccounts:
        list_new_pa.append(PaymentAccount(
            legal_entity_id=request.legalEntityId,
            user_bank_id=request.userBankId,
            number=number)
        )

    await user_bank.payment_accounts.add(*list_new_pa)

    # return UserAddCurrentAccountResponse()


@consumer(router=router, queue=bank_queue, pattern="bank.close-user-bank-account", request=CloseBankAccountRequest)
async def close_user_bank_account(request: CloseBankAccountRequest):
    pa = await PaymentAccount.filter(id=request.paymentAccountID, user_bank__user_id=request.userID).first()
    pa.status = 0
    await pa.save()

    return CloseBankAccountResponse(id=request.paymentAccountID)


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
        d_balance = DBalanceResponse(balance=balance.amount, currency="RUB")
        list_d_balances.append(DAccountBalanceResponse(bank=bank, balance=d_balance))

    return AccountBalancesResponse(balances=list_d_balances)