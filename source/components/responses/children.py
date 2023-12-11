from dataclasses import dataclass
from decimal import Decimal
from typing import Union


@dataclass
class DBalanceResponse:
    __slots__ = {"balance", "currency"}
    balance: Decimal
    currency: str


@dataclass
class DAccountBalanceResponse:
    __slots__ = {"bank", "balance"}
    bank: str
    balance: Union[DBalanceResponse, None]


@dataclass
class DSupportedBankResponse:
    __slots__ = {"id", "name", "url"}
    id: int
    name: str
    url: str


@dataclass
class DPaymentAccountResponse:
    id: int
    paymentAccountNumber: str
    legalEntityID: str
    status: bool
    bankID: int = None
    supportedBankLogo: str = None


@dataclass
class DBankResponse:
    __slots__ = {"id", "name", "bankID", "supportBankName", "token", "paymentAccounts"}
    id: int
    name: str
    bankID: int
    supportBankName: str
    token: str
    paymentAccounts: list[DPaymentAccountResponse]
