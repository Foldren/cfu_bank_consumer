from dataclasses import dataclass
from components.responses.children import CSupportedBankResponse, CBankResponse, CPaymentAccountResponse


@dataclass
class GetSupportedBanksResponse:
    banks: list[CSupportedBankResponse]


@dataclass
class CreateUserBankResponse:
    id: int
    name: str
    bankID: int
    bankUrl: str
    paymentAccounts: list[CPaymentAccountResponse] = None


@dataclass
class GetUserBanksResponse:
    __slots__ = {"banks"}
    banks: list[CBankResponse]


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
