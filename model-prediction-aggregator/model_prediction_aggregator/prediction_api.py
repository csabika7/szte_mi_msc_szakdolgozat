import urllib3


class ModelPredictionClient:

    def __init__(self, url):
        self.url = url

    def predict(self, data: bytes, filename: str, content_type: str):
        http = urllib3.PoolManager()
        resp = http.request("POST", self.url,
                            fields={
                                "img": (filename, data, content_type),
                            })
        return resp.data, resp.status
