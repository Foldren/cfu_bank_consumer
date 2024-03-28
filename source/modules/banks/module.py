from asyncio import sleep
from httpx import AsyncClient, ConnectError
from config import PROXY6NET_PROXIES


class Module:
    @staticmethod
    async def get_payment_accounts(token: str) -> list[str]:
        headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

        async with AsyncClient(proxies=PROXY6NET_PROXIES) as async_session:
            while True:
                try:
                    r_company_info = await async_session.post(
                        url="https://api.modulbank.ru/v1/account-info",
                        headers=headers
                    )
                except ConnectError:
                    await sleep(1)
                    continue
                break

            json_company_info = r_company_info.json()

            # Берем номера счетов --------------------------------------------------------------------------------------
            payment_accounts = []
            for pa in json_company_info[0]['bankAccounts']:
                payment_accounts.append(str(pa['number']))

            return payment_accounts
