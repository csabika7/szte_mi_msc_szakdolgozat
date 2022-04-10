FROM python:3.8.13 as builder

RUN mkdir /model-activation-listener
ADD model_activation_listener /model-activation-listener/model_activation_listener
ADD requirements.txt /model-activation-listener
ADD setup.py /model-activation-listener

WORKDIR /model-activation-listener

RUN python setup.py bdist_wheel

FROM python:3.8.13

COPY --from=builder /model-activation-listener/dist/*.whl /tmp
RUN pip install /tmp/*.whl
RUN rm /tmp/*

ENTRYPOINT ["python", "-u", "-m", "model_activation_listener"]