from pathlib import Path
import uuid

# CONSTANTS
UPLOAD_ROUTE = "/v1/model-store/model"
DOWNLOAD_ROUTE = "/v1/model-store/model/download/{}"
GET_ROUTE = "/v1/model-store/model/{}"
LIST_ROUTE = "/v1/model-store/model/list"
DELETE_ROUTE = "/v1/model-store/model/{}"

RESOURCES_DIR = Path(__file__).parent / "resources"
DUMM_MODEL_FILE = RESOURCES_DIR / "dummy_model.hdf5"


# UTILITY METHODS


def upload_model_and_assert(client):
    post_response = client.post(UPLOAD_ROUTE, data={
        "name": "test",
        "model_file": DUMM_MODEL_FILE.open("rb")
    })
    assert post_response.status_code == 200
    assert post_response.data != b''
    model_id = post_response.data.decode("utf-8")
    return model_id


def get_model_and_assert(client, model_id):
    get_response = client.get(GET_ROUTE.format(model_id))

    assert get_response.status_code == 200
    json_obj = get_response.json
    assert json_obj["name"] == "test"
    assert json_obj["id"] == model_id


def list_models_and_assert(client, model_id):
    get_response = client.get(LIST_ROUTE)
    json_obj = get_response.json
    assert json_obj["models"][0]["name"] == "test"
    assert json_obj["models"][0]["id"] == model_id


def delete_model_and_assert(client, model_id):
    delete_response = client.delete(DELETE_ROUTE.format(model_id))
    assert delete_response.status_code == 200


def list_models_and_assert_empty(client):
    response = client.get(LIST_ROUTE)
    assert b'{"models":[]}' in response.data


# TESTS


def test_list_models_empty(client):
    list_models_and_assert_empty(client)


def test_get_model_after_upload(client):
    model_id = upload_model_and_assert(client)
    get_model_and_assert(client, model_id)


def test_list_model_after_upload(client):
    model_id = upload_model_and_assert(client)
    list_models_and_assert(client, model_id)


def test_get_model_after_deleted_upload(client):
    model_id = upload_model_and_assert(client)
    get_model_and_assert(client, model_id)
    delete_model_and_assert(client, model_id)

    get_response_after_delete = client.get(DELETE_ROUTE.format(model_id))
    assert get_response_after_delete.status_code == 404


def test_list_model_after_deleted_upload(client):
    model_id = upload_model_and_assert(client)
    list_models_and_assert(client, model_id)
    delete_model_and_assert(client, model_id)
    test_list_models_empty(client)


def test_download_uploaded_model(client):
    model_id = upload_model_and_assert(client)
    response = client.get(DOWNLOAD_ROUTE.format(model_id))
    assert response.status_code == 200
    with DUMM_MODEL_FILE.open("rb") as dummy_model:
        dummy_model_bytes = dummy_model.read()
        assert dummy_model_bytes == response.data


def test_upload_no_name_parameter(client):
    response = client.post(UPLOAD_ROUTE, data={
        "model_file": DUMM_MODEL_FILE.open("rb")
    })
    assert response.status_code == 400


def test_upload_empty_name_parameter(client):
    response = client.post(UPLOAD_ROUTE, data={
        "name": "",
        "model_file": DUMM_MODEL_FILE.open("rb")
    })
    assert response.status_code == 400


def test_upload_no_model_file_parameter(client):
    response = client.post(UPLOAD_ROUTE, data={
        "name": "test"
    })
    assert response.status_code == 400


def test_upload_empty_model_file_name_parameter(client):
    response = client.post(UPLOAD_ROUTE, data={
        "name": "test",
        "model_file": (DUMM_MODEL_FILE.open("rb"), "", "application/octet-stream")
    })
    assert response.status_code == 400


def test_upload_invalid_model_file_extension_parameter(client):
    response = client.post(UPLOAD_ROUTE, data={
        "name": "test",
        "model_file": (DUMM_MODEL_FILE.open("rb"), "dummy.png", "image/png")
    })
    assert response.status_code == 400


def test_upload_no_parameter(client):
    response = client.post(UPLOAD_ROUTE, data={
    })
    assert response.status_code == 400


def test_delete_non_existent(client):
    response = client.delete(DELETE_ROUTE.format(str(uuid.uuid4())))
    assert response.status_code == 404


def test_get_non_existent(client):
    response = client.get(GET_ROUTE.format(str(uuid.uuid4())))
    assert response.status_code == 404


def test_download_non_existent(client):
    response = client.get(DOWNLOAD_ROUTE.format(str(uuid.uuid4())))
    assert response.status_code == 404
