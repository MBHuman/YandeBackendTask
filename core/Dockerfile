# syntax=docker/dockerfile:1
FROM python:3.7
WORKDIR /
# RUN apk add --no-cache gcc musl-dev linux-headers
ENV APP_NAME Mega Market Open API
ENV DESCRIPTION Вступительное задание в Летнюю Школу Бэкенд Разработки Яндекса 2022
ENV APP_VERSION=1.0
ENV APP_HOST=0.0.0.0
ENV APP_PORT=8000
RUN python3 -m pip install poetry
COPY . .
RUN poetry update
EXPOSE 80
CMD ["poetry", "run", "start"]