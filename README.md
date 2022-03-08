# Overview
Thesis work of Csaba Kocsis for University of Szeged TTIK Computer Engineering Msc.

# Installation Guide
Development is done on a Windows machine therefore all commands below follow Windows path syntax.
## Model server
### Build docker and helm package
```pwsh
docker build .\model-server -t model-server:0.1 --no-cache
helm package .\charts\model-server
```
### Helm install
```pwsh
helm install model-server .\model-server-1.0.0.tgz
```
## Model Storage server
### Build docker and helm package
```pwsh
docker build .\model-storage -t model-storage:0.1 --no-cache
helm package .\charts\model-storage\
```
### Helm istall
```pwsh
helm install model-storage .\model-storage-1.0.0.tgz
```
## SSO server
### Build docker and helm package
```pwsh
docker build .\sso-server -t sso-server:0.1 --no-cache
helm package .\charts\sso-server
```
### Build image for post install hook
```pwsh
docker build .\sso-server\realm-setup -t sso-server-post-install:0.1 --no-cache
```
### Generate self signed cert
Reference: https://wiki.openssl.org/index.php/Binaries
```pwsh
openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout privateKey.key -out certificate.crt
cp privateKey.key .\charts\sso-server\files
cp certificate.crt .\charts\sso-server\files
```
### Helm install
```bash
helm install sso-server .\sso-server-1.0.0.tgz
```
## Install ingress controller
```pwsh
helm repo add apisix https://charts.apiseven.com
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install apisix apisix/apisix  --namespace default `
 --set gateway.type=NodePort --set gateway.tls.enabled=true --set gateway.tls.nodePort=31152 `
 --set ingress-controller.enabled=true --set ingress-controller.config.apisix.serviceNamespace=default
```

## Admin web server
### Build docker and helm package
```pwsh
helm package .\charts\admin-web-server\
```
### Helm install
```pwsh
helm install admin-web-server .\admin-web-server-1.0.0.tgz
```
