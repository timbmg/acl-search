FROM python:3.10.5-slim-buster

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./index ./index

COPY ./logging.conf ./logging.conf
