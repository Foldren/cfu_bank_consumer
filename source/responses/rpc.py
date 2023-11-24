from dataclasses import dataclass, field
from typing import Any


@dataclass
class RpcError:
    message: str
    statusCode: int = 400


@dataclass
class RpcResponse:
    data: Any = None
    error: RpcError = None
