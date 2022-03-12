from flask import Flask, request, jsonify
import base64
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
    b64_encoded_img = request.data
    input_img = convert_img_to_model_input(b64_encoded_img)
    prediction = MODEL.predict(input_img)
    return jsonify(prediction.tolist())


def convert_img_to_model_input(b64_encoded_img):
    b64_decoded_img = base64.b64decode(b64_encoded_img)
    img_tensor = tf.io.decode_raw(b64_decoded_img, tf.uint8)
    img = tf.reshape(img_tensor, (1, 227, 227, 3))
    return img


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
