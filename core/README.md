# Описание

API для задания в Школу Бэкэнда Яндекса

## Структура

```
├── Dockerfile
├── README.md
├── core
│   ├── api
│   │   ├── advanced
│   │   │   ├── __init__.py
│   │   │   ├── router.py
│   │   │   └── services.py
│   │   └── base
│   │       ├── __init__.py
│   │       ├── models.py
│   │       ├── router.py
│   │       └── services.py
│   ├── logs
│   │   └── fastapi.log
│   ├── src
│   │   ├── __init__.py
│   │   └── application.py
│   └── util
|       |── __init__.py
│       ├── advlogger.py
│       ├── db_dao.py
│       ├── metadata.py
│       ├── remove_422.py
│       ├── schemas.py
│       └── settings.py
├── logs
│   └── fastapi.log
├── main.py
├── requirements.txt
└── tests
    └── unit_test.py
```

## Информация

В папке <code>api</code> хранятся запросы, они разделены на две категории, продвинутую и базовую, как в <code>openapi.yaml </code> файле из задания

Файлы:
- <code>router.py</code> содержит информацию по пути запроса и формату возврата
- <code>services.py</code> содержит логику запроса
- <code>model.py</code> содержит внутренние модели для логики запроса

<code>logs</code> - логи REST API

<code>src</code> - приложение FastAPI
Файлы:
- <code>application.py</code> - Файл с приложением FastAPI

<code>util</code> - структуры и классы, которые нужны для работы REST API
Файлы:
- <code>advlogget.py</code> содержит логику логирования
- <code>db_dao.py</code> класс подключения к базе данных и работе с ней
- <code>metadata.py</code> метаданные для автоматической документации
- <code>remove-_422.py</code> удаление 422 ошибки из автоматической документации
- <code>schemas.py</code> схемы данных, использованные в проекте
- <code>settings.py</code> настройки микросервиса 


<code>main.py</code> - точка входа программы

<code>tests</code> - тесты API

Файлы:
- <code>unit_test.py</code> покрытие тестами из условий openapi.yaml файла
