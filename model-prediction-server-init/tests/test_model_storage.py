import tempfile
from model_predicition_server_init.model_storage import ModelStorageClient
import os
import pytest


@pytest.fixture()
def temp_model_file_path():
    temp_model_file_path = os.path.join(tempfile.tempdir, "temp_model.hdf5")
    if os.path.exists(temp_model_file_path):
        os.remove(temp_model_file_path)

    yield temp_model_file_path

    if os.path.exists(temp_model_file_path):
        os.remove(temp_model_file_path)


@pytest.fixture()
def temp_model_rec_file_path():
    temp_model_rec_file_path = os.path.join(tempfile.tempdir, ".model_file_received")
    if os.path.exists(temp_model_rec_file_path):
        os.remove(temp_model_rec_file_path)

    yield temp_model_rec_file_path

    if os.path.exists(temp_model_rec_file_path):
        os.remove(temp_model_rec_file_path)


def test_model_storage_client_model_file_not_downloaded(mocker, temp_model_file_path, temp_model_rec_file_path):
    assert not os.path.exists(temp_model_file_path)
    assert not os.path.exists(temp_model_rec_file_path)

    mocked_pool_manager_request = mocker.patch("urllib3.PoolManager.request")
    mocked_shutil_copy = mocker.patch("shutil.copyfileobj")
    client = ModelStorageClient("http://localhost", tempfile.tempdir, "temp_model.hdf5")
    client.download_model()

    mocked_pool_manager_request.assert_called_once()
    mocked_shutil_copy.assert_called_once()
    assert os.path.exists(temp_model_file_path)
    assert os.path.exists(temp_model_rec_file_path)


def test_model_storage_client_model_file_already_downloaded(mocker, temp_model_file_path, temp_model_rec_file_path):
    with open(temp_model_file_path, mode="a"):
        pass
    with open(temp_model_rec_file_path, mode="a"):
        pass

    mocked_pool_manager_request = mocker.patch("urllib3.PoolManager.request")
    mocked_shutil_copy = mocker.patch("shutil.copyfileobj")
    client = ModelStorageClient("http://localhost", tempfile.tempdir, "temp_model.hdf5")
    client.download_model()

    mocked_pool_manager_request.assert_not_called()
    mocked_shutil_copy.assert_not_called()
    assert os.path.exists(temp_model_file_path)
    assert os.path.exists(temp_model_rec_file_path)


def test_model_storage_client_model_file_already_downloaded_but_received_file_not_created(mocker,
                                                                                          temp_model_file_path,
                                                                                          temp_model_rec_file_path):
    with open(temp_model_file_path, mode="a"):
        pass

    mocked_pool_manager_request = mocker.patch("urllib3.PoolManager.request")
    mocked_shutil_copy = mocker.patch("shutil.copyfileobj")
    client = ModelStorageClient("http://localhost", tempfile.tempdir, "temp_model.hdf5")
    client.download_model()

    mocked_pool_manager_request.assert_called_once()
    mocked_shutil_copy.assert_called_once()
    assert os.path.exists(temp_model_file_path)
    assert os.path.exists(temp_model_rec_file_path)
