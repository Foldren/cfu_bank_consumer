from dataclasses import dataclass
from decimal import Decimal
from typing import Union


@dataclass
class DBalance:
    __slots__ = {"balance", "currency"}
    balance: Decimal
    currency: str


@dataclass
class DExpenses:
    __slots__ = {"cash", "nonCash"}
    cash: DBalance
    nonCash: DBalance


@dataclass
class DAccountBalance:
    __slots__ = {"bank", "balance"}
    bank: str
    balance: Union[DBalance, None]


@dataclass
class DCashBalanceOnHand:
    __slots__ = {"fio", "balance"}
    fio: str
    balance: DBalance


@dataclass
class DSupportedBank:
    __slots__ = {"id", "name", "url"}
    id: int
    name: str
    url: str


@dataclass
class DBank:
    __slots__ = {"id", "name", "bankID", "token"}
    id: int
    name: str
    bankID: int
    token: str
