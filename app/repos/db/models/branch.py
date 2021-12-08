from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from app.core.config import settings


class BranchDDB(Model):
    """Branch model in DynamoDB"""

    class Meta:
        table_name = "branch-project-1985"
        region = settings.REGION_ID
        connect_timeout_seconds = 8
        read_timeout_seconds = 8
        max_retry_attempts = 1

    branch_id = UnicodeAttribute(hash_key=True)
    crm_id = UnicodeAttribute(range_key=True)
    # external_ledger_id = UnicodeAttribute()
    # external_payments_card_id = UnicodeAttribute()
    created_by = UnicodeAttribute()
    creation_date = UTCDateTimeAttribute()
