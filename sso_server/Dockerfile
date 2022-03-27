FROM quay.io/keycloak/keycloak-x:16.1.1 as builder

ENV KC_METRICS_ENABLED=true
ENV KC_DB=postgres
RUN /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak-x:16.1.1
COPY --from=builder /opt/keycloak/lib/quarkus/ /opt/keycloak/lib/quarkus/
WORKDIR /opt/keycloak
# Replace for production
RUN keytool -genkeypair -storepass password -storetype PKCS12 -keyalg RSA -keysize 2048 -dname "CN=server" -alias server -ext "SAN:c=DNS:localhost,IP:127.0.0.1" -keystore conf/server.keystore

ENTRYPOINT ["/opt/keycloak/bin/kc.sh", "start"]