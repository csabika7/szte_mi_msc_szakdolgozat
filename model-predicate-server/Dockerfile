FROM tensorflow/tensorflow:latest

COPY ./server.py /root/server.py
COPY ./requirements.txt /root/requirements.txt

RUN python3 -m pip install -r /root/requirements.txt

CMD python3 /root/server.py