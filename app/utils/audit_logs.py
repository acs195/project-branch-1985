import json
from enum import Enum
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from pynamodb.attributes import JSONAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from app.core.config import settings
from app.core.logger import logger
from app.utils.misc import AwareDatetime, flat_dict
from app.utils.pagination import PaginatorDynamoDB


class CustomJSONAttribute(JSONAttribute):
    def serialize(self, value: Optional[dict]) -> Optional[str]:
        if value is None:
            return None
        return json.dumps(jsonable_encoder(value))

    def deserialize(self, value: str) -> dict:
        return json.loads(value, strict=False)


class AuditLogDDB(Model):
    """Audit log in DynamoDB"""

    class Meta:
        # host = "http://localhost:4567"
        table_name = "project-branch-1985"
        region = settings.REGION_ID
        connect_timeout_seconds = 8
        read_timeout_seconds = 8
        max_retry_attempts = 1

    username = UnicodeAttribute(hash_key=True)
    timestamp = UTCDateTimeAttribute(range_key=True)
    action = UnicodeAttribute()
    entity = UnicodeAttribute()
    entity_id = UnicodeAttribute()
    payload = CustomJSONAttribute()

    def dict(self) -> dict:
        serialized = {}
        for key in self.attribute_values:
            serialized[key] = self.__getattribute__(key)
        return serialized


class AuditLogger:
    PROTECTED_FIELDS = ("password",)

    @classmethod
    def write(cls, entity: str, username: str, action: str, payload: dict) -> None:
        try:
            cls._protect_fields(payload)
            audit_entry = dict(
                username=username,
                timestamp=AwareDatetime.now(),
                action=action.value if isinstance(action, Enum) else action,
                entity=entity.value if isinstance(entity, Enum) else entity,
                payload=flat_dict(payload),
            )
            if payload.get("id"):
                audit_entry.update(entity_id=str(payload.get("id")))

            audit_log = AuditLogDDB(**audit_entry)
            audit_log.save()

        except Exception as e:
            logger.error(f"Error in audit logging: {e}")

    @classmethod
    def _protect_fields(cls, payload: dict) -> None:
        for field in cls.PROTECTED_FIELDS:
            payload.pop(field, None)

    @classmethod
    def read_user_activity(cls, username: str, paginator: PaginatorDynamoDB) -> List[AuditLogDDB]:
        last_evaluated_key: dict = {}
        if paginator.last_key:
            last_evaluated_key = {"username": {"S": username}, "timestamp": {"S": paginator.last_key}}

        query = AuditLogDDB.query(
            hash_key=username,
            limit=paginator.page_size,
            last_evaluated_key=last_evaluated_key,
            scan_index_forward=False,
        )
        result = [a for a in query]
        paginator.update_params(query)
        return result
