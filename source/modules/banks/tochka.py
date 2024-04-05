from httpx import AsyncClient
from config import PROXY6NET_PROXIES


class Tochka:
    @staticmethod
    async def get_payment_accounts(token: str) -> list[str]:
        headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

        async with AsyncClient(proxies=PROXY6NET_PROXIES) as async_session:
            r_accounts = await async_session.get(
                url="https://enter.tochka.com/uapi/open-banking/v1.0/accounts",
                headers=headers
            )

            if r_accounts.status_code != 200:
                raise Exception(f"[error]: Error on api tochka on operation get balances:\n\n {r_accounts.text}")

            json_balances = r_accounts.json()["Data"]["Account"]

            # Получаем балансы -----------------------------------------------------------------------------------------
            payment_accounts = []
            for pa in json_balances:
                pa_number = pa['accountId'].split("/")[0]
                payment_accounts.append(pa_number)

            return payment_accounts
