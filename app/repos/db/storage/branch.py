"""This is the repository module for branches"""

from app.repos.db.models.branch import BranchDDB
from app.repos.db.storage.base import BaseRepo


class BranchRepo(BaseRepo):
    """This handles branch repository operations"""

    MODEL = BranchDDB
    TABLE_NAME = "project-branch-1985"
    PK_NAME = "branch_id"
    PK_TEMPLATE = "BRANCH#{}"
    SK_NAME = "data"
    SK_TEMPLATE = "METADATA"
    SK_TEMPLATE_BILL_ACCT = "BILL_ACCT#{}"
