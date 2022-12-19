# syntax=docker/dockerfile:1

FROM python:3.10

LABEL Maintainer="mrrayb"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python3 setup.py

EXPOSE 3080

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]
