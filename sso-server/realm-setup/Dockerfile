FROM ubuntu:latest

RUN apt update && apt install -y curl jq

COPY ./add_realm.sh /realm_setup/add_realm.sh

ENV KEYCLOAK_PROTO=https
ENV KEYCLOAK_HOST=localhost
ENV KEYCLOAK_REALM=weed_rec_admin_realm
ENV KEYCLOAK_ADMIN=admin
ENV KEYCLOAK_ADMIN_PASSWORD=admin

ENTRYPOINT ["/realm_setup/add_realm.sh"]