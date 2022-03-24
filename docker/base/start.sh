#!/bin/sh
/start_uwsgi.sh $1 &
/docker-entrypoint.sh nginx -g "daemon off;"
