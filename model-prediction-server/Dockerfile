FROM python:3.8.13 as builder

RUN mkdir /model-prediction-server
ADD model_prediction_server /model-prediction-server/model_prediction_server
ADD requirements.txt /model-prediction-server
ADD setup.py /model-prediction-server

WORKDIR /model-prediction-server

RUN python setup.py bdist_wheel

FROM python:3.8.13

COPY --from=builder /model-prediction-server/dist/*.whl /tmp
RUN pip install /tmp/*.whl
RUN rm /tmp/*

ENTRYPOINT ["python", "-m", "model_prediction_server"]