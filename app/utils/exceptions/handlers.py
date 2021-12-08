"""This module contains custom exception handlers"""

from functools import wraps
from typing import Any, Callable, TypeVar

from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import ValidationError

from app.core.logger import logger
from app.utils.exceptions.branch import BranchNotFound

Params = TypeVar("Params")
KwParams = TypeVar("KwParams")


def common_exception_handler(exc: Exception) -> None:
    try:
        raise exc
    except HTTPException:
        raise
    except ValidationError as e:
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.exception(e)
        raise e


def branch_exception_handler(func: Callable) -> Callable:
    """This decorator handles exceptions at the controller API level"""

    @wraps(func)
    def wrapper(*args: Params, **kwargs: KwParams) -> Any:
        try:
            return func(*args, **kwargs)
        except BranchNotFound as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))
        except Exception as e:
            common_exception_handler(e)

    return wrapper
