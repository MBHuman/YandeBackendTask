# encoding=utf-8
from fastapi import APIRouter
from core.api.advanced.services import sales_service, statistic_service
from core.util.metadata import get_descriptions
from core.util.settings import get_settings
from uuid import UUID
from core.util.remove_422 import remove_422
from core.util.schemas import Error, ShopUnitStatisticResponse, Datetime

__all__ = ['router']

settings = get_settings()
descriptions = get_descriptions()


router = APIRouter(
    tags=['Дополнительные задачи'],
    prefix=f'{settings.ROOT_PATH}'
)


@router.get("/sales",
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
    return await sales_service(date=date)


@router.get('/node/{id}/statistic',
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
            description=descriptions.statistic)
@remove_422
async def statistic(id: UUID, dateStart: Datetime, dateEnd: Datetime):
    return await statistic_service(id=id, dateStart=dateStart, dateEnd=dateEnd)
