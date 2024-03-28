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


@dataclass
class GetPaymentAccountsRequest:
    __slots__ = {"userID", "bankID"}
    userID: str
    bankID: int


@dataclass
class DeletePaymentAccountsRequest:
    __slots__ = {"paymentAccountsID", "userID", "bankID"}
    paymentAccountsID: list[int]
    bankID: int
    userID: str


@dataclass
class GetApiPaymentAccountsRequest:
    __slots__ = {"bankID", "token"}
    bankID: int
    token: str
