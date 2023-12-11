from dataclasses import dataclass


@dataclass
class CreateBankRequest:
    bankID: int
    name: str
    token: str
    userID: str
    legalEntityID: str = None
    paymentAccountsNumber: list[str] = None


@dataclass
class UpdateUserBankRequest:
    id: int
    userID: str
    name: str = None
    token: str = None


@dataclass
class DeleteUserBanksRequest:
    __slots__ = {"userID", "banksID"}
    userID: str
    banksID: list[int]


@dataclass
class GetUserBanksRequest:
    __slots__ = {"userID"}
    userID: str