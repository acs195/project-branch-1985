import pytest

from app.core.security import UserSecurity
from app.domain.models.branch import Branch
from app.repos.db.models.branch import BranchDDB


@pytest.fixture
def branch() -> Branch:
    user_db = BranchDDB(
        username="username",
        password=UserSecurity.PWD_CONTEXT.encrypt("password"),
    )
    yield Branch.from_orm(user_db)
