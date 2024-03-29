from components.responses.children import CSupportedBankResponse, CBankResponse, CPaymentAccountResponse
from components.responses.bank import GetSupportedBanksResponse, CreateUserBankResponse, UpdateUserBankResponse, \
    DeleteUserBanksResponse, GetUserBanksResponse
from config import STATIC_CATEGORIES
from db_models.bank import UserBank, SupportBank, PaymentAccount
from db_models.telegram import Category
from decorators import consumer
from faststream.rabbit import RabbitRouter
from queues import bank_queue
from components.requests.bank import CreateUserBankRequest, DeleteUserBanksRequest, GetUserBanksRequest, \
    UpdateUserBankRequest

router = RabbitRouter()


@consumer(router=router, queue=bank_queue, pattern="bank.get-supported-banks")
async def get_supported_banks() -> GetSupportedBanksResponse:
    """
    Роут на получение списка поддерживаемых банков
    :return: response объект на получение списка поддерживаемых банков GetSupportedBanksResponse
    """

    support_banks = await SupportBank.all()
    list_banks = []

    for bank in support_banks:
        list_banks.append(CSupportedBankResponse(id=bank.id, name=bank.name, url=bank.logo_url))

    return GetSupportedBanksResponse(banks=list_banks)


@consumer(router=router, queue=bank_queue, pattern="bank.create-user-bank", request=CreateUserBankRequest)
async def create_user_bank(request: CreateUserBankRequest) -> CreateUserBankResponse:
    """
    Роут на создание пользовательского банка, если есть расчетные счета, также прикрепляет их к банку. Дополнительно
    проверяет наличие сервисных и статических категории, при необходимости создает их
    :param request: объект на создание пользовательского банка CreateUserBankRequest
    :return: response объект на создание пользовательского банка CreateUserBankResponse
    """

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
        try:
            await PaymentAccount.bulk_create(list_p_accounts_obj)
        except Exception as e:
            await created_bank.delete()
            raise Exception(e)

        created_p_accounts = await PaymentAccount.filter(user_bank_id=created_bank.id)

        # Формируем из них респонсы
        list_p_accounts_response = []
        for pa in created_p_accounts:
            list_p_accounts_response.append(
                CPaymentAccountResponse(id=pa.id, paymentAccountNumber=pa.number, status=pa.status,
                                        legalEntityID=request.legalEntityID)
            )

    # Проверяем есть ли статические категории
    static_categories = await Category.filter(user_id=request.userID, status=2).all()

    if not static_categories:
        static_categories_obj = []

        for sc in STATIC_CATEGORIES:
            static_categories_obj.append(Category(user_id=request.userID, status=3, name=sc))

        await Category.bulk_create(static_categories_obj, ignore_conflicts=True)

    return CreateUserBankResponse(id=created_bank.id, name=created_bank.name, bankID=support_bank.id,
                                  bankUrl=support_bank.logo_url, paymentAccounts=list_p_accounts_response)


@consumer(router=router, queue=bank_queue, pattern="bank.update-user-bank", request=UpdateUserBankRequest)
async def update_user_bank(request: UpdateUserBankRequest) -> UpdateUserBankResponse:
    """
    Роут на обновление пользовательского банка
    :param request: объект на обновление пользовательского банка UpdateUserBankRequest
    :return: response объект на обновление пользовательского банка UpdateUserBankResponse
    """

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
async def delete_user_banks(request: DeleteUserBanksRequest) -> DeleteUserBanksResponse:
    """
    Роут на удаление пользовательских банков
    :param request: объект на удаление пользовательских банков DeleteUserBanksRequest
    :return: response объект на удаление пользовательских банков DeleteUserBanksResponse
    """

    await UserBank.filter(id__in=request.banksID, user_id=request.userID).delete()

    return DeleteUserBanksResponse(banksID=request.banksID)


@consumer(router=router, queue=bank_queue, pattern="bank.get-user-banks", request=GetUserBanksRequest)
async def get_user_banks(request: GetUserBanksRequest) -> GetUserBanksResponse:
    """
    Роут на получение списка пользовательских банков
    :param request: объект на получение списка пользовательских банков GetUserBanksRequest
    :return: response объект на получение списка пользовательских банков GetUserBanksResponse
    """

    user_banks = await UserBank.filter(user_id=request.userID).prefetch_related("support_bank",
                                                                                "payment_accounts").all()
    list_banks = []

    for bank in user_banks:
        list_payment_accounts = []
        for pa in bank.payment_accounts:
            list_payment_accounts.append(CPaymentAccountResponse(id=pa.id, paymentAccountNumber=pa.number,
                                                                 status=pa.status, legalEntityID=pa.legal_entity_id))

        list_banks.append(
            CBankResponse(
                id=bank.id,
                name=bank.name,
                bankID=bank.support_bank.id,
                supportBankName=bank.support_bank.name,
                token=bank.token.decode('utf-8'),
                paymentAccounts=list_payment_accounts
            )
        )

    return GetUserBanksResponse(banks=list_banks)
