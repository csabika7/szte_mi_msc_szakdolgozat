from flask import Blueprint, request, send_from_directory, current_app, Response
from model_storage.files import ModelFileHandler, InvalidFileExtension
from model_storage.database import db
from model_storage.db_models import ModelEntity
from model_storage.dtos import Model, ModelList
import os
import uuid


api_v1 = Blueprint("model-store", __name__)


@api_v1.route("/model", methods=["POST"])
def store():
    name = request.values["name"]
    file = request.files["model_file"]
    if not file:
        return Response(response="Model file is required: 'model_file'.", status=400, mimetype="text/plain")
    if file.filename is None or file.filename == "":
        return Response(response="Model file name is empty.", status=400, mimetype="text/plain")
    if name is None or name == "":
        return Response(response="Required field: 'name'.", status=400, mimetype="text/plain")
    try:
        file_handler = ModelFileHandler(file, current_app.config["MODEL_STORAGE_PATH"])
        file_name = file_handler.save()

        model_id = str(uuid.uuid4())
        model = ModelEntity(id=model_id, name=name, file_name=file_name)
        db.session.add(model)
        db.session.commit()
        return Model(model_id, name).to_dict(), 200
    except InvalidFileExtension:
        return Response(response="Invalid file format. Accepted format: hdf5.", status=400, mimetype="text/plain")
    except IOError as ex:
        return Response(response="Unable to save file.", status=500, mimetype="text/plain")


@api_v1.route("/model/<string:model_id>", methods=["DELETE"])
def delete_model(model_id):
    m = ModelEntity.query.get(model_id)
    if not m:
        return Response(response="Model does not exist.", status=404, mimetype="text/plain")
    db.session.delete(m)
    db.session.commit()
    os.remove(os.path.join(current_app.config["MODEL_STORAGE_PATH"], m.file_name))
    return Response(response="", status=200, mimetype="text/plain")


@api_v1.route("/model/<string:model_id>", methods=["GET"])
def get_metadata(model_id):
    m = ModelEntity.query.get(model_id)
    if not m:
        return Response(response="Model does not exist.", status=404, mimetype="text/plain")
    return Model(m.id, m.name).to_dict()


@api_v1.route("/model/list", methods=["GET"])
def get_all_metadata():
    model_list = ModelEntity.query.all()
    return ModelList([Model(m.id, m.name) for m in model_list]).to_dict()


@api_v1.route("/model/download/<string:model_id>", methods=["GET"])
def download_model_file(model_id):
    m = ModelEntity.query.get(model_id)
    if not m:
        return Response(response="Model does not exist.", status=404, mimetype="text/plain")
    return send_from_directory(current_app.config["MODEL_STORAGE_PATH"], m.file_name)
