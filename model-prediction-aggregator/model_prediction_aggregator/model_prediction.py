import urllib3
from flask import current_app
from model_prediction_aggregator.dtos import PredictionResponse
from model_prediction_aggregator.activated_models_api import ActivatedModelsRepositoryClient


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


class ModelPredictionAggregator:

    def __init__(self, activated_models_repo: ActivatedModelsRepositoryClient):
        self.activated_models_repo = activated_models_repo

    def predict_all(self, img, filename):
        activated_models = self.activated_models_repo.get_activated_models()
        current_app.logger.info("Active models: {}", str(activated_models))
        prediction_results = []
        for activated_model in activated_models:
            client = ModelPredictionClient(activated_model.url)
            data, status = client.predict(img, filename, "image/png")
            if status == 200:
                prediction_result = float(data.decode('utf-8'))
                prediction_results.append(PredictionResponse(activated_model.name, prediction_result))
            else:
                current_app.logger.error("{} model has returned response with status {}.".format(activated_model.name,
                                                                                                 status))
        return prediction_results


class MaxPredictionSelector:

    def __init__(self, cutoff: float):
        self.cutoff = cutoff

    def select(self, predictions: list):
        max_prediction = PredictionResponse("", 0.0)
        for prediction in predictions:
            if max_prediction.certainty < prediction.certainty and self.cutoff < prediction.certainty:
                max_prediction.name = prediction.name
                max_prediction.certainty = prediction.certainty
