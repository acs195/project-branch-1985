"""This is the user security module"""

from fastapi import Header, HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from app.core.config import settings
from app.core.logger import logger
from app.schemas.auth import TokenDataSchema

TOKEN_DATA_BYPPASED = {
    "user_id": "1",
    "username": "2",
    "branch_id": "3",
    "exp": 4,
}


class UserSecurity:
    """This is the authentication processing"""

    TOKEN_PREFIX: str = "Bearer"
    ALGORITHM: str = "HS256"
    PWD_CONTEXT = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    def __init__(self, token: str = Header(None)) -> None:
        if settings.SECURITY_BYPASS:
            self.token_data: TokenDataSchema = TokenDataSchema(**TOKEN_DATA_BYPPASED)
        else:
            self.token_data: TokenDataSchema = self.validate_token(token)

    @property
    def user_id(self):
        return self.token_data.user_id

    def validate_token(self, token: str) -> TokenDataSchema:
        """Validate the token provided in the request"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[self.ALGORITHM])
            return TokenDataSchema(**payload)
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired",
            )
        except (JWTError, ValidationError, AttributeError) as e:
            logger.warning(str(e))
        except Exception as e:
            logger.warning(f"Unknown JWT error: {e}")

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
