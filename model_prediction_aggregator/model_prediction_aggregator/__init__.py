from flask import Flask, request
import kubernetes
import os
import threading
import time
import urllib3
import json


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
LABEL_SELECTOR = os.environ["LABEL_SELECTOR_FOR_MODEL_PREDICATE_SERVICES"]

# Flask setup
app = Flask(__name__)


# Kuberentes configuration
configuration = kubernetes.client.Configuration()
configuration.api_key['authorization'] = SERVICE_ACCOUNT_TOKEN
configuration.api_key_prefix['authorization'] = "Bearer"
configuration.host = "https://{}:{}".format(os.environ["KUBERNETES_SERVICE_HOST"],
                                            os.environ["KUBERNETES_SERVICE_PORT"])
configuration.ssl_ca_cert = SERVICE_ACCOUNT_CA_CERT_PATH


SERVICES = dict()


def update_service_list(thread_name):
    while True:
        time.sleep(60)
        try:
            with kubernetes.client.ApiClient(configuration) as api_client:
                core_v1 = kubernetes.client.CoreV1Api(api_client)
                resp = core_v1.list_namespaced_service(namespace=NAMESPACE, label_selector=LABEL_SELECTOR,
                                                       timeout_seconds=60)
                SERVICES.clear()
                for item in resp.items:
                    SERVICES[item.metadata.annotations["model_name"]] = \
                        "http://{}/v1/model/predict".format(item.metadata.name)
                app.logger.info(SERVICES)
        except Exception as e:
            app.logger.error(e)


x = threading.Thread(target=update_service_list, args=(1,), daemon=True)
x.start()


def send_predicate(file, url):
    data = file.read()
    http = urllib3.PoolManager()
    resp = http.request(
        "POST",
        url,
        fields={
            "img": (file.filename, data),
        }
    )
    return resp.data, resp.status


@app.route("/v1/model/predict/", methods=["POST"])
def predicate():
    file = request.files["img"]
    if not file:
        return "Image file is required.", 400
    if file.filename == "":
        return "Image file name is empty.", 400
    response = {"name": None, "certainty": 0.0}
    for model_name, service_url in SERVICES.items():
        data, status = send_predicate(file, service_url)
        prediction = float(data.decode('utf-8'))
        if response["certainty"] < prediction:
            response["name"] = model_name
            response["certainty"] = prediction
        if status != 200:
            return "", 500
    return response, 200


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

