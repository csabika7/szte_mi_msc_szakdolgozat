import os
import pytest

os.environ["MODEL_DATA_VOLUME"] = str(os.path.join(os.getcwd(), "resources"))
os.environ["MODEL_FILE_NAME"] = "dummy_model.hdf5"

from model_prediction_server import create_app


@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
