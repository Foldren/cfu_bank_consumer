from dataclasses import asdict
from json import dumps
from response.rpc import RpcResponse, RpcError


def rpc_exception(func):
    def wrapper():
        response = RpcResponse()
        try:
            func(response)
        except Exception as e:
            response.error = RpcError(message=str(e))
            response.data = None
        return dumps(asdict(response, dict_factory=lambda x: {k: v for (k, v) in x if v is not None}))
    return wrapper
