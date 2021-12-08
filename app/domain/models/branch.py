"""This is the domain models module for branches"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Branch(BaseModel):
    """This class represents a branch in the domain"""

    id: str
    crm_id: str
    external_ledger_id: Optional[str]
    external_payments_card_id: Optional[str]
    created_by: str
    creation_date: datetime
