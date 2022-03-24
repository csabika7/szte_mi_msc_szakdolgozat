#!/bin/sh
uwsgi -s /tmp/uwsgi_service.sock --manage-script-name --mount /$1=$1:app --chmod-socket=666 --limit-post=1073741824 --enable-threads
