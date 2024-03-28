from httpx import AsyncClient
from config import PROXY6NET_PROXIES


class Tinkoff:
    @staticmethod
    async def get_payment_accounts(token: str):
        headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}
        url_operation = 'https://business.tinkoff.ru/openapi/api/v1/bank-accounts'

        async with AsyncClient(proxies=PROXY6NET_PROXIES) as async_session:
            r_balances = await async_session.get(
                url=url_operation,
                headers=headers
            )

        json_balances_list = r_balances.json()

        payment_accounts = []
        for pa in json_balances_list:
            payment_accounts.append(str(pa['accountNumber']))

        return payment_accounts
