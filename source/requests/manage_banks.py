class ExpensesRequest:
    dateFrom: str
    dateTo: str
    legalEntities: list[str]
    userID: str


class AccountBalancesRequest:
    legalEntities: list[str]
    userID: str


class CashBalancesOnHandRequest:
    legalEntities: list[str]
    userID: str


class CreateBankRequest:
    bankID: int
    name: str
    token: str
    userID: str


class GetUserBankRequest:
    userID: str


class UpdateUserBankRequest:
    id: int
    name: str = ""
    token: str = ""
    userID: str


class DeleteUserBankRequest:
    userID: str
    bankID: int


class CloseBankAccountRequest:
    userID: str
    paymentAccountID: int
