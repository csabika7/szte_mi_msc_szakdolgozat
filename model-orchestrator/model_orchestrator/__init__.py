from flask import Flask
import os
from model_orchestrator.api.v1.routes import api_v1


def get_config():
    conf = dict()

    conf["MODEL_STORAGE_PROTO"] = os.environ["MODEL_STORAGE_PROTO"]
    conf["MODEL_STORAGE_HOST"] = os.environ["MODEL_STORAGE_HOST"]
    conf["MODEL_STORAGE_PORT"] = os.environ["MODEL_STORAGE_PORT"]

    conf["KUBERNETES_SERVICE_HOST"] = os.environ["KUBERNETES_SERVICE_HOST"]
    conf["KUBERNETES_SERVICE_PORT"] = os.environ["KUBERNETES_SERVICE_PORT"]
    conf["SERVICE_ACCOUNT_ROOT"] = "/var/run/secrets/kubernetes.io/serviceaccount"

    conf["REDIS_HOST"] = os.environ["REDIS_HOST"]
    conf["REDIS_PORT"] = os.environ["REDIS_PORT"]
    conf["REDIS_CHANNEL"] = os.environ["REDIS_CHANNEL"]
    return conf


def create_app(config=None):
    app = Flask(__name__)
    # setup config
    if config:
        app.config.from_mapping(config)
    # setup API
    app.register_blueprint(blueprint=api_v1, url_prefix="/v1/model-orchestrator")

    return app


if __name__ == '__main__':
    app = create_app(get_config())
    app.run(host="0.0.0.0")

