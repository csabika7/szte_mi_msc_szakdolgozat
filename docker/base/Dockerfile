FROM python:3.10.2 as builder

ADD nginx.conf /
ADD start_uwsgi.sh /
ADD start.sh /

RUN pip install wheel
