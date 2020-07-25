import json
from dataclasses import asdict

from flask import Blueprint, jsonify, request

from currency.models import CurrencySource
from currency.sources import get_source_currency, get_currency_by_rate

blueprint = Blueprint("currency", __name__)


@blueprint.route("/currency", methods=["GET"])
def get_currency(currency_id: int = None) -> json:
    if request.args.get("by") == "rate":
        return jsonify(get_currency_by_rate())
    return jsonify(
        asdict(get_source_currency(CurrencySource.CENTRAL_BANK)),
        asdict(get_source_currency(CurrencySource.OFB)),
        asdict(get_source_currency(CurrencySource.NBU)),
        asdict(get_source_currency(CurrencySource.KAPITAL_BANK)),
    )
