from dataclasses import dataclass

from components.responses.children import DAccountBalance


@dataclass
class CloseBankAccountResponse:
    __slots__ = {"id"}
    id: int


@dataclass
class AccountBalancesResponse:
    __slots__ = {"balances"}
    balances: list[DAccountBalance]


@dataclass
class UserAddCurrentAccountResponse:
    __slots__ = {"userId", "legalEntityId", "userBankId", "currentAccounts"}
    paymentAccountId: int
    supportedBankId: int
    currentAccounts: list[str]
