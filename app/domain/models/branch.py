"""This is the domain models module for branches"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class Branch(BaseModel):
    """This class represents a branch in the domain"""

    branch_id: str
    crm_id: str
    external_ledger_id: Optional[str]
    external_payments_card_id: Optional[str]
    created_by: str
    created_on: datetime
    updated_on: Optional[datetime]

    class Config:
        extra = Extra.allow
