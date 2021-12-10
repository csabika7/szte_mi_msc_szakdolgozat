from flask import Flask, request, jsonify
from models import weed_model

app = Flask(__name__)

@app.route("/v1/model/predict", methods=["POST"])
def predict():
    #img = request.files['img']
    #input = convert_img_to_model_input(img)
    #weed_model.predict(input)
    
    print("Predict endpoint called...")
    return jsonify([])

def convert_img_to_model_input(img):
    pass


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")