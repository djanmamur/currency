import urllib
from functools import lru_cache
from typing import Callable, Dict, DefaultDict, List
import bs4
import sys
from logging import getLogger
import requests
from collections import defaultdict
from bs4 import BeautifulSoup
from lxml import html

logger = getLogger(__name__)

bs4.sys = sys  # BS4 fails with `sys` not found without this monkeypatch

from .models import BankModel, Bid, CurrencySource, Currency


def get_currency_by_rate() -> DefaultDict:
    currencies_by_bank: List[BankModel] = [
        get_source_currency(currency) for currency in CurrencySource
    ]

    currencies_by_rate = defaultdict(list)
    for bank_currency in currencies_by_bank:
        for currency in bank_currency.currency_data:
            currencies_by_rate[currency.currency].append(
                {bank_currency.bank_name: {"buy": currency.buy, "sell": currency.sell,}}
            )

    return currencies_by_rate


@lru_cache(maxsize=256)
def get_source_currency(currency_source: CurrencySource) -> BankModel:
    return BankModel(
        bank_name=currency_source.name,
        currency_data=CurrencySourceMap[currency_source](),
    )


def _get_cb_data() -> List[Bid]:
    """
    Retrieve and get Central Bank data
    """
    url: str = "http://cbu.uz/ru/arkhiv-kursov-valyut/json/"
    bank_data: Dict = requests.get(url).json()

    return [
        Bid(currency=bank_currency.get("Ccy"), buy=bank_currency.get("Rate"))
        for bank_currency in bank_data
        if bank_currency.get("Ccy") in Currency.names()
    ]


def _get_ofb_data() -> List[Bid]:
    def _normalize(string) -> str:
        return string.text_content().split("\n")[1].replace("\t", "").replace(" ", "")

    url = "https://ofb.uz/about/kurs-obmena-valyut/"
    page = html.fromstring(requests.get(url).content)
    tr_elements = page.xpath("//tr")

    bids: List[Bid] = []
    try:
        for j in range(1, len(tr_elements)):
            T = tr_elements[j]

            currency_name = _normalize(T[0])[:3]
            buy_rate = _normalize(T[2])
            sell_rate = _normalize(T[3])

            bid = Bid(currency_name, buy_rate, sell_rate)
        bids.append(bid)
    except Exception as e:
        logger.warning(f"Error occurred while fetching OFB data: {e}")

    return bids


def _get_nbu_data() -> List[Bid]:
    url: str = "https://nbu.uz/exchange-rates/json/"
    bank_data: Dict = requests.get(url).json()

    return [
        Bid(
            currency=bank_currency.get("code"),
            buy=bank_currency.get("nbu_buy_price"),
            sell=bank_currency.get("nbu_cell_price"),
        )
        for bank_currency in bank_data
        if bank_currency.get("code") in Currency.names()
    ]


def _get_kapital_bank_data() -> List[Bid]:
    url = "https://kapitalbank.uz/ru/services/exchange-rates"
    soup = BeautifulSoup(urllib.request.urlopen(url).read())

    bids: List[Bid] = []

    for currency_name in Currency.names():
        bank_currency_tag = soup.find("div", class_=f"item-{currency_name.lower()}")
        bank_currency = [
            i.split(" ")[0] for i in bank_currency_tag.text.split("\n") if i
        ]

        currency_name, buy_rate, sell_rate, *_ = bank_currency
        bids.append(Bid(currency_name, buy_rate, sell_rate))
    return bids


CurrencySourceMap: Dict[CurrencySource, Callable] = {
    CurrencySource.OFB: _get_ofb_data,
    CurrencySource.NBU: _get_nbu_data,
    CurrencySource.CENTRAL_BANK: _get_cb_data,
    CurrencySource.KAPITAL_BANK: _get_kapital_bank_data,
}
