from flask import Flask

# Flask setup (web, db)
app = Flask(__name__)


@app.route("/v1/model/predicate", methods=["POST"])
def predicate(model_id):
    pass


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
