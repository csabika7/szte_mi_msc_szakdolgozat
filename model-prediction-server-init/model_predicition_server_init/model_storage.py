import urllib3
import os
import shutil


class ModelStorageClient:

    def __init__(self, model_file_url: str, model_data_volume: str, model_file_name: str):
        self.model_file_url = model_file_url
        self.model_data_volume = model_data_volume
        self.model_file_path = os.path.join(self.model_data_volume, model_file_name)

    def download_model(self):
        if os.path.exists(os.path.join(self.model_data_volume, ".model_file_received")):
            return
        http = urllib3.PoolManager()
        with open(self.model_file_path, "wb") as file:
            resp = http.request("GET", self.model_file_url, preload_content=False)
            shutil.copyfileobj(resp, file)
        with open(os.path.join(self.model_data_volume, ".model_file_received"), mode='a'):
            pass
