from dataclasses import dataclass
from decimal import Decimal
from typing import Union


@dataclass
class CBalanceResponse:
    __slots__ = {"balance", "currency"}
    balance: Decimal
    currency: str


@dataclass
class CAccountBalanceResponse:
    __slots__ = {"bank", "balance"}
    bank: str
    balance: Union[CBalanceResponse, None]


@dataclass
class CSupportedBankResponse:
    __slots__ = {"id", "name", "url"}
    id: int
    name: str
    url: str


@dataclass
class CPaymentAccountResponse:
    id: int
    paymentAccountNumber: str
    legalEntityID: str
    status: bool
    bankID: int = None
    supportedBankLogo: str = None


@dataclass
class CBankResponse:
    __slots__ = {"id", "name", "bankID", "supportBankName", "token", "paymentAccounts"}
    id: int
    name: str
    bankID: int
    supportBankName: str
    token: str
    paymentAccounts: list[CPaymentAccountResponse]


@dataclass
class CDataCollectResponse:
    __slots__ = {"legalEntity", "counterpartyInn", "amount", "type"}
    legalEntity: str
    counterpartyInn: str
    amount: Decimal
    type: str
