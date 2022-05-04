#!/usr/bin/env sh

# Authenticate as an admin to create resources in Keycloak
access_token=$(curl $KEYCLOAK_PROTO://$KEYCLOAK_HOST/realms/master/protocol/openid-connect/token --insecure \
  --request POST \
  --data "client_id=admin-cli" \
  --data "username=$KEYCLOAK_ADMIN" \
  --data "password=$KEYCLOAK_ADMIN_PASSWORD" \
  --data "grant_type=password" | jq --raw-output ".access_token")

# Create realm
curl $KEYCLOAK_PROTO://$KEYCLOAK_HOST/admin/realms --insecure \
     --request POST \
     --header "Content-Type: application/json" \
     --header "Authorization: Bearer  $access_token" \
     --data "{\"realm\":\"$KEYCLOAK_REALM\",\"enabled\":true}"

# Create client for model administration for web access
ingress_client_config=$(cat /realm_data/ingress_client_config.json | tr -d "\n" | tr -d " ")
curl $KEYCLOAK_PROTO://$KEYCLOAK_HOST/admin/realms/$KEYCLOAK_REALM/clients \
     --insecure --request POST \
     --header "Content-Type: application/json" \
     --header "Authorization: Bearer  $access_token" \
     --data $ingress_client_config

# Create client for model administration for rest client access
ingress_client_config=$(cat /realm_data/public_client_config.json | tr -d "\n" | tr -d " ")
curl $KEYCLOAK_PROTO://$KEYCLOAK_HOST/admin/realms/$KEYCLOAK_REALM/clients \
     --insecure --request POST \
     --header "Content-Type: application/json" \
     --header "Authorization: Bearer  $access_token" \
     --data $ingress_client_config


# Create admin user for realm
ingress_client_config=$(cat /realm_data/admin_user.json | tr -d "\n" | tr -d " ")
curl $KEYCLOAK_PROTO://$KEYCLOAK_HOST/admin/realms/$KEYCLOAK_REALM/users \
     --insecure --request POST \
     --header "Content-Type: application/json" \
     --header "Authorization: Bearer  $access_token" \
     --data $ingress_client_config