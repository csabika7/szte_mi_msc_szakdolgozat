from pkg_resources import resource_string
from flask import Flask
import os
import kubernetes
from kubernetes.utils import create_from_yaml
import urllib3
import json
import yaml


def read_file(path):
    try:
        return open(path).read()
    except IOError:
        exit(1)


# Constants
SERVICE_ACCOUNT_ROOT = "/var/run/secrets/kubernetes.io/serviceaccount"
SERVICE_ACCOUNT_TOKEN = read_file(os.path.join(SERVICE_ACCOUNT_ROOT, "token"))
SERVICE_ACCOUNT_CA_CERT_PATH = os.path.join(SERVICE_ACCOUNT_ROOT, "ca.crt")
NAMESPACE = read_file(os.path.join(SERVICE_ACCOUNT_ROOT, "namespace"))
MODEL_STORAGE_PROTO = os.environ["MODEL_STORAGE_PROTO"]
MODEL_STORAGE_HOST = os.environ["MODEL_STORAGE_HOST"]
MODEL_STORAGE_PORT = os.environ["MODEL_STORAGE_PORT"]
GET_MODEL_URL_TEMPLATE = "{}://{}:{}/v1/model-store/model/{}"
LIST_MODELS_URL_TEMPLATE = "{}://{}:{}/v1/model-store/model/list"
DOWNLOAD_MODEL_URL_TEMPLATE = "{}://{}:{}/v1/model-store/model/download/{}"

LIST_MODELS_URL = LIST_MODELS_URL_TEMPLATE.format(MODEL_STORAGE_PROTO, MODEL_STORAGE_HOST, MODEL_STORAGE_PORT)


# Flask setup (web, db)
app = Flask(__name__)
configuration = kubernetes.client.Configuration()
configuration.api_key['authorization'] = SERVICE_ACCOUNT_TOKEN
configuration.api_key_prefix['authorization'] = "Bearer"
configuration.host = "https://{}:{}".format(os.environ["KUBERNETES_SERVICE_HOST"],
                                            os.environ["KUBERNETES_SERVICE_PORT"])
configuration.ssl_ca_cert = SERVICE_ACCOUNT_CA_CERT_PATH


def read_service_template(model_id, model_name):
    template_text = resource_string("model-orchestrator.resources", "service.yaml").decode("utf-8")
    service_name = "model-prediction-{}-service".format(model_id)
    app_name = "model-prediction-{}".format(model_id)
    formatted_template_text = template_text.format(service_name=service_name,
                                                   app_name=app_name,
                                                   model_id=model_id,
                                                   model_name=model_name)
    return yaml.load(formatted_template_text, Loader=yaml.FullLoader)


def read_deployment_template(model_id, model_name):
    template_text = resource_string("model-orchestrator.resources", "deployment.yaml").decode("utf-8")
    deployment_name = "model-prediction-{}-deployment".format(model_id)
    app_name = "model-prediction-{}".format(model_id)
    container_name = "model-prediction-{}".format(model_id)
    model_url = DOWNLOAD_MODEL_URL_TEMPLATE.format(MODEL_STORAGE_PROTO,
                                                   MODEL_STORAGE_HOST,
                                                   MODEL_STORAGE_PORT,
                                                   model_id)
    formatted_template_text = template_text.format(deployment_name=deployment_name,
                                                   app_name=app_name,
                                                   container_name=container_name,
                                                   model_id=model_id,
                                                   model_name=model_name,
                                                   model_url=model_url)
    app.logger.info(formatted_template_text)
    return yaml.load(formatted_template_text, Loader=yaml.FullLoader)


def create_kubernetes_objects(objects):
    with kubernetes.client.ApiClient(configuration) as api_client:
        create_from_yaml(k8s_client=api_client, yaml_objects=objects, namespace=NAMESPACE)


def get_model(model_id):
    url = GET_MODEL_URL_TEMPLATE.format(MODEL_STORAGE_PROTO, MODEL_STORAGE_HOST, MODEL_STORAGE_PORT, model_id)

    http = urllib3.PoolManager()
    resp = http.request("GET", url)
    if resp.status == 200:
        return json.loads(resp.data.decode('utf-8')), 200
    app.logger.error("Model storage service response: {}".format(resp.status))
    return None, resp.status


def list_models():
    http = urllib3.PoolManager()
    resp = http.request("GET", LIST_MODELS_URL)
    if resp.status == 200:
        return json.loads(resp.data.decode('utf-8')), 200
    app.logger.error("Model storage service response: {}".format(resp.status))
    return None, resp.status


@app.route("/v1/model-orchestrator/model/activate/<string:model_id>", methods=["POST"])
def activate(model_id):
    model, status = get_model(model_id)
    if status == 404:
        return "", 404
    if status != 200:
        return "", 500

    service_template = read_service_template(model["id"], model["name"])
    deployment_template = read_deployment_template(model["id"], model["name"])
    create_kubernetes_objects([deployment_template, service_template])
    return "", 200


@app.route("/v1/model-orchestrator/model/deactivate/<string:model_id>", methods=["POST"])
def deactivate(model_id):
    model, status = get_model(model_id)
    if status == 404:
        return "", 404
    if status != 200:
        return "", 500

    with kubernetes.client.ApiClient(configuration) as api_client:
        apps_v1_api = kubernetes.client.AppsV1Api(api_client)
        apps_v1_api.delete_namespaced_deployment(namespace=NAMESPACE,
                                                 name="model-prediction-{}-deployment".format(model_id))
        v1 = kubernetes.client.CoreV1Api(api_client)
        v1.delete_namespaced_service(namespace=NAMESPACE,
                                     name="model-prediction-{}-service".format(model_id))
    return "", 200


@app.route("/v1/model-orchestrator/model/list", methods=["GET"])
def get_services():
    model_list_resp, status = list_models()
    if status != 200:
        return "", 500

    with kubernetes.client.ApiClient(configuration) as api_client:
        apps_v1_api = kubernetes.client.AppsV1Api(api_client)
        deployment_list_resp = apps_v1_api.list_namespaced_deployment(namespace=NAMESPACE,
                                                                      label_selector="managed_by=model-orchestrator")
        active_model_ids = dict()
        for item in deployment_list_resp.items:
            active_model_ids[item.metadata.annotations["model_id"]] = True

        return {
            "models": [{
                "id": model["id"],
                "name": model["name"],
                "active": active_model_ids.get(model["id"]) or False
            } for model in model_list_resp["models"]]
        }


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
