from typing import Any

import pytest
from fastapi.encoders import jsonable_encoder

from app.domain.models.branch import Branch
from app.repos.db.models.branch import BranchDDB
from app.repos.db.storage.branch import BranchRepo
from app.utils.misc import AwareDatetime


@pytest.fixture
def branch(db: Any) -> Branch:
    branch_db = BranchDDB(
        branch_id="818beb63-9a78-423b-9b28-5f5e0d0824f6",
        crm_id="00Q4x000008tONdEAM",
        created_by="1",
        external_ledger_id="20-1000159",
        # external_payments_card_id="cus_KNGEt7NfzitisQ",
        created_on=AwareDatetime.now(),
    )
    BranchRepo(db=db).create(jsonable_encoder(branch_db.dict(exclude_unset=True, exclude_none=True)))
    yield Branch(**branch_db.dict())


@pytest.fixture
def branch_with_bill_accts(db: Any, branch: Branch) -> Branch:
    bill_acct_1 = "40-100881"
    bill_acct_2 = "40-100882"
    branch_db = BranchRepo(db=db).update(branch.branch_id, {"bill_acct": bill_acct_1})
    BranchRepo(db=db).update(branch.branch_id, {"bill_acct": bill_acct_2})
    yield Branch(**branch_db.dict(exclude_unset=True, exclude_none=True, exclude={"data_key"}))
