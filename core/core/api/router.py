# encoding=utf-8

from http.client import responses
from fastapi import (APIRouter)
from fastapi.exceptions import RequestValidationError
from core.api.models import (ShopUnitImportRequest, Error)
from core.api.models import ShopUnit, ShopUnitStatisticResponse
from core.api.models import Datetime
from core.api.services import delete_service, imports_service, nodes_serivce, sales_service, statistic_service
from core.api.models import ShopUnitImportFormated, ShopUnitImportRequestFormated
from core.util.exceptions import ItemNotFound
from core.src.metadata import (get_tags, get_descriptions)
from core.util import get_settings
from uuid import UUID
from core.src.remove_422 import remove_422
import functools
from datetime import datetime
from pydantic.datetime_parse import parse_datetime

__all__ = ['router']

settings = get_settings()
tags = get_tags()
descriptions = get_descriptions()
db = settings.db
log = settings.logger

router = APIRouter(
    tags=["Базовые задачи"],
    prefix=f'{settings.ROOT_PATH}'
)


router2 = APIRouter(
    tags=['Дополнительные задачи'],
    prefix=f'{settings.ROOT_PATH}'
)


@router.post("/imports",
             responses={400: {"model": Error,
                              "description": "Невалидная схема документа или входные данные не верны.",
                              "content": {
                                  "application/json": {
                                      "example": {"code": 400, "message": "Validation Failed"}
                                  }
                              }},
                        200: {"model": None, "description": "Вставка или обновление прошли успешно.", }},
             description=descriptions.imports)
@remove_422
async def imports(data: ShopUnitImportRequest):
    if len(data.items) != len(set(item.id for item in data.items)):
        raise RequestValidationError(errors=[])

    def lfilter(func, xs): return functools.reduce(
        lambda x, y: x + 1 if func(y) else x, xs, 0)

    def cond(item): return (item.type == 'OFFER' and item.price is None or
                            item.type == 'CATEGORY' and item.price is not None or
                            item.id == item.parentId)
    numPriceError = lfilter(cond, data.items)
    if numPriceError > 0:
        raise RequestValidationError(errors=[])
    items = []
    for item in data.items:
        items.append(ShopUnitImportFormated(id=str(item.id), name=item.name,
                                            parentId=str(item.parentId),
                                            type=item.type.value, price=item.price))

    date_timestamp = parse_datetime(data.updateDate).timestamp()
    formated_data = ShopUnitImportRequestFormated(items=items,
                                                  updateDate=date_timestamp)
    log.info(formated_data)
    result = await db.run("api_write.imports", formated_data.dict())


@router.delete("/delete/{id}",
               responses={404: {"model": Error,
                                "description": "Категория/товар не найден.",
                                "content": {
                                    "application/json": {
                                        "example": {"code": 404, "message": "Item not found"}
                                    }
                                }},
                          400: {"model": Error,
                                "description": "Невалидная схема документа или входные данные не верны.",
                                "content": {
                                    "application/json": {
                                        "example": {"code": 400, "message": "Validation Failed"}
                                    }
                                }},
                          200: {"model": None,
                                "description": "Удаление прошло успешно."}},
               description=descriptions.delete)
@remove_422
async def delete(id: UUID):
    await db.run("api_write.delete", str(id))


@router.get("/nodes/{id}",
            responses={404: {"model": Error,
                             "description": "Категория/товар не найден.",
                             "content": {
                                 "application/json": {
                                     "example": {"code": 404, "message": "Item not found"}
                                 }
                             }},
                       400: {"model": Error,
                             "description": "Невалидная схема документа или входные данные не верны.",
                             "content": {
                                 "application/json": {
                                     "example": {"code": 400, "message": "Validation Failed"}
                                 }
                             }},
                       200: {"model": ShopUnit,
                             "description": "Информация об элементе."}},
            description=descriptions.nodes)
@remove_422
async def nodes(id: UUID):
    result = await db.run("api_read.nodes", str(id))
    log.info(result)
    mp = {}
    main_parent = result[0][0][0][5]

    for _, e in enumerate(reversed(result[0])):
        id_in = e[0][0]
        name = e[0][1]
        typeUnit = 'CATEGORY' if e[0][2] == 2 else 'OFFER'
        price = e[0][3]
        date_timestamp = e[0][4]
        date = datetime.isoformat(datetime.utcfromtimestamp(date_timestamp), sep="T", timespec='milliseconds') + 'Z'
        parentId = e[0][5]
        if parentId not in mp:
            mp[parentId] = [[], 0]
        if id_in in mp:
            mp[parentId][1] += mp[id_in][1]
            mp[parentId][0].append(ShopUnit(id=id_in, name=name, date=date, parentId=parentId, type=typeUnit, price=mp[id_in][1], children=mp[id_in][0]))
            del mp[id_in]
        else:
            mp[parentId][1] += price
            mp[parentId][0].append(ShopUnit(id=id_in, name=name, date=date, parentId=parentId, type=typeUnit, price=price))
    log.info(mp)
    return mp[main_parent][0]




@router2.get("/sales",
             responses={400: {"model": Error,
                              "description": "Невалидная схема документа или входные данные не верны.",
                              "content": {
                                  "application/json": {
                                      "example": {"code": 400, "message": "Validation Failed"}
                                  }
                              }},
                        200: {"model": ShopUnitStatisticResponse,
                              "description": "Список товаров, цена которых была обновлена."}},
             description=descriptions.sales)
@remove_422
async def sales(date: Datetime):
    await sales_service(date=date)


@router2.get('/node/{id}/statistic',
             responses={404: {"model": Error,
                              "description": "Категория/товар не найден.",
                              "content": {
                                  "application/json": {
                                      "example": {"code": 404, "message": "Item not found"}
                                  }
                              }},
                        400: {"model": Error,
                              "description": "Невалидная схема документа или входные данные не верны.",
                              "content": {
                                  "application/json": {
                                      "example": {"code": 400, "message": "Validation Failed"}
                                  }
                              }},
                        200: {"model": ShopUnitStatisticResponse,
                              "description": "Статистика по элементу."}},
             description=descriptions.nodes)
@remove_422
async def statistic(id: UUID, dateStart: Datetime, dateEnd: Datetime):
    await statistic_service(id=id, dateStart=dateStart, dateEnd=dateEnd)
