from dataclasses import dataclass


class AccountBalancesRequest:
    legalEntities: list[str]
    userID: str


class CashBalancesOnHandRequest:
    legalEntities: list[str]
    userID: str


@dataclass
class CreateBankRequest:
    __slots__ = {"bankID", "name", "token", "userID"}
    bankID: int
    name: str
    token: str
    userID: str


@dataclass
class UpdateUserBankRequest:
    id: int
    userID: str
    name: str = None
    token: str = None


@dataclass
class DeleteUserBankRequest:
    __slots__ = {"userID", "bankID"}
    userID: str
    bankID: int


@dataclass
class GetUserBankRequest:
    __slots__ = {"userID"}
    userID: str


@dataclass
class CloseBankAccountRequest:
    __slots__ = {"userID", "paymentAccountID"}
    userID: str
    paymentAccountID: int


@dataclass
class ExpensesRequest:
    __slots__ = {"dateFrom", "dateTo", "legalEntities", "userID"}
    dateFrom: str
    dateTo: str
    legalEntities: list[str]
    userID: str
