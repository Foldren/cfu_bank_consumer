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
    id: int
    name: str
    url: str


@dataclass
class SupportedBankResponse:
    banks: list[DSupportedBank]


class IBank:
    id: int
    name: str
    bankID: int
    token: str


class ExpensesResponse:
    commodityCosts: IExpenses
    businessExpenses: IExpenses


class AccountBalancesResponse:
    balances: list[IAccountBalance]


class CashBalancesOnHandResponse:
    cashBalancesOnHand: list[ICashBalanceOnHand]


class CreateBankResponse:
    id: int
    name: str
    bankID: int
    bankUrl: str


class GetUserBankResponse:
    banks: list[IBank]


class UpdateUserBankResponse:
    id: int
    name: str
    bankID: int
    bankUrl: str


class DeleteUserBankResponse:
    id: int


class CloseBankAccountResponse:
    id: int
