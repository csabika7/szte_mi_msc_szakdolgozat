FROM python:3.10.2

COPY ./server.py /root/server.py
COPY ./templates/* /root/templates/
COPY ./requirements.txt /root/requirements.txt

RUN python3 -m pip install -r /root/requirements.txt

ENV TEMPLATES_DIR /root/templates/

CMD python3 /root/server.py