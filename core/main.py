import uvicorn
from core.util.settings import get_settings
from core.src import get_app

__all__ = []


def public(f):
    __all__.append(f.__name__)
    return f



settings = get_settings()
log = settings.logger
app = get_app()
# uvicorn.run(app, host=settings.HOST, port=settings.PORT)
