from flask import Flask, request
import tensorflow as tf
import urllib3
import os
import shutil

MODEL_FILE_URL = os.environ["MODEL_FILE_URL"]
MODEL_DATA_VOLUME = os.environ["MODEL_DATA_VOLUME"]
MODEL_FILE_PATH = os.path.join(MODEL_DATA_VOLUME, "model.hdf5")

app = Flask(__name__)


def save_model_file():
    print("Saving model file...")
    http = urllib3.PoolManager()
    with open(MODEL_FILE_PATH, "wb") as file:
        resp = http.request("GET", MODEL_FILE_URL, preload_content=False)
        shutil.copyfileobj(resp, file)
        print("Model file saved.")


# TODO do checks before downloading
save_model_file()

print("Loading model.")
MODEL = tf.keras.models.load_model(MODEL_FILE_PATH)
print("Model loaded.")


@app.route("/v1/model/predict", methods=["POST"])
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
        app.logger.error(e)
        return "", 500


def convert_img_to_model_input(raw_img):
    img_tensor = tf.io.decode_image(raw_img, channels=3)
    img = tf.reshape(img_tensor, (1, 227, 227, 3))
    return img


if __name__ == '__main__':
    app.run(host="0.0.0.0")
