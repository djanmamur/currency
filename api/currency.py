import json
from dataclasses import asdict

from flask import Blueprint, jsonify

from currency.models import CurrencySource
from currency.sources import get_source_currency

blueprint = Blueprint("menu", __name__)


@blueprint.route("/currency", methods=["GET"])
def get_currency() -> json:
    return jsonify(
        asdict(get_source_currency(CurrencySource.CENTRAL_BANK)),
        asdict(get_source_currency(CurrencySource.OFB)),
        asdict(get_source_currency(CurrencySource.NBU)),
        asdict(get_source_currency(CurrencySource.KAPITAL_BANK)),
    )
