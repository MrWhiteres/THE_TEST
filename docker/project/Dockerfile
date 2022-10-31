FROM python:3.11-rc-alpine3.16

WORKDIR /THE_TEST/.
COPY .. ..
RUN apk update && apk add postgresql-client && apk add make && rm -rf /var/cache/apt
RUN pip install -r ../requirements.txt && pip install --upgrade pip && chmod u+x ../task/tasks.sh
ENTRYPOINT ["../task/tasks.sh"]


