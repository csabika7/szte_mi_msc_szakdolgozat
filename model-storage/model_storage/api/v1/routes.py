from flask import Blueprint, request, send_from_directory, current_app
from model_storage.files import ModelFileHandler, InvalidFileExtension
from model_storage.database import db
from model_storage.db_models import MLModel
import os
import uuid


api_v1 = Blueprint("model-store", __name__)


@api_v1.route("/model", methods=["POST"])
def store():
    name = request.values["name"]
    file = request.files["model_file"]
    if not file:
        return "Model file is required: 'model_file'.", 400
    if file.filename is None or file.filename == "":
        return "Model file name is empty.", 400
    if name is None or name == "":
        return "Required field: 'name'.", 400
    try:
        file_handler = ModelFileHandler(file, current_app.config["MODEL_STORAGE_PATH"])
        file_name = file_handler.save()

        model_id = str(uuid.uuid4())
        model = MLModel(id=model_id, name=name, file_name=file_name)
        db.session.add(model)
        db.session.commit()
        return model_id, 200
    except InvalidFileExtension:
        return "Invalid file format. Accepted format: hdf5.", 400
    except IOError as ex:
        return "Unable to save file", 500


@api_v1.route("/model/<string:model_id>", methods=["DELETE"])
def delete_model(model_id):
    m = MLModel.query.get(model_id)
    if not m:
        return "", 404
    db.session.delete(m)
    db.session.commit()
    os.remove(os.path.join(current_app.config["MODEL_STORAGE_PATH"], m.file_name))
    return "", 200


@api_v1.route("/model/<string:model_id>", methods=["GET"])
def get_metadata(model_id):
    m = MLModel.query.get(model_id)
    if not m:
        return "", 404
    return {
        "id": m.id,
        "name": m.name
    }


@api_v1.route("/model/list", methods=["GET"])
def get_all_metadata():
    model_list = MLModel.query.all()
    return {
        "models": [{"id": m.id, "name": m.name} for m in model_list]
    }


@api_v1.route("/model/download/<string:model_id>", methods=["GET"])
def download_model_file(model_id):
    m = MLModel.query.get(model_id)
    if not m:
        return "", 404
    return send_from_directory(current_app.config["MODEL_STORAGE_PATH"], m.file_name)
