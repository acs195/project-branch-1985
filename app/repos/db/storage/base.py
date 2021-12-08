"""This is the base module for repository"""

import abc
from typing import Any, Optional

ModelType = Any


class BaseRepo(abc.ABC):
    """This handles base repository operations"""

    MODEL: ModelType = ModelType

    def __init__(self) -> None:
        pass

    def get(self, id: str) -> Optional[ModelType]:
        """Get object by id from DB"""
        return self.MODEL.get(branch_id=id)

    def get_one_by(self, field: str, value: Any) -> Optional[ModelType]:
        """Get object by a specific field from DB"""
        return self.MODEL.get(**{field: value})

    def create(self, obj_create: dict) -> ModelType:
        """Create an object into the DB"""
        db_obj = self.MODEL(**obj_create)
        db_obj.save()
        return db_obj

    def update(self, id: int, obj_update: dict) -> ModelType:
        """Update an object into the DB"""
        db_obj = self.MODEL.get(branch_id=id)
        for field in obj_update:
            db_obj.set(**{field: obj_update[field]})

        return db_obj
