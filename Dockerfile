FROM python:3.12.1

RUN apt update && apt upgrade -y

WORKDIR /shop_gen

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# create an unprivledged user
RUN adduser --disabled-password --gecos '' app

RUN pip3 install setuptools>=70.0.0

COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

COPY shop_gen .