from dataclasses import dataclass
from components.responses.children import DSupportedBankResponse, DBankResponse, DPaymentAccountResponse


@dataclass
class GetSupportedBanksResponse:
    banks: list[DSupportedBankResponse]


@dataclass
class CreateUserBankResponse:
    id: int
    name: str
    bankID: int
    bankUrl: str
    paymentAccounts: list[DPaymentAccountResponse] = None


@dataclass
class GetUserBanksResponse:
    __slots__ = {"banks"}
    banks: list[DBankResponse]


@dataclass
class UpdateUserBankResponse:
    __slots__ = {"id", "name", "bankID", "bankUrl"}
    id: int
    name: str
    bankID: int
    bankUrl: str


@dataclass
class DeleteUserBanksResponse:
    __slots__ = {"banksID"}
    banksID: list[int]
