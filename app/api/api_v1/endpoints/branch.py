"""This is the api module for branches"""

from fastapi import APIRouter, Depends, status

from app.core.security import UserSecurity
from app.domain.business.branch import BranchService
from app.repos.db.storage.branch import BranchRepo
from app.schemas.branch import BranchCreateSchema, BranchSchema, BranchUpdateSchema
from app.utils.exceptions.handlers import branch_exception_handler

router = APIRouter()


@router.get("/", response_model=BranchSchema)
@branch_exception_handler
def get_branch_by_bill_acct(
    bill_acct_id: str,
    security: UserSecurity = Depends(),
    branch_repo: BranchRepo = Depends(),
) -> BranchSchema:
    """Get a single branch by billing account  ## THIS IS NOT ENTIRELY FINISHED ##"""
    branch_srv = BranchService(branch_repo)
    branch = branch_srv.get_by_bill_acct(bill_acct_id)
    return branch


@router.get("/{branch_id}", response_model=BranchSchema)
@branch_exception_handler
def get_branch(
    branch_id: str,
    security: UserSecurity = Depends(),
    branch_repo: BranchRepo = Depends(),
) -> BranchSchema:
    """Get a single branch"""
    branch_srv = BranchService(branch_repo)
    branch = branch_srv.get(branch_id)
    return branch


@router.post("/", response_model=BranchSchema, status_code=status.HTTP_201_CREATED)
@branch_exception_handler
def create_branch(
    branch_create: BranchCreateSchema,
    security: UserSecurity = Depends(),
    branch_repo: BranchRepo = Depends(),
) -> BranchSchema:
    """Create branch"""
    branch_srv = BranchService(branch_repo)
    branch = branch_srv.create(branch_create, created_by=security.user_id)
    return branch


@router.put("/{branch_id}", response_model=BranchSchema)
@branch_exception_handler
def update_branch(
    branch_id: str,
    branch_update: BranchUpdateSchema,
    security: UserSecurity = Depends(),
    branch_repo: BranchRepo = Depends(),
) -> BranchSchema:
    """Update branch"""
    branch_srv = BranchService(branch_repo)
    branch = branch_srv.update(branch_id, branch_update, updated_by=security.user_id)
    return branch
