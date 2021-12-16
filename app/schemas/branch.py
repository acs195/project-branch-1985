"""This is the schema module for branches"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra


class BranchSchema(BaseModel):
    """This is the branch list schema"""

    branch_id: str
    crm_id: Optional[str]
    external_ledger_id: Optional[str]
    external_payments_card_id: Optional[str]
    created_by: Optional[str]
    created_on: Optional[datetime]
    updated_on: Optional[datetime]

    class Config:
        extra = Extra.allow

    def dict(self, **kwargs) -> dict:
        kwargs.update(exclude_none=True, exclude={"data_key"})
        return super().dict(**kwargs)


class BranchCreateSchema(BaseModel):
    """This is the branch create schema"""

    branch_id: str
    crm_id: str


class BranchUpdateSchema(BaseModel):
    """This is the branch update schema"""

    external_ledger_id: Optional[str]
    external_payments_card_id: Optional[str]

    class Config:
        extra = Extra.allow
