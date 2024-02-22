from tortoise import Tortoise
from config import TORTOISE_CONFIG
from models import SupportBank


async def init_db():
    await Tortoise.init(TORTOISE_CONFIG)
    await Tortoise.generate_schemas(safe=True)

    support_banks = await SupportBank.all()

    if not support_banks:
        support_bank_list = [
            SupportBank(name="Тинькофф"),
            SupportBank(name="Модуль"),
            SupportBank(name="Точка"),
        ]

        await SupportBank.bulk_create(support_bank_list)
