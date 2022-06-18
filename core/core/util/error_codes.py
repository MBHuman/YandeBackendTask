
__all__ = []

from core.api.models import Error


def public(f):
    __all__.append(f.__name__)
    return f


def get_api_error(error_code: int) -> Error:
    return Error()
