FROM python:3.7.4-alpine

WORKDIR /api

COPY . /api/

RUN apk add gcc musl-dev openssl-dev libffi-dev make
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD python3 app.py
