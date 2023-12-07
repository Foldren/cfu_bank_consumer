from dataclasses import dataclass
from components.responses.children import DAccountBalanceResponse, DPaymentAccountResponse


@dataclass
class ClosePaymentAccountResponse:
    __slots__ = {"id"}
    id: int


@dataclass
class AccountBalancesResponse:
    __slots__ = {"balances"}
    balances: list[DAccountBalanceResponse]


@dataclass
class CreatePaymentAccountResponse:
    __slots__ = {"supportedBankLogoUrl", "bankID", "paymentAccountNumber"}
    supportedBankLogoUrl: str
    bankID: int
    paymentAccountNumber: str


@dataclass
class GetPaymentAccountsResponse:
    __slots__ = {"paymentAccounts"}
    paymentAccounts: list[DPaymentAccountResponse]


@dataclass
class DeletePaymentAccountsResponse:
    __slots__ = {"paymentAccountsID"}
    paymentAccountsID: list[int]

