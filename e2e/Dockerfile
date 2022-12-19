# syntax=docker/dockerfile:1

FROM python:3.10

LABEL Maintainer="mrrayb"

WORKDIR /e2e

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "pytest", "-s" ]
