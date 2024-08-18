FROM python:3.8-alpine

ENV PORT 3000
EXPOSE 3000

RUN apk update && apk add --no-cache python3 py3-pip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "server.py" ]