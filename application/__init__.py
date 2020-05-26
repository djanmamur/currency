from flask import Flask

from api import currency
from settings import ProductionConfig


def create_app(config_object=ProductionConfig):
    application = Flask(__name__)
    application.config.from_object(config_object)

    register_blueprints(application)
    # register_error_handlers(application)

    return application


def register_blueprints(application):
    application.register_blueprint(currency.blueprint)


def register_error_handlers(app):
    def error_handler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(Exception)(error_handler)

