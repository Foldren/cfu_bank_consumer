from dataclasses import dataclass


@dataclass
class ClosePaymentAccountRequest:
    __slots__ = {"userID", "bankID", "paymentAccountID"}
    userID: str
    bankID: int
    paymentAccountID: int


@dataclass
class AccountBalancesRequest:
    __slots__ = {"legalEntities", "userID"}
    legalEntities: list[str]
    userID: str


@dataclass
class CreatePaymentAccountRequest:
    __slots__ = {"paymentAccountNumber", "userID", "bankID", "legalEntityID"}
    paymentAccountNumber: str
    userID: str
    bankID: int
    legalEntityID: str
