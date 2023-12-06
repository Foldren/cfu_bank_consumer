from dataclasses import dataclass
from decimal import Decimal
from typing import Union


@dataclass
class DBalanceResponse:
    __slots__ = {"balance", "currency"}
    balance: Decimal
    currency: str


@dataclass
class DExpensesResponse:
    __slots__ = {"cash", "nonCash"}
    cash: DBalanceResponse
    nonCash: DBalanceResponse


@dataclass
class DAccountBalanceResponse:
    __slots__ = {"bank", "balance"}
    bank: str
    balance: Union[DBalanceResponse, None]


@dataclass
class DCashBalanceOnHandResponse:
    __slots__ = {"fio", "balance"}
    fio: str
    balance: DBalanceResponse


@dataclass
class DSupportedBankResponse:
    __slots__ = {"id", "name", "url"}
    id: int
    name: str
    url: str


@dataclass
class DPaymentAccountResponse:
    __slots__ = {"id", "number", "status"}
    id: int
    number: str
    status: bool


@dataclass
class DBankResponse:
    __slots__ = {"id", "name", "bankID", "supportBankName", "token", "paymentAccounts"}
    id: int
    name: str
    bankID: int
    supportBankName: str
    token: str
    paymentAccounts: list[DPaymentAccountResponse]

