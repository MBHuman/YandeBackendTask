

from fastapi.exceptions import RequestValidationError
from core.util.schemas import ShopUnitImportRequest, ShopUnit, ItemNotFound
from core.api.base.models import ShopUnitImportFormated, ShopUnitImportRequestFormated
from pydantic.datetime_parse import parse_datetime
import functools
from core.util.settings import get_settings
from uuid import UUID
from datetime import datetime

__all__ = []


def public(f):
    __all__.append(f.__name__)
    return f


settings = get_settings()
db = settings.db
log = settings.logger


@public
async def import_service(data: ShopUnitImportRequest):
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


@public
async def delete_serice(id: UUID):
    await db.run("api_write.delete", str(id))


@public
async def nodes_service(id: UUID):
    result = await db.run("api_read.nodes", str(id))
    log.info(result)
    mp = {}
    if len(result[0]) == 0:
        raise ItemNotFound()
    response_data = None

    for _, e in enumerate(reversed(result[0])):
        id_in = e[0][0]
        name = e[0][1]
        typeUnit = 'CATEGORY' if e[0][2] == 2 else 'OFFER'
        price = e[0][3]
        date_timestamp = e[0][4]
        date = datetime.isoformat(datetime.utcfromtimestamp(
            date_timestamp), sep="T", timespec='milliseconds') + 'Z'
        parentId = e[0][5]
        if parentId not in mp:
            mp[parentId] = [[], 0, 0]
        if id_in in mp:
            mp[parentId][2] += mp[id_in][2]
            mp[parentId][1] += mp[id_in][1]
            mp[parentId][0].append(ShopUnit(id=id_in, name=name, date=date, parentId=parentId,
                                type=typeUnit, price=(mp[id_in][1] // mp[id_in][2]), children=mp[id_in][0]))
            del mp[id_in]
        else:
            mp[parentId][2] += 1
            mp[parentId][1] += (0 if typeUnit == 'CATEGORY' else price)
            mp[parentId][0].append(ShopUnit(
                id=id_in, name=name, date=date, parentId=parentId, type=typeUnit, price=(None if typeUnit == 'CATEGORY' else price), children=([] if typeUnit == 'CATEGORY' else None)))
    for e in mp:
        response_data = mp[e][0][0]
    return response_data
