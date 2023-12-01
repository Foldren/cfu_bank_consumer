from dataclasses import dataclass


@dataclass
class CloseBankAccountRequest:
    __slots__ = {"userID", "paymentAccountID"}
    userID: str
    paymentAccountID: int


@dataclass
class AccountBalancesRequest:
    __slots__ = {"legalEntities", "userID"}
    legalEntities: list[str]
    userID: str


@dataclass
class UserAddCurrentAccountRequest:
    __slots__ = {"userId", "legalEntityId", "userBankId", "currentAccounts"}
    userId: str
    legalEntityId: str
    userBankId: int
    currentAccounts: list[str]
