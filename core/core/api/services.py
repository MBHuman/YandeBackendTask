# encoding=utf-8

from uuid import UUID
from core.api.models import ShopUnitImportRequest
from core.api.models import Datetime
from core.util import get_settings

__all__ = []


def public(f):
    __all__.append(f.__name__)
    return f


settings = get_settings()


@public
async def imports_service(item: ShopUnitImportRequest):
    return


@public
async def delete_service(id: UUID):
    return


@public
async def nodes_serivce(id: UUID):
    return


@public
async def sales_service(date: Datetime):
    return


@public
async def statistic_service(id: UUID, dateStart: Datetime, dateEnd: Datetime):
    return
