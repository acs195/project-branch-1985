"""This is the schema module for branches"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BranchSchema(BaseModel):
    """This is the branch list schema"""

    id: str
    crm_id: str
    external_ledger_id: Optional[str]
    external_payments_card_id: Optional[str]
    created_by: str
    creation_date: datetime


class BranchCreateSchema(BaseModel):
    """This is the branch create schema"""

    id: str
    crm_id: str


class BranchUpdateSchema(BaseModel):
    """This is the branch update schema"""

    external_ledger_id: Optional[str]
    external_payments_card_id: Optional[str]
