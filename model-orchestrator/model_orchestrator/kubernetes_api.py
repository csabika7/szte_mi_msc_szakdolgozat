import kubernetes.client as kube_client
from kubernetes.client import Configuration
import kubernetes.utils as kube_utils
from model_orchestrator.kubernetes_resources import ModelPredictionServerDeploymentYaml, \
    ModelPredictionServerServiceYaml


class ModelPredictionServerHandler:

    def __init__(self, kube_config: Configuration, namespace: str):
        self.kube_config = kube_config
        self.namespace = namespace

    def create_model_prediction_server(self, model_id: str, model_name: str, download_url: str):
        service = ModelPredictionServerServiceYaml(model_id, model_name).to_yaml()
        deployment = ModelPredictionServerDeploymentYaml(model_id, model_name, download_url).to_yaml()
        self._create_kubernetes_objects([service, deployment])

    def delete_model_prediction_server(self, model_id: str):
        with kube_client.ApiClient(self.kube_config) as api_client:
            apps_v1_api = kube_client.AppsV1Api(api_client)
            apps_v1_api.delete_namespaced_deployment(namespace=self.namespace,
                                                     name="model-prediction-{}-deployment".format(model_id))
            core_v1_api = kube_client.CoreV1Api(api_client)
            core_v1_api.delete_namespaced_service(namespace=self.namespace,
                                                  name="model-prediction-{}-service".format(model_id))

    def list_model_prediction_server(self):
        with kube_client.ApiClient(self.kube_config) as api_client:
            apps_v1_api = kube_client.AppsV1Api(api_client)
            deployment_list_res = apps_v1_api.list_namespaced_deployment(namespace=self.namespace,
                                                                         label_selector="managed_by=model-orchestrator")
            active_model_ids = []
            for item in deployment_list_res.items:
                active_model_ids.append(item.metadata.annotations["model_id"])
            return active_model_ids

    def _create_kubernetes_objects(self, objects: list):
        with kube_client.ApiClient(self.kube_config) as api_client:
            kube_utils.create_from_yaml(k8s_client=api_client, yaml_objects=objects, namespace=self.namespace)
