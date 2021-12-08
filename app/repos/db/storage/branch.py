"""This is the repository module for branches"""

from app.repos.db.models.branch import BranchDDB
from app.repos.db.storage.base import BaseRepo


class BranchRepo(BaseRepo):
    """This handles branch repository operations"""

    MODEL = BranchDDB
