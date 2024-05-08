# pull official base image
FROM python:3.12-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
#pango es una dependencia de weasyprint
RUN apk update && apk add postgresql-dev gcc musl-dev libpq-dev wget pango  \
     libffi-dev python3-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
     libc-dev linux-headers 

 

# install dependencies
RUN pip install --upgrade pip


COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x initdb.sh
