from flask import Blueprint, current_app, Response
from model_orchestrator.message_queue import MessageQueueClient
from model_orchestrator.model_store import ModelStorageClient
from model_orchestrator.kubernetes_api import ModelPredictionServerHandler
import kubernetes
import os
import json

api_v1 = Blueprint("model-orchestrator", __name__)


def get_model_config():
    proto = current_app.config.get("MODEL_STORAGE_PROTO")
    host = current_app.config.get("MODEL_STORAGE_HOST")
    port = current_app.config.get("MODEL_STORAGE_PORT")
    return proto, host, port


def get_kube_config():
    service_account_root = current_app.config.get("SERVICE_ACCOUNT_ROOT")
    service_account_token = open(os.path.join(service_account_root, "token")).read()
    service_account_ca_cert_path = os.path.join(service_account_root, "ca.crt")

    configuration = kubernetes.client.Configuration()
    configuration.api_key['authorization'] = service_account_token
    configuration.api_key_prefix['authorization'] = "Bearer"
    configuration.host = "https://{}:{}".format(current_app.config.get("KUBERNETES_SERVICE_HOST"),
                                                current_app.config.get("KUBERNETES_SERVICE_PORT"))
    configuration.ssl_ca_cert = service_account_ca_cert_path
    return configuration


def get_namespace():
    service_account_root = current_app.config.get("SERVICE_ACCOUNT_ROOT")
    namespace = open(os.path.join(service_account_root, "namespace")).read()
    return namespace


@api_v1.route("/model/activate/<string:model_id>", methods=["POST"])
def activate(model_id):
    client = ModelStorageClient(*get_model_config())
    model, status = client.get_model(model_id)
    if status == 404:
        return Response(response="Model does not exist.", status=404, mimetype="text/plain")
    if status != 200:
        return Response(response="", status=500, mimetype="text/plain")

    current_app.logger.info("Creating model prediction server for {}.", model_id)
    server_handler = ModelPredictionServerHandler(get_kube_config(), get_namespace())
    server_handler.create_model_prediction_server(model.id, model.name, client.get_download_url(model.id))

    redis_channel = current_app.config.get("REDIS_CHANNEL")
    current_app.logger.info("Sending state change message for {} to channel {}. New state: activated",
                            model_id, redis_channel)
    queue = MessageQueueClient(host=current_app.config.get("REDIS_HOST"), port=current_app.config.get("REDIS_PORT"))
    queue.send_message(channel=redis_channel, message=json.dumps({"model_id": model_id, "state": "activated"}))

    return Response(response="", status=200, mimetype="text/plain")


@api_v1.route("/model/deactivate/<string:model_id>", methods=["POST"])
def deactivate(model_id):
    client = ModelStorageClient(*get_model_config())
    model, status = client.get_model(model_id)
    if status == 404:
        return Response(response="Model does not exist.", status=404, mimetype="text/plain")
    if status != 200:
        return Response(response="", status=500, mimetype="text/plain")

    current_app.logger.info("Deleting model prediction server for {}.", model_id)
    server_handler = ModelPredictionServerHandler(get_kube_config(), get_namespace())
    server_handler.delete_model_prediction_server(model.id)

    redis_channel = current_app.config.get("REDIS_CHANNEL")
    current_app.logger.info("Sending state change message for {} to channel {}. New state: deactivated",
                            model_id, redis_channel)
    queue = MessageQueueClient(host=current_app.config.get("REDIS_HOST"), port=current_app.config.get("REDIS_PORT"))
    queue.send_message(channel=redis_channel, message=json.dumps({"model_id": model_id, "state": "deactivated"}))

    return Response(response="", status=200, mimetype="text/plain")


@api_v1.route("/model/<string:model_id>", methods=["DELETE"])
def delete(model_id):
    server_handler = ModelPredictionServerHandler(get_kube_config(), get_namespace())
    active_model_id_list = server_handler.list_model_prediction_server()

    if model_id in active_model_id_list:
        return Response(response="Cannot delete active model.", status=409, mimetype="text/plain")

    client = ModelStorageClient(*get_model_config())
    data, status = client.delete_model(model_id)
    return data, status


@api_v1.route("/model/list", methods=["GET"])
def get_services():
    client = ModelStorageClient(*get_model_config())
    model_list, status = client.list_models()
    if status != 200:
        return Response(response="", status=500, mimetype="text/plain")

    server_handler = ModelPredictionServerHandler(get_kube_config(), get_namespace())
    active_model_id_list = server_handler.list_model_prediction_server()

    return {
        "models": [{
            "id": model.id,
            "name": model.name,
            "active": model.id in active_model_id_list
        } for model in model_list]
    }
