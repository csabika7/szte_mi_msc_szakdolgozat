FROM python:3.8.13 as builder

ARG PROJECT_NAME
ARG MODULE_NAME

RUN mkdir /${PROJECT_NAME}
ADD ${MODULE_NAME} /${PROJECT_NAME}/${MODULE_NAME}
ADD requirements.txt /${PROJECT_NAME}
ADD setup.py /${PROJECT_NAME}

WORKDIR /${PROJECT_NAME}

RUN python setup.py bdist_wheel

FROM python:3.8.13

ARG PROJECT_NAME
ARG MODULE_NAME
ENV PROJECT_NAME=${PROJECT_NAME}
ENV MODULE_NAME=${MODULE_NAME}

RUN pip install uwsgi

COPY --from=builder /${PROJECT_NAME}/dist/*.whl /tmp
RUN pip install /tmp/*.whl
RUN rm /tmp/*

ENTRYPOINT uwsgi --master --http 0.0.0.0:80 --mount /$PROJECT_NAME=$MODULE_NAME.uwsgi:app --manage-script-name --chmod-socket=666 --limit-post=1073741824 --buffer-size=65535
CMD [""]
