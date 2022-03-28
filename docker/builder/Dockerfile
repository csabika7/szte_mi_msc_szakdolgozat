FROM builder-base:1.0 as builder

ARG PROJECT_NAME
ARG MODULE_NAME

RUN mkdir /${PROJECT_NAME}
ADD ${MODULE_NAME} /${PROJECT_NAME}/${MODULE_NAME}
ADD requirements.txt /${PROJECT_NAME}
ADD setup.py /${PROJECT_NAME}

WORKDIR /${PROJECT_NAME}

RUN python setup.py bdist_wheel

FROM nginx:1.21.6

ARG PROJECT_NAME
ARG MODULE_NAME
ENV PROJECT_NAME=${PROJECT_NAME}
ENV MODULE_NAME=${MODULE_NAME}

RUN apt-get update && apt-get install -y build-essential python3-dev python3-pip
RUN pip install uwsgi

COPY --from=builder /${PROJECT_NAME}/dist/*.whl /tmp
RUN pip install /tmp/*
RUN rm /tmp/*

COPY --from=builder  /nginx.conf /etc/nginx
COPY --from=builder  /start_uwsgi.sh /
RUN chmod 755 /start_uwsgi.sh
COPY --from=builder  /start.sh /
RUN chmod 755 /start.sh

ENTRYPOINT /start.sh $PROJECT_NAME $MODULE_NAME
CMD [""]
