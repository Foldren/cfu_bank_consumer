from tortoise import Tortoise
from config import POSTGRES_URL
from models import SupportBank


async def init_db():
    await Tortoise.init(
        db_url=POSTGRES_URL,
        modules={'models': ["models"]},
    )
    await Tortoise.generate_schemas(safe=True)
    support_banks = await SupportBank.all()

    if not support_banks:
        support_bank_list = [
            SupportBank(name="Тинькофф"),
            SupportBank(name="Модуль"),
            SupportBank(name="Точка"),
        ]

        await SupportBank.bulk_create(support_bank_list)
