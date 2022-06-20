from enum import Enum
from pydantic import BaseModel, Field, validator
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from fastapi.exceptions import RequestValidationError
from pydantic.datetime_parse import parse_datetime

__all__ = [
    'ShopUnitType',
    'Int64',
    'Datetime',
    'ShopUnit',
    'ShopUnitImport',
    'ShopUnitImportRequest',
    'ShopUnitStatisticUnit',
    'Error'
]


class ShopUnitType(str, Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"


class Int64(int):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            if v < 0 or v < -2 ** 63 or v > 2 ** 63 - 1:
                raise RequestValidationError(
                    code=400, message="Validation Failed")
        except:
            raise RequestValidationError(code=400, message="Validation Failed")
        return v


class Datetime(datetime):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            v = parse_datetime(v)
        except:
            raise RequestValidationError(code=400, message="Validation Failed")
        return v.isoformat(timespec='milliseconds').replace("+00:00", "Z")


class ShopUnit(BaseModel):
    id: UUID
    name: str
    date: Datetime
    parentId: Optional[UUID] = Field(None)
    type: ShopUnitType
    price: Optional[Int64] = Field(None)
    children: Optional[List] = Field(None)


class ShopUnitImport(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = Field(None)
    type: ShopUnitType
    price: Optional[Int64] = Field(None)


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport] = Field(...,
                                        description="Импортируемые элементы")
    updateDate: Datetime = Field(
        ..., description="Время обновления добавляемых товаров/категорий.", example='2022-05-28T21:12:01.000Z')


class ShopUnitStatisticUnit(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = Field(None)
    type: ShopUnitType
    price: Optional[Int64] = Field(None)
    date: Datetime


class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit]


class Error(BaseModel):
    code: int
    message: str


class ItemNotFound(Exception):
    pass
