FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN apt-get update && apt-get -y dist-upgrade

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
