"""This module contains custom exception for branches"""


class BranchNotFound(Exception):
    """Branch is not found in repo"""

    def __init__(self, branch_id: str) -> None:
        message = f"Branch not found: {branch_id}"
        super().__init__(message)
