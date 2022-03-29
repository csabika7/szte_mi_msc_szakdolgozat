from flask import Blueprint, request
from model_prediction_server.ml_model import Model, convert_img_to_model_input
import os

api_v1 = Blueprint("model", __name__)


MODEL = Model(os.path.join(os.environ.get("MODEL_DATA_VOLUME"),
                           os.environ.get("MODEL_FILE_NAME")))


@api_v1.route("/predict", methods=["POST"])
def predict():
    file = request.files["img"]
    if not file:
        return "Image file is required.", 400
    if file.filename == "":
        return "Image file name is empty.", 400
    try:
        input_img = convert_img_to_model_input(file.read())
        prediction = MODEL.predict(input_img)
        return str(prediction.tolist()[0][0])
    except Exception as e:
        return "", 500
