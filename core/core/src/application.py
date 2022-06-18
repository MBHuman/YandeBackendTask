# encoding=utf-8

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from core.util.exceptions import ItemNotFound

from core.src.remove_422 import remove_422s
from core.util import get_settings
from core.api.router import router as main_router, router2 as advanced_router
from core.api.models import Error


__all__ = ['get_app']

settings = get_settings()
log = settings.logger


def get_app():
    app = FastAPI(title=settings.APP_NAME,
                  version=settings.APP_VERSION,
                  description=settings.DESCRIPTION)

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=Error(code=status.HTTP_400_BAD_REQUEST,
                          message="Validation Failed").dict()
        )

    @app.exception_handler(ItemNotFound)
    async def request_validation_exception_handler(
        request: Request, exc: ItemNotFound
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=Error(code=status.HTTP_404_NOT_FOUND,
                          message="Item not found").dict()
        )

    # v1
    app.include_router(main_router)
    app.include_router(advanced_router)

    @app.on_event("startup")
    async def create_connection() -> None:
        await settings.db.create_connection()

    remove_422s(app)

    return app
