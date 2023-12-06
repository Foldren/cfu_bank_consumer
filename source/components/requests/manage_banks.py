from dataclasses import dataclass
from components.requests.children import DPaymentAccountRequest


@dataclass
class CashBalancesOnHandRequest:
    __slots__ = {"legalEntities", "userID"}
    legalEntities: list[str]
    userID: str


@dataclass
class CreateBankRequest:
    bankID: int
    name: str
    token: str
    userID: str
    paymentAccounts: list[DPaymentAccountRequest] = None


@dataclass
class UpdateUserBankRequest:
    id: int
    userID: str
    name: str = None
    token: str = None


@dataclass
class DeleteUserBanksRequest:
    __slots__ = {"userID", "banksID"}
    userID: str
    banksID: list[int]


@dataclass
class GetUserBanksRequest:
    __slots__ = {"userID"}
    userID: str


@dataclass
class ExpensesRequest:
    __slots__ = {"dateFrom", "dateTo", "legalEntities", "userID"}
    dateFrom: str
    dateTo: str
    legalEntities: list[str]
    userID: str
