from dataclasses import dataclass
from enum import IntEnum, unique
from typing import List


@unique
class EnumBase(IntEnum):
    def __new__(cls, value: int, fullName: str, shortName: str = ""):
        obj = int.__new__(cls, value)

        obj._value_ = value
        obj.fullName = fullName
        obj.shortName = shortName

        return obj

    @classmethod
    def names(cls):
        return [c.name for c in list(cls)]


class Currency(EnumBase):
    EUR = (
        1,
        "Euro",
        "Евро",
    )
    USD = (
        2,
        "United States dollar",
        "Доллары США",
    )
    GBP = (
        3,
        "British Pound",
        "Фунт Стерлинг",
    )
    RUB = (
        4,
        "Russian Roubles",
        "Российский Рубль",
    )


@dataclass
class Bid:
    currency: Currency
    buy: str = "-"
    sell: str = "-"


class CurrencySource(EnumBase):
    CENTRAL_BANK = (
        1,
        "Central Bank",
        "Центральный Банк",
    )
    OFB = (
        2,
        "Orient Finance Bank",
        "Ориент Финанс Банк",
    )
    NBU = (
        3,
        "National Bank of Uzbekistan",
        "Национальный Банк Узбекистана",
    )
    KAPITAL_BANK = (
        4,
        "Kapital Bank",
        "Капитал Банк",
    )


@dataclass
class BankModel:
    bank_name: str
    currency_data: List[Bid]
