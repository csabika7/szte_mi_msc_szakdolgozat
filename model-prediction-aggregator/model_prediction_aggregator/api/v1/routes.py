from flask import Blueprint, request, current_app
from model_prediction_aggregator.prediction_api import ModelPredictionClient
from model_prediction_aggregator.activated_models_api import ActivatedModelsRepositoryClient
from werkzeug.datastructures import FileStorage

api_v1 = Blueprint("model-prediction-aggregator", __name__)


@api_v1.route("/predict", methods=["POST"])
def predicate():
    file: FileStorage = request.files["img"]
    if not file:
        return "Image file is required.", 400
    if file.filename == "":
        return "Image file name is empty.", 400
    activated_models_repo = ActivatedModelsRepositoryClient(current_app.config.get("ACTIVATED_MODEL_DB_SOCKET"),
                                                            current_app.config.get("ACTIVATED_MODEL_KEY"))
    activated_models = activated_models_repo.get_activated_models()
    current_app.logger.info("Active models: {}", str(activated_models))
    raw_img = file.read()
    filename = file.filename
    response = {"name": "", "certainty": 0.0}
    for model_name, service_url in activated_models.items():
        client = ModelPredictionClient(service_url)
        data, status = client.predict(raw_img, filename, "image/png")
        if status == 200:
            prediction = float(data.decode('utf-8'))
            if response["certainty"] < prediction and 0.5 < prediction:
                response["name"] = model_name
                response["certainty"] = prediction
        else:
            current_app.logger.error("{} model has returned response with status {}.".format(model_name, status))
    return response, 200
