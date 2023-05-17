# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ENV PORT 3000
EXPOSE 3000

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "server", "run"]