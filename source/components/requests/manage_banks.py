from dataclasses import dataclass


@dataclass
class CashBalancesOnHandRequest:
    __slots__ = {"legalEntities", "userID"}
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
class ExpensesRequest:
    __slots__ = {"dateFrom", "dateTo", "legalEntities", "userID"}
    dateFrom: str
    dateTo: str
    legalEntities: list[str]
    userID: str
