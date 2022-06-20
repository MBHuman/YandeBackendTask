
from pydantic.datetime_parse import parse_datetime
from datetime import timedelta, datetime
from core.util.schemas import ShopUnitStatisticUnit, ShopUnitStatisticResponse, Datetime
from uuid import UUID

from core.util.settings import get_settings

__all__ = []

settings = get_settings()
db = settings.db

def public(f):
    __all__.append(f.__name__)
    return f

@public
async def sales_service(date: Datetime):
    date_to = parse_datetime(date).timestamp()
    date_from = (parse_datetime(date) - timedelta(hours=24)).timestamp()
    result = await db.run('api_read.sales', date_from, date_to)
    items = [ShopUnitStatisticUnit(id=res[0],
                                   name=res[1],
                                   parentId=res[5],
                                   type='CATEGORY' if res[2] == 2 else 'OFFER',
                                   price=res[3],
                                   date=datetime.isoformat(datetime.utcfromtimestamp(res[4]), sep="T", timespec='milliseconds') + 'Z')
             for res in result[0]]
    return ShopUnitStatisticResponse(items=items)

@public
async def statistic_service(id: UUID, dateStart: Datetime, dateEnd: Datetime):
    return