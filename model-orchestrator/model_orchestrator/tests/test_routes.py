import os.path
import pytest
from model_orchestrator import create_app
from pytest_mock.plugin import MockerFixture
import tempfile
import json


@pytest.fixture()
def app():
    token_path = os.path.join(tempfile.tempdir, "token")
    namespace_path = os.path.join(tempfile.tempdir, "namespace")

    with open(token_path, mode="a") as f:
        pass
    with open(namespace_path, mode="a") as f:
        pass


    app = create_app({
        "TESTING": True,
        "MODEL_STORAGE_PROTO": "http",
        "MODEL_STORAGE_HOST": "localhost",
        "MODEL_STORAGE_PORT": "80",
        "SERVICE_ACCOUNT_ROOT": str(tempfile.tempdir),
        "KUBERNETES_SERVICE_HOST": "localhost",
        "KUBERNETES_SERVICE_PORT": "80"
    })

    yield app

    os.remove(token_path)
    os.remove(namespace_path)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_activate_success(mocker: MockerFixture, client):
    mocker.patch("model_orchestrator.api.v1.routes.ModelStorageClient.get_model",
                 new=lambda self, model_id: ({"id": model_id, "name": "TEST_NAME"}, 200))
    mocked_create_mps = \
        mocker.patch("model_orchestrator.kubernetes_api.ModelPredictionServerHandler.create_model_prediction_server")

    result = client.post("/v1/model-orchestrator/model/activate/TEST_ID")

    mocked_create_mps.assert_called_once_with("TEST_ID", "TEST_NAME", mocker.ANY)
    assert result.status_code == 200


def test_activate_not_found(mocker: MockerFixture, client):
    mocker.patch("model_orchestrator.api.v1.routes.ModelStorageClient.get_model",
                 new=lambda self, model_id: (None, 404))

    result = client.post("/v1/model-orchestrator/model/activate/TEST_ID")

    assert result.status_code == 404


def test_activate_fail(mocker: MockerFixture, client):
    mocker.patch("model_orchestrator.api.v1.routes.ModelStorageClient.get_model",
                 new=lambda self, model_id: (None, 500))

    result = client.post("/v1/model-orchestrator/model/activate/TEST_ID")

    assert result.status_code == 500


def test_deactivate_success(mocker: MockerFixture, client):
    mocker.patch("model_orchestrator.api.v1.routes.ModelStorageClient.get_model",
                 new=lambda self, model_id: ({"id": model_id, "name": "TEST_NAME"}, 200))
    mocked_delete_mps = \
        mocker.patch("model_orchestrator.kubernetes_api.ModelPredictionServerHandler.delete_model_prediction_server")

    result = client.post("/v1/model-orchestrator/model/deactivate/TEST_ID")

    mocked_delete_mps.assert_called_once_with("TEST_ID")
    assert result.status_code == 200


def test_deactivate_not_found(mocker: MockerFixture, client):
    mocker.patch("model_orchestrator.api.v1.routes.ModelStorageClient.get_model",
                 new=lambda self, model_id: (None, 404))

    result = client.post("/v1/model-orchestrator/model/deactivate/TEST_ID")

    assert result.status_code == 404


def test_deactivate_fail(mocker: MockerFixture, client):
    mocker.patch("model_orchestrator.api.v1.routes.ModelStorageClient.get_model",
                 new=lambda self, model_id: (None, 500))

    result = client.post("/v1/model-orchestrator/model/deactivate/TEST_ID")

    assert result.status_code == 500


def test_list_success(mocker: MockerFixture, client):
    mocker.patch("model_orchestrator.api.v1.routes.ModelStorageClient.list_models",
                 new=lambda self: ({"models": [{"id": "ID1", "name": "NAME1"}, {"id": "ID2", "name": "NAME2"}]}, 200))
    mocker.patch("model_orchestrator.kubernetes_api.ModelPredictionServerHandler.list_model_prediction_server",
                 new=lambda self: ["ID1"])

    result = client.get("/v1/model-orchestrator/model/list")

    assert result.status_code == 200
    assert json.loads(result.data) == {
        "models": [
            {"id": "ID1", "name": "NAME1", "active": True},
            {"id": "ID2", "name": "NAME2", "active": False}
        ]
    }


def test_list_fail(mocker: MockerFixture, client):
    mocker.patch("model_orchestrator.api.v1.routes.ModelStorageClient.list_models", new=lambda self: (None, 500))

    result = client.get("/v1/model-orchestrator/model/list")

    assert result.status_code == 500
