FROM tensorflow/tensorflow:latest

COPY ./models/ambrosia_artemisiifolia/weed_model.hdf5 /root/weed_model.hdf5
COPY ./models.py /root/models.py
COPY ./server.py /root/server.py
COPY ./requirements.txt /root/requirements.txt

RUN python3 -m pip install -r /root/requirements.txt

CMD python3 /root/server.py