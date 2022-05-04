from pkg_resources import resource_string
import yaml


class KubernetesYamlTemplate:

    def __init__(self, template_text: str):
        self.template_text = template_text

    def fill_template(self, **kwargs):
        formatted_template_text = self.template_text.format(**kwargs)
        return yaml.load(formatted_template_text, Loader=yaml.FullLoader)


class ModelPredictionServerServiceYaml:

    def __init__(self, model_id: str, model_name: str):
        self.model_id = model_id
        self.model_name = model_name

    def to_yaml(self):
        template_text = resource_string("model_orchestrator.resources", "service.yaml").decode("utf-8")
        service_name = "model-prediction-{}-service".format(self.model_id)
        app_name = "model-prediction-{}".format(self.model_id)
        template = KubernetesYamlTemplate(template_text)
        return template.fill_template(service_name=service_name,
                                      app_name=app_name,
                                      model_id=self.model_id,
                                      model_name=self.model_name)


class ModelPredictionServerDeploymentYaml:

    def __init__(self, model_id: str, model_name: str, download_url: str):
        self.model_id = model_id
        self.model_name = model_name
        self.download_url = download_url

    def to_yaml(self):
        template_text = resource_string("model_orchestrator.resources", "deployment.yaml").decode("utf-8")
        deployment_name = "model-prediction-{}-deployment".format(self.model_id)
        app_name = "model-prediction-{}".format(self.model_id)
        container_name = "model-prediction-{}".format(self.model_id)
        template = KubernetesYamlTemplate(template_text)
        return template.fill_template(deployment_name=deployment_name,
                                      app_name=app_name,
                                      container_name=container_name,
                                      model_id=self.model_id,
                                      model_name=self.model_name,
                                      model_url=self.download_url)
