#!/bin/sh
/start_uwsgi.sh $1 $2 &
/docker-entrypoint.sh nginx -g "daemon off;"
