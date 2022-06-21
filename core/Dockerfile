# syntax=docker/dockerfile:1
FROM python:3.7
WORKDIR /
# RUN apk add --no-cache gcc musl-dev linux-headers
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 80
ADD main.py main.py