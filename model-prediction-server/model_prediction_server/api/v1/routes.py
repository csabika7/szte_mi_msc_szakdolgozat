from flask import Blueprint, request, Response
from model_prediction_server.ml_model import Model, convert_img_to_model_input
import os


MODEL = Model(os.path.join(os.environ.get("MODEL_DATA_VOLUME"),
                           os.environ.get("MODEL_FILE_NAME")))


api_v1 = Blueprint("model", __name__)


@api_v1.route("/predict", methods=["POST"])
def predict():
    file = request.files["img"]
    if not file:
        return Response(response="Image file is required.", status=400, mimetype="text/plain")
    if file.filename == "":
        return Response(response="Image file name is empty.", status=400, mimetype="text/plain")
    if file.mimetype != "image/png":
        return Response(response="Image must be PNG.", status=400, mimetype="text/plain")
    try:
        input_img = convert_img_to_model_input(file.read())
        prediction = MODEL.predict(input_img)
        return Response(response=str(prediction.tolist()[0][0]), status=500, mimetype="text/plain")
    except Exception as e:
        return Response(response="", status=500, mimetype="text/plain")
