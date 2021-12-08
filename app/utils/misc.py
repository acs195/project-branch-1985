from copy import deepcopy
from datetime import date, datetime

from app.core.config import settings


class AwareDatetime:
    """Class to manage aware datetime objects"""

    @staticmethod
    def now() -> datetime:
        return datetime.now(settings.TIME_ZONE)

    @staticmethod
    def today() -> date:
        return datetime.now(settings.TIME_ZONE).date()


def flat_dict(data: dict) -> dict:
    """Remove the keys in a dictionary that are dictionaries"""
    new_data = deepcopy(data)
    for key, value in data.items():
        if isinstance(value, dict):
            new_data.pop(key)

    return new_data
