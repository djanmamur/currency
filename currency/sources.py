import urllib
from functools import lru_cache
from typing import Dict, List
from  lxml import html
import requests
from bs4 import BeautifulSoup

from .models import BankModel, Bid, CurrencySource, Currency


@lru_cache(maxsize=256)
def get_source_currency(currency_Source: CurrencySource) -> BankModel:
    return BankModel(
        bank_name=currency_Source.name,
        currency_data=CurrencySourceMap[currency_Source](),
    )


def _get_cb_data() -> List[Bid]:
    """
    Retrieve and get Central Bank data
    """
    url: str = "http://cbu.uz/ru/arkhiv-kursov-valyut/json/"
    bank_data: Dict = requests.get(url).json()

    return [
        Bid(
            currency=bank_currency.get("Ccy"),
            buy=bank_currency.get("Rate")
        )
        for bank_currency in bank_data
        if bank_currency.get("Ccy") in Currency.names()
    ]


def _get_ofb_data() -> List[Bid]:
    def _normalize(string) -> str:
        return string.text_content().split("\n")[1].replace("\t", "").replace(" ", "")

    url = "https://ofb.uz/about/kurs-obmena-valyut/"
    page = html.fromstring(requests.get(url).content)
    tr_elements = page.xpath('//tr')

    bids: List[Bid] = []

    for j in range(1, len(tr_elements)):
        T = tr_elements[j]

        currency_name = _normalize(T[0])[:3]
        buy = _normalize(T[2])
        sell = _normalize(T[3])

        bid = Bid(
            currency=currency_name,
            buy=buy,
            sell=sell,
        )
        bids.append(bid)

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
            i.split(" ")[0]
            for i in bank_currency_tag.text.split("\n")
            if i
        ]
        bid = Bid(
            currency=bank_currency[0],
            buy=bank_currency[1],
            sell=bank_currency[2],
        )
        bids.append(bid)

    return bids


CurrencySourceMap: Dict = {
    CurrencySource.CENTRAL_BANK: _get_cb_data,
    CurrencySource.OFB: _get_ofb_data,
    CurrencySource.NBU: _get_nbu_data,
    CurrencySource.KAPITAL_BANK: _get_kapital_bank_data,
}