from flask import Blueprint, request, current_app, Response
from model_prediction_aggregator.model_prediction import ModelPredictionAggregator, MaxPredictionSelector
from model_prediction_aggregator.activated_models_api import ActivatedModelsRepositoryClient
from model_prediction_aggregator.archive import ImageArchive
from model_prediction_aggregator.image import resize_img
from werkzeug.datastructures import FileStorage


TARGET_HEIGHT = 227
TARGET_WIDTH = 227

api_v1 = Blueprint("model-prediction-aggregator", __name__)


@api_v1.route("/predict", methods=["POST"])
def predict():
    file: FileStorage = request.files["img"]
    if not file:
        return Response(response="Image file is required.", status=400, mimetype="text/plain")
    if file.filename == "":
        return Response(response="Image file name is empty.", status=400, mimetype="text/plain")
    if file.mimetype != "image/png":
        return Response(response="Image must be PNG.", status=400, mimetype="text/plain")

    # step #1 resize image
    raw_img = file.read()
    resized_image = resize_img(raw_img, TARGET_WIDTH, TARGET_HEIGHT)
    filename = file.filename

    # step #2 call all active models
    activated_models_repo = ActivatedModelsRepositoryClient(current_app.config.get("ACTIVATED_MODEL_DB_SOCKET"),
                                                            current_app.config.get("ACTIVATED_MODEL_KEY"))
    prediction_aggregator = ModelPredictionAggregator(activated_models_repo)
    predictions = prediction_aggregator.predict_all(resized_image, filename)

    # step #3 select the result with maximum certainty but it has to be at least 0.5
    selector = MaxPredictionSelector(0.5)
    prediction = selector.select(predictions)

    # step #4 archive image in original size
    try:
        archive = ImageArchive()
        archive.save(raw_img)
    except Exception as e:
        current_app.logger.error("Unable to save to image archive", e)

    return prediction.to_dict(), 200
