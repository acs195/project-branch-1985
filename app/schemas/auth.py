"""This is the module for API schemas for authentication"""

from pydantic import BaseModel


class TokenDataSchema(BaseModel):
    """This is the token data schema"""

    user_id: str
    username: str
    branch_id: str
    exp: int
