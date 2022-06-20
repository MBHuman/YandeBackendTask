from typing import Tuple, Any, NoReturn, Union
import asynctnt
from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from core.util.schemas import ItemNotFound


class DatabaseDao:

    def __init__(self, host: str, port: int, user: str, password: str, logger):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self._connection = None
        self.logger = logger
        self.connection_error: str = ''

    @property
    def connection(self):
        return self._connection

    async def create_connection(self) -> NoReturn:
        if self._connection is None:
            self.logger.error('{create_connection connection is None}')
            self._connection = asynctnt.Connection(host=self.host, port=self.port, username=self.user,
                                                   password=self.password, reconnect_max_attempts=0, fetch_schema=False, auto_refetch_schema=False)
            await self._connection.connect()
            if self.connection is not None:
                self.logger.info(f'{self.connection.is_connected} {self.connection.is_fully_connected} '
                                 f'self.connection={self.connection}')

    async def check_connect(self) -> bool:
        if self.connection is None:
            self.logger.error('{check_connect connection is None}')
            return False

        if not self.connection.is_connected:
            self.logger.error(
                f'{self.connection.is_connected} {self.connection.is_fully_connected} '
                f'self.connection={self.connection}')
            return False

        if self.connection.is_fully_connected is True:
            return True
        else:
            self.logger.error(f'{self.connection.is_connected} '
                              f'{self.connection.is_fully_connected} self.connection={self.connection}')
            return False

    async def run(self, command: str, *args) -> Tuple[Any, ...]:
        # Подключаемся при каждом обращении, чтобы точно убедиться в наличии соединения
        if await self.check_connect() is False:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=["Connection error"],
            )
        try:
            if args:
                result = await self.connection.call(command, args)
            else:
                result = await self.connection.call(command)
            parse_result = self._parse_body_from_db_run(result)
            return parse_result
        except asynctnt.exceptions.TarantoolDatabaseError as e:
            # ошибка сномером 42 ER_ACCESS_DENIED возникает когда тарантул ещё не доконца запустился,
            # нужно переподключиться
            if e.code == 42:
                self.connection.close()
            self.logger.error(f'database call error {command} {args} {e}')
            if e.code == 400:
                raise RequestValidationError(errors=[])
            elif e.code == 404:
                raise ItemNotFound()
            else:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    detail=["Something wrong"])

    def _parse_body_from_db_run(self, response) -> Union[list, tuple]:
        """Парсим результат, который пришел из БД.
           Поведение аналогичное синхронному модулю
           https://github.com/tarantool/taraantool-python/blob/0f95f2828895bdcd9a4ba8cf3eb5c67cf7fa4396/tarantool/response.py#L107
        """
        if not isinstance(response.body, (list, tuple)) and response.body is not None:
            return [response.body]
        else:
            return response.body
