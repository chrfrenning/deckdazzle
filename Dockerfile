# syntax=docker/dockerfile:1

# FROM python:3.8-slim-buster
FROM docker

ENV PORT 3000
EXPOSE 3000

RUN apk add --update python3 py3-pip
RUN python3 --version && pip3 --version

RUN apk add sudo

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
RUN chmod +x startup.sh

CMD [ "/bin/sh", "startup.sh"]