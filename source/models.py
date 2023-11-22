from enum import IntEnum, Enum
from tortoise import Model
from tortoise.fields import BigIntField, ForeignKeyRelation, ForeignKeyField, ReverseRelation, TextField, OnDelete, \
    BinaryField, DateField, IntEnumField, BooleanField, CharField, CharEnumField, DecimalField


class SupportBank(Model):
    id = BigIntField(pk=True)
    name = CharField(max_length=50, null=False)
    logo_url = TextField(maxlength=320, null=False)
    user_banks: ReverseRelation['UserBank']

    class Meta:
        table = "support_banks"


class UserBank(Model):
    id = BigIntField(pk=True)
    user_id = CharField(max_length=100, null=False, index=True)
    support_bank: ForeignKeyRelation['SupportBank'] = ForeignKeyField('models.SupportBank', on_delete=OnDelete.CASCADE,
                                                                      related_name="user_banks", null=False)
    payment_accounts: ReverseRelation['PaymentAccount']
    name = CharField(max_length=50, null=False)
    token = BinaryField(null=False)

    class Meta:
        table = "user_banks"


class PaymentAccountStatus(IntEnum):
    active = 1
    close = 0


class PaymentAccount(Model):
    id = BigIntField(pk=True)
    legal_entity_id = CharField(max_length=100, null=False, index=True)
    user_bank: ForeignKeyRelation['UserBank'] = ForeignKeyField('models.UserBank', on_delete=OnDelete.CASCADE,
                                                                related_name="payment_accounts", null=False)
    data_collects: ReverseRelation['PaymentAccount']
    start_date = DateField(null=False)
    last_date = DateField(null=True)
    number = BigIntField(null=False)
    status = IntEnumField(enum_type=PaymentAccountStatus, description="Статус расчётного счета", default=1)

    class Meta:
        table = "payment_accounts"


class DataCollectType(str, Enum):
    income = "Доход"
    cost = "Расход"


class DataCollectWallet(str, Enum):
    tinkoff = "Тинькофф"
    module = "Модуль"
    tochka = "Точка"
    ozon = "Ozon"


class DataCollect(Model):
    id = BigIntField(pk=True)
    payment_account: ForeignKeyRelation['PaymentAccount'] = ForeignKeyField('models.PaymentAccount',
                                                                            on_delete=OnDelete.CASCADE,
                                                                            related_name="data_collects", null=True)
    trxn_date = DateField(null=False, index=True)
    executor_chat_id = CharField(max_length=50, default='Нет chat_id', null=True)
    executor_name = CharField(max_length=100, null=False)
    type = CharEnumField(enum_type=DataCollectType, description='Тип операции', null=False)
    wallet = CharEnumField(enum_type=DataCollectWallet, description='Кошелек', null=False)
    amount = DecimalField(max_digits=19, decimal_places=2, null=False)
    org_name = CharField(max_length=100, null=False)
    contragent_inn = CharField(max_length=19, default='', null=True)

    class Meta:
        table = "data_collects"


# class Contragent():
#     id = BigIntField(pk=True)
#     user_id = CharField(max_length=100, index=True, null=False)
#     category: ForeignKeyRelation['Category'] = ForeignKeyField('models.Category',
#                                                                on_delete=OnDelete.CASCADE,
#                                                                related_name="contragents", null=False)
#     inn = BigIntField(null=False, unique=True)
#     name = CharField(max_length=50, null=False)
#
#     class Meta:
#         table = "contragents"
#
#
# class CategoryLevel(IntEnum):
#     one = 1
#     two = 2
#     three = 3
#     four = 4
#     five = 5
#
#
# class Category():
#     id = BigIntField(pk=True)
#     parent: ForeignKeyRelation['Category'] = ForeignKeyField('models.Category', on_delete=OnDelete.CASCADE,
#                                                              related_name="child_categories", null=True)
#     child_categories: ReverseRelation["Category"]  # Связь один ко многим к самому себе (выводим дочерние элементы)
#     contragents: ReverseRelation['Contragent']
#     name = CharField(max_length=50, null=False)
#     status = BooleanField(default=1)
#     level = IntEnumField(enum_type=CategoryLevel, description="Уровень вложенности категории", default=1)
#
#     class Meta:
#         table = "categories"
