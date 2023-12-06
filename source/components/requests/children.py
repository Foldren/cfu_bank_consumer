from dataclasses import dataclass


@dataclass
class DPaymentAccountRequest:
    __slots__ = {"number", "status", "legalEntityID"}
    number: str
    status: bool
    legalEntityID: str
