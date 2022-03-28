import pytest
from model_storage import create_app, init_database
import os
import shutil
import tempfile


@pytest.fixture()
def app():
    db_path = os.path.join(tempfile.tempdir, "temp.db")
    upload_path = os.path.join(tempfile.tempdir, "model_uploads")
    os.mkdir(upload_path)
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///{}".format(db_path)
    })

    init_database(app)

    os.environ["MODEL_STORAGE_PATH"] = str(upload_path)

    yield app

    shutil.rmtree(upload_path)
    os.remove(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
