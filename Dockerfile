FROM python:3.7-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc  \
    && apt-get install libc6-dev -y \
    && apt-get install libpq-dev -y \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r deploy/requirements.txt
