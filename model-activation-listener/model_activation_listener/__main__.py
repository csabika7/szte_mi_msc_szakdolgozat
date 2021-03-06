import json
from model_activation_listener.kubernetes_api import ModelPredictionServerEndpointHandler
from model_activation_listener.dtos import ActivationEvent
import time
import redis
import kubernetes
import os


def read_file(path):
    try:
        return open(path).read()
    except IOError:
        exit(1)


# Kubernetes configuration
SERVICE_ACCOUNT_ROOT = "/var/run/secrets/kubernetes.io/serviceaccount"
SERVICE_ACCOUNT_TOKEN = read_file(os.path.join(SERVICE_ACCOUNT_ROOT, "token"))
SERVICE_ACCOUNT_CA_CERT_PATH = os.path.join(SERVICE_ACCOUNT_ROOT, "ca.crt")
NAMESPACE = read_file(os.path.join(SERVICE_ACCOUNT_ROOT, "namespace"))

configuration = kubernetes.client.Configuration()
configuration.api_key['authorization'] = SERVICE_ACCOUNT_TOKEN
configuration.api_key_prefix['authorization'] = "Bearer"
configuration.host = "https://{}:{}".format(os.environ["KUBERNETES_SERVICE_HOST"],
                                            os.environ["KUBERNETES_SERVICE_PORT"])
configuration.ssl_ca_cert = SERVICE_ACCOUNT_CA_CERT_PATH
# Redis configuration
REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_CHANNEL = os.environ.get("REDIS_CHANNEL")
# Model prediction aggregator client configuration
LABEL_SELECTOR = os.environ["LABEL_SELECTOR_FOR_MODEL_PREDICATE_SERVICES"]

ACTIVATED_MODEL_DB_SOCKET = os.environ["ACTIVATED_MODEL_DB_SOCKET"]
ACTIVATED_MODEL_KEY = os.environ["ACTIVATED_MODEL_KEY"]


mps_url_handler = ModelPredictionServerEndpointHandler(kube_config=configuration,
                                                       namespace=NAMESPACE,
                                                       label_selector=LABEL_SELECTOR,
                                                       model_name_annotation_key="model_name")

print("Connecting to message queue redis {}:{}".format(REDIS_HOST, REDIS_PORT))
mq_redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
print("Connected.")
print("Connecting to active model db redis")
kv_redis_client = redis.Redis(unix_socket_path=ACTIVATED_MODEL_DB_SOCKET)
print("Connected.")

print("Initialize DB at startup.")
active_model_list = mps_url_handler.get_active_model_list()
print("Currently active models: {}".format(active_model_list))
kv_redis_client.set(ACTIVATED_MODEL_KEY, json.dumps(active_model_list.to_dict()))

print("Subscribing to channel {}".format(REDIS_CHANNEL))
queue = mq_redis_client.pubsub(ignore_subscribe_messages=True)
queue.subscribe(REDIS_CHANNEL)
print("Subscribed successfully. Start listening to messages.")
# Event loop
last_update_time = time.time()
while True:
    message = queue.get_message()
    if message:
        activation_event = json.loads(message["data"], object_hook=lambda d: ActivationEvent(**d))
        print("Model activation event received: model_id: {}, state: {}".format(activation_event.model_id,
                                                                                activation_event.state))
        active_model_list = mps_url_handler.get_active_model_list()
        kv_redis_client.set(ACTIVATED_MODEL_KEY, json.dumps(active_model_list.to_dict()))
        print("Active model prediction server saved for key {}: {}".format(ACTIVATED_MODEL_KEY, active_model_list))
        last_update_time = time.time()
    elif last_update_time - time.time() > 60:
        print("No model activation event has been received for a minute. Update model list.")
        active_model_list = mps_url_handler.get_active_model_list()
        kv_redis_client.set(ACTIVATED_MODEL_KEY, json.dumps(active_model_list.to_dict()))
        last_update_time = time.time()
    time.sleep(0.001)
