FROM harbor.nicleary.com/dockerhub/python:3.11.2

RUN apt update && apt upgrade -y

WORKDIR /shop_gen

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# create an unprivledged user
RUN adduser --disabled-password --gecos '' app

COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

COPY shop_gen .