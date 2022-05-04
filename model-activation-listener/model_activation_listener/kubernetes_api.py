import kubernetes.client as kube_client
from kubernetes.client import Configuration
from model_activation_listener.dtos import ActiveModel, ActiveModelList


class ModelPredictionServerEndpointHandler:

    def __init__(self, kube_config: Configuration, namespace: str, label_selector: str,
                 model_name_annotation_key: str):
        self.kube_config = kube_config
        self.namespace = namespace
        self.label_selector = label_selector
        self.model_name_annotation_key = model_name_annotation_key

    def get_active_model_list(self):
        with kube_client.ApiClient(self.kube_config) as api_client:
            core_v1_api = kube_client.CoreV1Api(api_client)
            service_list_res = core_v1_api.list_namespaced_service(namespace=self.namespace,
                                                                   label_selector=self.label_selector)
            active_models = []
            for item in service_list_res.items:
                model_name = item.metadata.annotations[self.model_name_annotation_key]
                url = "http://{}/v1/model/predict".format(item.metadata.name)
                active_models.append(ActiveModel(model_name, url))
            return ActiveModelList(active_models)
