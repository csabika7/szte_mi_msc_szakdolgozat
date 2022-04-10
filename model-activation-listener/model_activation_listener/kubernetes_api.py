import kubernetes.client as kube_client
from kubernetes.client import Configuration


class ModelPredictionServerEndpointHandler:

    def __init__(self, kube_config: Configuration, namespace: str, label_selector: str,
                 prediction_path: str, model_name_annotation_key: str):
        self.kube_config = kube_config
        self.namespace = namespace
        self.label_selector = label_selector
        self.prediction_path = prediction_path
        self.model_name_annotation_key = model_name_annotation_key

    def list_model_prediction_server_urls(self):
        with kube_client.ApiClient(self.kube_config) as api_client:
            core_v1_api = kube_client.CoreV1Api(api_client)
            service_list_res = core_v1_api.list_namespaced_service(namespace=self.namespace,
                                                                   label_selector=self.label_selector)
            urls = dict()
            for item in service_list_res.items:
                model_name = item.metadata.annotations[self.model_name_annotation_key]
                urls[model_name] = "http://{}{}".format(item.metadata.name, self.prediction_path)
            return urls
