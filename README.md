# Overview
Thesis work of Csaba Kocsis for University of Szeged TTIK Computer Engineering Msc.
# Installation Guide
Development is done on a Windows machine therefore all commands below follow Windows path syntax.

NOTE: Machine learning model associated with this project is not available in this repository.
If you wish to use it then write me a message asking for it. However, you can also deploy your own model.
Requirements for the model:
- Keras can import the model by calling: ```tensorflow.keras.models.load_model```
- Model takes 227x227x3 matrix as an input.
- Model does binary classification
## Prerequisites
This application runs on Kubernetes.
Installation guides for installing Kubernetes:

Windows:
- Docker Desktop: https://docs.docker.com/desktop/windows/install/
- Kubernetes: https://docs.docker.com/desktop/kubernetes/

Linux:
- Docker: https://docs.docker.com/engine/install/#server
- Kubernetes: https://minikube.sigs.k8s.io/docs/start/

The deployment of the application is done with Helm package manager.

Installation guide for installing Helm: https://helm.sh/docs/intro/install/
## Initalization steps
### Helm repo update
```pwsh
helm repo add apisix https://charts.apiseven.com
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```
## Install ingress controller
```pwsh
helm install apisix apisix/apisix  --namespace default `
 --set gateway.type=NodePort --set gateway.tls.enabled=true --set gateway.tls.nodePort=31152 `
 --set ingress-controller.enabled=true --set ingress-controller.config.apisix.serviceNamespace=default
```
## SSO server
### Build docker
```pwsh
docker build .\sso-server -t sso-server:1.0
```
### Build image for post install hook
```pwsh
docker build .\sso-server\realm-setup -t sso-server-post-install:1.0
```
### Generate self signed cert
Reference: https://wiki.openssl.org/index.php/Binaries
```pwsh
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout privateKey.key -out certificate.crt
cp privateKey.key .\charts\sso-server\files
cp certificate.crt .\charts\sso-server\files
```
### Helm package
```pwsh
helm package .\charts\sso-server
```
### Helm install
```bash
helm install sso-server .\sso-server-1.0.0.tgz
```
## Model Storage server
### Build docker and helm package
```pwsh
docker build .\model-storage -f .\docker\builder\Dockerfile -t model-storage:1.0 --build-arg PROJECT_NAME=model-storage --build-arg MODULE_NAME=model_storage
helm package .\charts\model-storage\
```
### Helm istall
```pwsh
helm install model-storage .\model-storage-1.0.0.tgz
```
## Redis
### Helm install
```pwsh
helm install message-broker-redis bitnami/redis --set replica.replicaCount=1 --set architecture=standalone --set auth.enabled=false
```
## Model Orchestrator
### Build docker and helm package
```pwsh
docker build .\model-prediction-server-init -t model-prediction-server-init:1.0
docker build .\model-prediction-server -t model-prediction-server:1.0
docker build .\model-orchestrator -f .\docker\builder\Dockerfile -t model-orchestrator:1.0 --build-arg PROJECT_NAME=model-orchestrator --build-arg MODULE_NAME=model_orchestrator
helm package .\charts\model-orchestrator
```
### Helm install
```pwsh
helm install model-orchestrator .\model-orchestrator-1.0.0.tgz
```
## Model Predicate Aggregator server
### Build docker and helm package
```pwsh
docker build .\model-activation-listener -t model-activation-listener:1.0
docker build .\model-prediction-aggregator -f .\docker\builder\Dockerfile -t model-prediction-aggregator:1.0 --build-arg PROJECT_NAME=model-prediction-aggregator --build-arg MODULE_NAME=model_prediction_aggregator
helm package .\charts\model-prediction-aggregator
```
### Helm install
```pwsh
helm install model-prediction-aggregator .\model-prediction-aggregator-1.0.0.tgz
```
## Admin web server
### Build docker and helm package
```pwsh
docker build .\model-admin-web -t model-admin-web:1.0
helm package .\charts\admin-web-server\
```
### Helm install
```pwsh
helm install admin-web-server .\admin-web-server-1.0.0.tgz
```