from dataclasses import dataclass
from components.responses.children import DAccountBalanceResponse


@dataclass
class CloseBankAccountResponse:
    __slots__ = {"id"}
    id: int


@dataclass
class AccountBalancesResponse:
    __slots__ = {"balances"}
    balances: list[DAccountBalanceResponse]


@dataclass
class UserAddCurrentAccountResponse:
    __slots__ = {"userId", "legalEntityId", "userBankId", "currentAccounts"}
    paymentAccountsId: list[int]
    supportedBankId: int
    currentAccounts: list[str]
