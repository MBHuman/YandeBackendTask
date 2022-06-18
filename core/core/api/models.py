from enum import Enum
from fastapi import HTTPException
from pydantic import ValidationError
from pydantic import BaseModel, Field, validator
from uuid import UUID
from datetime import date, datetime, timezone
from typing import List, Optional
from fastapi.exceptions import RequestValidationError
from pydantic.datetime_parse import parse_datetime
from core.util.settings import get_settings
import sys

__all__ = [
    'ShopUnitType',
    'ShopUnit',
    'ShopUnitImport',
    'ShopUnitImportRequest',
    'ShopUnitStatisticUnit',
    'ShopUnitStatisticResponse',
    'Error',
    'NewValidationError'
]

settings = get_settings()
log = settings.logger


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
    children: Optional[List] = Field([])


class ShopUnitImport(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = Field(None)
    type: ShopUnitType
    price: Optional[Int64] = Field(None)


class ShopUnitImportFormated(BaseModel):
    id: str
    name: str
    parentId: Optional[str] = Field(None)
    type: str
    price: Optional[int] = Field(None)


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport] = Field(...,
                                        description="Импортируемые элементы")
    updateDate: Datetime = Field(
        ..., description="Время обновления добавляемых товаров/категорий.", example='2022-05-28T21:12:01.000Z')


class ShopUnitImportRequestFormated(BaseModel):
    items: List[ShopUnitImportFormated] = Field(...,
                                                description="Импортируемые элементы")
    updateDate: float = Field(
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
