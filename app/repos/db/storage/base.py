"""This is the base module for repository"""

import abc
from typing import Any, Optional

from fastapi import Depends

from app.core.logger import logger
from app.repos.db.database import get_db

ModelType = Any


class BaseRepo(abc.ABC):
    """This handles base repository operations"""

    MODEL: ModelType = ModelType
    TABLE_NAME: str
    PK_NAME: str
    PK_TEMPLATE: str
    SK_NAME: str
    SK_TEMPLATE: str

    def __init__(self, db: Any = Depends(get_db)) -> None:
        self.db = db

    def get(self, id: str) -> Optional[ModelType]:
        """Get object by id from DB"""
        try:
            lookup_key = {
                self.PK_NAME: {"S": self.PK_TEMPLATE.format(id)},
                self.SK_NAME: {"S": self.SK_TEMPLATE},
            }
            response = self.db.get_item(TableName=self.TABLE_NAME, Key=lookup_key)
            item = response.get("Item")
            if item:
                parsed_item = {key: list(value.values())[0] for key, value in item.items()}
                return self.MODEL(**parsed_item)
            else:
                return None
        except Exception as e:
            logger.error(f"Error on get item: {e}")
            raise

    def create(self, obj_create: dict) -> ModelType:
        """Create an object into the DB"""
        item_create = obj_create.copy()
        try:
            pk = item_create.pop(self.PK_NAME)
            item_template = {
                self.PK_NAME: {"S": self.PK_TEMPLATE.format(pk)},
                self.SK_NAME: {"S": self.SK_TEMPLATE},
                **{key: {"S": value} for key, value in item_create.items()},
            }
            self.db.put_item(TableName=self.TABLE_NAME, Item=item_template)
            return self.MODEL(**obj_create)
        except Exception as e:
            logger.error(f"Error on create item: {e}")
            raise

    def update(self, id: int, obj_update: dict) -> ModelType:
        """Update an object into the DB"""
        try:
            update_key = {
                self.PK_NAME: {"S": self.PK_TEMPLATE.format(id)},
                self.SK_NAME: {"S": self.SK_TEMPLATE},
            }
            update_expression = "SET " + ", ".join([f"{key} = :{key}" for key, _ in obj_update.items()])
            expression_values = {f":{key}": {"S": value} for key, value in obj_update.items()}
            # expression_values = {f":{key}": value for key, value in obj_update.items()}

            response = self.db.update_item(
                TableName=self.TABLE_NAME,
                Key=update_key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW",
            )
            item = response.get("Attributes")
            parsed_item = {key: list(value.values())[0] for key, value in item.items()}
            return self.MODEL(**parsed_item)
        except Exception as e:
            logger.error(f"Error on create item: {e}")
            raise
