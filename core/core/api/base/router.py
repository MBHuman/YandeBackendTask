# encoding=utf-8
from fastapi import APIRouter
from core.util.schemas import ShopUnitImportRequest, Error, ShopUnit
from core.api.base.services import import_service, delete_serice, nodes_service
from core.util.metadata import get_descriptions
from core.util.settings import get_settings
from uuid import UUID
from core.util.remove_422 import remove_422

__all__ = ['router']
descriptions = get_descriptions()
settings = get_settings()


router = APIRouter(
    tags=["Базовые задачи"],
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
    return await import_service(data=data)


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
    return await delete_serice(id=id)


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
    return await nodes_service(id=id)
