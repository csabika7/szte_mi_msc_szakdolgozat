from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import uuid

# Constants
MODEL_STORAGE_PATH = "E:\\temp\\"  # os.environ["MODEL_STORAGE_PATH"]
META_DATA_DB_FILE = "metadata.db"
META_DATA_DB_PATH = str(os.path.join(MODEL_STORAGE_PATH, META_DATA_DB_FILE))
ALLOWED_EXTENSIONS = {"hdf5"}


# Flask setup (web, db)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(META_DATA_DB_PATH)
db = SQLAlchemy(app)


class Model(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    file_name = db.Column(db.String(120), unique=True, nullable=False)


db.create_all()


# Routes and helper methods
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/v1/model-store/model", methods=["POST"])
def store():
    name = request.values["name"]
    file = request.files["model_file"]
    if not file:
        return "Model file is required: 'model_file'.", 400
    if file.filename == "":
        return "Model file name is empty.", 400
    if not name:
        return "Required field: 'name'.", 400
    if name == "":
        return "Model name is required.", 400
    try:
        if allowed_file(file.filename):
            file_name = secure_filename(file.filename)
            file.save(os.path.join(MODEL_STORAGE_PATH, file_name))
        model_id = str(uuid.uuid4())
        model = Model(id=model_id, name=name, file_name=file_name)
        db.session.add(model)
        db.session.commit()
        return model_id, 200
    except IOError as ex:
        print(ex)
        return "Unable to save file", 500


@app.route("/v1/model-store/model/<string:model_id>", methods=["GET"])
def get_metadata(model_id):
    m = Model.query.get(model_id)
    return {
        "id": m.id,
        "name": m.name
    }


@app.route("/v1/model-store/model/download/<string:model_id>", methods=["GET"])
def download_model_file(model_id):
    m = Model.query.get(model_id)
    return send_from_directory(MODEL_STORAGE_PATH, m.file_name)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
