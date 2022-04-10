FROM python:3.8.13 as builder

RUN mkdir /model-prediction-server-init
ADD model_predicition_server_init /model-prediction-server-init/model_predicition_server_init
ADD requirements.txt /model-prediction-server-init
ADD setup.py /model-prediction-server-init

WORKDIR /model-prediction-server-init

RUN python setup.py bdist_wheel

FROM python:3.8.13

COPY --from=builder /model-prediction-server-init/dist/*.whl /tmp
RUN pip install /tmp/*.whl
RUN rm /tmp/*

ENTRYPOINT ["python", "-m", "model_predicition_server_init"]