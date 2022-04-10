from model_prediction_server import create_app


app = create_app()
app.run(host="0.0.0.0", port=80)
