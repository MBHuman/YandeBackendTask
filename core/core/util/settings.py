from loguru import logger
from pydantic import PyObject
from core.util.db_dao import DatabaseDao
from core.util.advlogger import CustomizeLogger

__all__ = []


def public(f):
    __all__.append(f.__name__)
    return f


env_data = {
    "LOG_FILE_PATH": "logs/fastapi.log",
    "LOG_LEVEL": "DEBUG",
    "LOG_FORMAT": "<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> request id: {extra[request_id]} - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    "LOG_ROTATION": "20 days",
    "LOG_RETENTION": "1 month",
    "EVENT_LOG_DIR": "logs",
    "APP_NAME": "Mega Market Open API",
    "DESCRIPTION": "Вступительное задание в Летнюю Школу Бэкенд Разработки Яндекса 2022",
    "APP_VERSION": "1.0",
    "APP_HOST": "0.0.0.0",
    "APP_PORT": 80,
    "API_ROOT_PATH": "",

    "DB_HOST": "tarantool",
    "DB_PORT": '3301',
    "DB_USER": "admin",
    "DB_PASSWORD": "example"
}

LOG_FILE_PATH = env_data["LOG_FILE_PATH"]
LOG_LEVEL = env_data["LOG_LEVEL"]
LOG_FORMAT = env_data["LOG_FORMAT"]
LOG_ROTATION = env_data["LOG_ROTATION"]
LOG_RETENTION = env_data["LOG_RETENTION"]

logger = CustomizeLogger.customize_logging(
    LOG_FILE_PATH, LOG_LEVEL, LOG_ROTATION, LOG_RETENTION, LOG_FORMAT)


class Settings(object):

    _logger: PyObject = logger
    # :TODO change to ENV and container settings
    APP_NAME: str = env_data["APP_NAME"]
    APP_VERSION: str = env_data["APP_VERSION"]
    HOST: str = env_data["APP_HOST"]
    PORT: int = env_data["APP_PORT"]
    ROOT_PATH: str = env_data["API_ROOT_PATH"]
    DESCRIPTION: str = env_data["DESCRIPTION"]

    DB_HOST: str = env_data['DB_HOST']
    DB_PORT: int = env_data['DB_PORT']
    DB_USER: str = env_data['DB_USER']
    DB_PASSWORD: str = env_data['DB_PASSWORD']
    _db: DatabaseDao = DatabaseDao(host=DB_HOST,
                                   port=DB_PORT, user=DB_USER, password=DB_PASSWORD, logger=_logger)

    @property
    def db(self) -> DatabaseDao:
        return self._db

    @property
    def logger(self):
        return self._logger


@public
def get_settings() -> Settings:
    """
        Получение настроек приложения
    """
    return Settings()
