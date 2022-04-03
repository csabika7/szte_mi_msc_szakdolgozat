from kubernetes.client import V1ObjectMeta, V1Deployment, V1DeploymentList
from model_orchestrator.kubernetes_api import ModelPredictionServerHandler
from pytest_mock.plugin import MockerFixture
import yaml


def test_delete_mps(mocker: MockerFixture):
    mocker.patch("model_orchestrator.kubernetes_api.kube_client.ApiClient")
    mocked_apps = mocker.patch("model_orchestrator.kubernetes_api.kube_client.AppsV1Api.delete_namespaced_deployment")
    mocked_core = mocker.patch("model_orchestrator.kubernetes_api.kube_client.CoreV1Api.delete_namespaced_service")

    mps_handler = ModelPredictionServerHandler(None, "test_namespace")
    mps_handler.delete_model_prediction_server("TEST_ID")

    mocked_apps.assert_called_once_with(namespace="test_namespace",
                                        name="model-prediction-TEST_ID-deployment")
    mocked_core.assert_called_once_with(namespace="test_namespace",
                                        name="model-prediction-TEST_ID-service")


def test_list_mps(mocker: MockerFixture):
    mocker.patch("model_orchestrator.kubernetes_api.kube_client.AppsV1Api.list_namespaced_deployment",
                 new=lambda *args, **kwargs: V1DeploymentList(items=[
                     V1Deployment(metadata=V1ObjectMeta(annotations={"model_id": "TEST_ID"}))
                 ]))

    mps_handler = ModelPredictionServerHandler(None, "test_namespace")
    mps_list = mps_handler.list_model_prediction_server()

    assert mps_list == ["TEST_ID"]


def test_create_mps(mocker: MockerFixture):
    mocker.patch("model_orchestrator.kubernetes_api.kube_client.ApiClient")
    mocked_create_from_yaml = mocker.patch("model_orchestrator.kubernetes_api.kube_utils.create_from_yaml")

    mps_handler = ModelPredictionServerHandler(None, "test_namespace")
    mps_handler.create_model_prediction_server("TEST_ID", "TEST_NAME", "TEST_URL")

    expected_service_text = """
        apiVersion: v1
        kind: Service
        metadata:
          name: "model-prediction-TEST_ID-service"
          annotations:
            model_name: "TEST_NAME"
            model_id: "TEST_ID"
          labels:
            managed_by: model-orchestrator
        spec:
          selector:
            app: "model-prediction-TEST_ID"
          ports:
            - protocol: TCP
              port: 80
              targetPort: 80
    """
    expected_deployment_text = """
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: "model-prediction-TEST_ID-deployment"
          labels:
            app: "model-prediction-TEST_ID"
            managed_by: model-orchestrator
          annotations:
            model_name: "TEST_NAME"
            model_id: "TEST_ID"
        spec:
          replicas: 1
          selector:
            matchLabels:
              app: "model-prediction-TEST_ID"
          template:
            metadata:
              labels:
                app: "model-prediction-TEST_ID"
            spec:
              initContainers:
              - name: download-model
                image: model-prediction-server-init:1.0
              containers:
              - name: "model-prediction-TEST_ID"
                image: model-prediction-server:1.0
                ports:
                  - containerPort: 80
                env:
                  - name: MODEL_FILE_URL
                    value: "TEST_URL"
                  - name: MODEL_DATA_VOLUME
                    value: /data
                volumeMounts:
                  - mountPath: /data
                    name: model-data-volume
              volumes:
                - name: model-data-volume
                  emptyDir:
                    medium: ""
    """

    expected_deployment_yaml = yaml.load(expected_deployment_text, Loader=yaml.FullLoader)
    expected_service_yaml = yaml.load(expected_service_text, Loader=yaml.FullLoader)
    mocked_create_from_yaml.assert_called_once_with(k8s_client=mocker.ANY,
                                                    yaml_objects=[expected_service_yaml, expected_deployment_yaml],
                                                    namespace="test_namespace")
