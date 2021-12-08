"""This is the business module for branch"""

from typing import Optional

from app.domain.models.branch import Branch
from app.repos.db.storage.branch import BranchRepo
from app.utils.exceptions.branch import BranchNotFound


class BranchService:
    """This is the service for branch operations"""

    def __init__(self, branch_repo: BranchRepo) -> None:
        self.branch_repo = branch_repo

    def get_branch(self, branch_id: str) -> Optional[Branch]:
        """Get branch by id from repo"""
        branch = self.branch_repo.get_one_by("branch_id", branch_id)
        if not branch:
            raise BranchNotFound(branch_id)

        return Branch.from_orm(branch)
