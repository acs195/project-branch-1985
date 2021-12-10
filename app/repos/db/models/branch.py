"""This is the DB models module for branches"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, validator


class BranchDDB(BaseModel):
    """This class represents a branch in the domain"""

    branch_id: str
    crm_id: str
    created_by: str
    created_on: datetime
    updated_on: Optional[datetime]

    class Config:
        extra = Extra.allow

    @validator("branch_id")
    def parse_pk(cls, branch_id: str) -> str:
        if "BRANCH" in branch_id:
            return branch_id.split("#")[1]

        return branch_id
