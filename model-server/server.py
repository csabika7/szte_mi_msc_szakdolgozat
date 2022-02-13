from flask import Flask, request, jsonify
from models import weed_model
import base64
import tensorflow as tf

app = Flask(__name__)


@app.route("/v1/model/predict", methods=["POST"])
def predict():
    b64_encoded_img = request.data
    input = convert_img_to_model_input(b64_encoded_img)
    prediction = weed_model.predict(input)
    return jsonify(prediction.tolist())


def convert_img_to_model_input(b64_encoded_img):
    b64_decoded_img = base64.b64decode(b64_encoded_img)
    img_tensor = tf.io.decode_raw(b64_decoded_img, tf.uint8)
    img = tf.reshape(img_tensor, (1, 28, 28, 1))
    return img


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
