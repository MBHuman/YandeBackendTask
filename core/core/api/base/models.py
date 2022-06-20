from typing import List, Optional
from pydantic import BaseModel, Field

__all__ = []


class ShopUnitImportFormated(BaseModel):
    id: str
    name: str
    parentId: Optional[str] = Field(None)
    type: str
    price: Optional[int] = Field(None)


class ShopUnitImportRequestFormated(BaseModel):
    items: List[ShopUnitImportFormated] = Field(...,
                                                description="Импортируемые элементы")
    updateDate: float = Field(
        ..., description="Время обновления добавляемых товаров/категорий.", example='2022-05-28T21:12:01.000Z')
