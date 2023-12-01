from dataclasses import dataclass
from components.responses.children import DExpenses, DCashBalanceOnHand, DSupportedBank, DBank


@dataclass
class SupportedBankResponse:
    banks: list[DSupportedBank]


@dataclass
class CreateBankResponse:
    __slots__ = {"id", "name", "bankID", "bankUrl"}
    id: int
    name: str
    bankID: int
    bankUrl: str


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
class ExpensesResponse:
    __slots__ = {"commodityCosts", "businessExpenses"}
    commodityCosts: DExpenses
    businessExpenses: DExpenses


@dataclass
class CashBalancesOnHandResponse:
    __slots__ = {"cashBalancesOnHand"}
    cashBalancesOnHand: list[DCashBalanceOnHand]
