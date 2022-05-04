from model_orchestrator.dtos import Model
import urllib3.request
import json


GET_MODEL_URL_TEMPLATE = "{}://{}:{}/v1/model-store/model/{}"
LIST_MODELS_URL_TEMPLATE = "{}://{}:{}/v1/model-store/model/list"
DELETE_MODEL_URL_TEMPLATE = "{}://{}:{}/v1/model-store/model/{}"
DOWNLOAD_MODEL_URL_TEMPLATE = "{}://{}:{}/v1/model-store/model/download/{}"


class ModelStorageClient:

    def __init__(self, proto: str, host: str, port: str):
        self.proto = proto
        self.host = host
        self.port = port

    def get_model(self, model_id: str):
        url = GET_MODEL_URL_TEMPLATE.format(self.proto, self.host, self.port, model_id)
        http = urllib3.PoolManager()
        resp = http.request("GET", url)
        if resp.status == 200:
            return json.loads(resp.data, object_hook=lambda d: Model(**d)), 200
        return None, resp.status

    def list_models(self):
        url = LIST_MODELS_URL_TEMPLATE.format(self.proto, self.host, self.port)
        http = urllib3.PoolManager()
        resp = http.request("GET", url)
        if resp.status == 200:
            return [Model(**item) for item in json.loads(resp.data)["models"]], 200
        return None, resp.status

    def delete_model(self, model_id):
        url = DELETE_MODEL_URL_TEMPLATE.format(self.proto, self.host, self.port, model_id)
        http = urllib3.PoolManager()
        resp = http.request("DELETE", url)
        return resp.data, resp.status

    def get_download_url(self, model_id):
        return DOWNLOAD_MODEL_URL_TEMPLATE.format(self.proto, self.host, self.port, model_id)
