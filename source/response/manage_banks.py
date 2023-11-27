from dataclasses import dataclass
from typing import Union


class IBalance:
    balance: int
    currency: str


class IExpenses:
    cash: IBalance
    nonCash: IBalance


class IAccountBalance:
    bank: str
    balance: Union[IBalance, None]


class ICashBalanceOnHand:
    fio: str
    balance: IBalance

@dataclass
class DSupportedBank:
    __slots__ = {"id", "name", "url"}
    id: int
    name: str
    url: str


@dataclass
class SupportedBankResponse:
    __slots__ = {"banks"}

    banks: list[DSupportedBank]

    # async def add_bank(self, bank_id: int, name: str, url: str):
    #     self.banks.append(self.DSupportedBank(id=bank_id, name=name, url=url))


@dataclass
class CreateBankResponse:
    __slots__ = {"id", "name", "bankID", "bankUrl"}
    id: int
    name: str
    bankID: int
    bankUrl: str


@dataclass
class DBank:
    __slots__ = {"id", "name", "bankID", "token"}
    id: int
    name: str
    bankID: int
    token: str


@dataclass
class GetUserBankResponse:
    __slots__ = {"banks"}
    banks: list[DBank]


@dataclass
class UpdateUserBankResponse:
    __slots__ = {"id", "name", "bankID", "bankUrl"}
    id: int
    name: str
    bankID: int
    bankUrl: str


@dataclass
class DeleteUserBankResponse:
    __slots__ = {"id"}
    id: int


@dataclass
class CloseBankAccountResponse:
    __slots__ = {"id"}
    id: int


class ExpensesResponse:
    commodityCosts: IExpenses
    businessExpenses: IExpenses


class AccountBalancesResponse:
    balances: list[IAccountBalance]


class CashBalancesOnHandResponse:
    cashBalancesOnHand: list[ICashBalanceOnHand]
