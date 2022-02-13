{{ define "sso-db-service-name" }}
sso-db-server-service
{{ end }}

{{ define "sso-db-url" }}
{{ printf "jdbc:postgresql://%s:%.0f/keycloak" (include "sso-db-service-name" . | trim ) .Values.db.port }}
{{ end }}