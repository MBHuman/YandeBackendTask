from fastapi import FastAPI
from typing import Any, Callable, Set, TypeVar
from fastapi.openapi.utils import generate_operation_id
from fastapi.routing import APIRoute

__all__ = []


def public(f):
    __all__.append(f.__name__)
    return f


F = TypeVar("F", bound=Callable[..., Any])


@public
def remove_422(func: F) -> F:
    func.__remove_422__ = True
    return func

@public
def remove_422s(app: FastAPI) -> None:
    openapi_schema = app.openapi()
    operation_ids_to_update: Set[str] = set()
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        methods = route.methods or ["GET"]
        if getattr(route.endpoint, "__remove_422__", None):
            for method in methods:
                operation_ids_to_update.add(
                    generate_operation_id(route=route, method=method))
    paths = openapi_schema["paths"]
    for path, operations in paths.items():
        for method, metadata in operations.items():
            operation_id = metadata.get("operationId")
            if operation_id in operation_ids_to_update:
                metadata["responses"].pop("422", None)
