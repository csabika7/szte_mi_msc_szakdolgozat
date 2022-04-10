from flask import Flask
from model_prediction_aggregator.api.v1.routes import api_v1
import os


def get_config():
    conf = dict()
    conf["ACTIVATED_MODEL_DB_SOCKET"] = os.environ["ACTIVATED_MODEL_DB_SOCKET"]
    conf["ACTIVATED_MODEL_KEY"] = os.environ["ACTIVATED_MODEL_KEY"]
    return conf


def create_app(config=None):
    app = Flask(__name__)
    # setup config
    if config:
        app.config.from_mapping(config)
    # setup API
    app.register_blueprint(blueprint=api_v1, url_prefix="/v1/model")

    return app


if __name__ == '__main__':
    app = create_app(get_config())
    app.run(host="0.0.0.0")

