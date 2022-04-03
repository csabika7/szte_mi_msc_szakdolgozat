from model_orchestrator.kubernetes_resources import ModelPredictionServerServiceYaml, \
    ModelPredictionServerDeploymentYaml


def test_create_model_prediction_server_service_yaml():
    services = ModelPredictionServerServiceYaml("TEST_ID", "TEST_NAME")
    service_yaml = services.to_yaml()
    expected_service_yaml = {
        'apiVersion': 'v1',
        'kind': 'Service',
        'metadata': {
            'name': 'model-prediction-TEST_ID-service',
            'annotations': {
                'model_name': 'TEST_NAME',
                'model_id': 'TEST_ID'
            },
            'labels': {
                'managed_by': 'model-orchestrator'
            }
        },
        'spec': {
            'selector': {
                'app': 'model-prediction-TEST_ID'
            },
            'ports': [
                {
                    'protocol': 'TCP',
                    'port': 80,
                    'targetPort': 80
                }
            ]
        }
    }
    assert service_yaml == expected_service_yaml


def test_create_model_prediction_server_deployment_yaml():
    deployment = ModelPredictionServerDeploymentYaml("TEST_ID", "TEST_NAME", "TEST_URL")
    deployment_yaml = deployment.to_yaml()
    expected_deployment_yaml = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            'name': 'model-prediction-TEST_ID-deployment',
            'labels': {
                'app': 'model-prediction-TEST_ID',
                'managed_by': 'model-orchestrator'
            },
            'annotations': {
                'model_name': 'TEST_NAME',
                'model_id': 'TEST_ID'
            }
        },
        'spec': {
            'replicas': 1,
            'selector': {
                'matchLabels': {
                    'app': 'model-prediction-TEST_ID'
                }
            },
            'template': {
                'metadata': {
                    'labels': {
                        'app': 'model-prediction-TEST_ID'
                    }
                },
                'spec': {
                    'initContainers': [
                        {
                            'name': 'download-model',
                            'image': 'model-prediction-server-init:1.0'
                        }
                    ],
                    'containers': [
                        {
                            'name': 'model-prediction-TEST_ID',
                            'image': 'model-prediction-server:1.0',
                            'ports': [
                                {
                                    'containerPort': 80
                                }
                            ],
                            'env': [
                                {
                                    'name': 'MODEL_FILE_URL',
                                    'value': 'TEST_URL'
                                },
                                {
                                    'name': 'MODEL_DATA_VOLUME',
                                    'value': '/data'
                                }
                            ],
                            'volumeMounts': [
                                {
                                    'mountPath': '/data',
                                    'name': 'model-data-volume'
                                }
                            ]
                        }
                    ],
                    'volumes': [
                        {
                            'name': 'model-data-volume',
                            'emptyDir': {
                                'medium': ''
                            }
                        }
                    ]
                }
            }
        }
    }
    assert deployment_yaml == expected_deployment_yaml
