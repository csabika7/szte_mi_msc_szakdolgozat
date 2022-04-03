from model_orchestrator.model_store import ModelStorageClient
from pytest_mock.plugin import MockerFixture
from urllib3.response import HTTPResponse


def test_get_model_success(mocker: MockerFixture):
    mocker.patch("urllib3.PoolManager.request",
                 new=lambda *args, **kwargs: HTTPResponse(status=200, body=b'{"id": "TEST_ID", "name": "TEST_NAME"}'))

    client = ModelStorageClient("http", "localhost", "80")

    model = client.get_model("TEST_ID")

    assert model == ({"id": "TEST_ID", "name": "TEST_NAME"}, 200)


def test_get_model_not_found(mocker: MockerFixture):
    mocker.patch("urllib3.PoolManager.request",
                 new=lambda *args, **kwargs: HTTPResponse(status=404))

    client = ModelStorageClient("http", "localhost", "80")

    model = client.get_model("TEST_ID")

    assert model == (None, 404)


def test_list_model_success(mocker: MockerFixture):
    mocker.patch("urllib3.PoolManager.request",
                 new=lambda *args, **kwargs: HTTPResponse(status=200,
                                                          body=b'{"models": [{"id": "TEST_ID", "name": "TEST_NAME"}]}'))

    client = ModelStorageClient("http", "localhost", "80")

    model = client.list_models()

    assert model == ({"models": [{"id": "TEST_ID", "name": "TEST_NAME"}]}, 200)


def test_list_model_fail(mocker: MockerFixture):
    mocker.patch("urllib3.PoolManager.request",
                 new=lambda *args, **kwargs: HTTPResponse(status=500))

    client = ModelStorageClient("http", "localhost", "80")

    model = client.list_models()

    assert model == (None, 500)
