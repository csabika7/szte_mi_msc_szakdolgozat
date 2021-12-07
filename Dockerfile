FROM tensorflow/tensorflow:latest

COPY ./model.hdf5 /root/model.hdf5
COPY ./model.py /root/model.py

CMD python3 /root/model.py