import traceback
from http import HTTPStatus

from flask import Flask, jsonify, json

from api import currency
from settings import ProductionConfig


def create_app(config_object=ProductionConfig):
    application = Flask(__name__)
    application.config.from_object(config_object)

    register_blueprints(application)
    register_error_handlers(application)

    return application


def register_blueprints(application):
    application.register_blueprint(currency.blueprint)


def register_error_handlers(app):
    def _handle_response(message: str) -> json:
        return jsonify({
            "error": message
        })

    def handle_not_found(e):
        return _handle_response("page not found")

    def handle_unknown_exception(e):
        traceback.print_exc()
        return _handle_response(e.args)

    app.errorhandler(HTTPStatus.NOT_FOUND)(handle_not_found)
    app.errorhandler(Exception)(handle_unknown_exception)


