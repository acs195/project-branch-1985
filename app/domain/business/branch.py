"""This is the business module for branch"""

from app.domain.models.branch import Branch
from app.repos.db.storage.branch import BranchRepo
from app.schemas.branch import BranchCreateSchema, BranchUpdateSchema
from app.utils.exceptions.branch import BranchNotFound
from app.utils.misc import AwareDatetime


class BranchService:
    """This is the service for branch operations"""

    def __init__(self, branch_repo: BranchRepo) -> None:
        self.branch_repo = branch_repo

    def get(self, branch_id: str) -> Branch:
        """Get branch by id from repo"""
        branch_db = self.branch_repo.get(branch_id)
        if not branch_db:
            raise BranchNotFound(branch_id)

        return Branch(**branch_db.dict())

    def create(self, branch_create: BranchCreateSchema, created_by: str) -> Branch:
        """Add branch to repo"""
        branch_db = self.branch_repo.create(
            {
                **branch_create.dict(exclude_unset=True, exclude_none=True),
                "created_by": created_by,
                "created_on": str(AwareDatetime.now()),
            }
        )
        branch = Branch(**branch_db.dict())
        return branch

    def update(self, branch_id: str, branch_update: BranchUpdateSchema, updated_by: str) -> Branch:
        """Update branch in repo"""
        self.get(branch_id)

        branch_db = self.branch_repo.update(
            branch_id,
            {
                **branch_update.dict(exclude_unset=True, exclude_none=True),
                "updated_by": updated_by,
                "updated_on": str(AwareDatetime.now()),
            },
        )
        branch = Branch(**branch_db.dict())
        return branch
