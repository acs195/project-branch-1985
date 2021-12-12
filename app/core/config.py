"""Thi is the config module"""

from datetime import timezone
from enum import Enum
from os import environ

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

ENV_NAME = environ["ENV_NAME"]


class AppEnvironmentEnum(str, Enum):
    DEV = "dev"
    TEST = "test"
    STAGE = "stage"
    PROD = "prod"


class Settings(BaseSettings):
    """The app settings"""

    # Main
    PROJECT_NAME: str = "branch"
    API_V1_STR: str = "/api/branch/v1"
    ENV_NAME: AppEnvironmentEnum = getattr(AppEnvironmentEnum, ENV_NAME.upper())
    HOST: str = environ.get("API_GATEWAY_URL_BRANCH", "localhost")
    PORT: int = int(environ.get("PORT", 5000))
    TIME_ZONE = timezone.utc

    # Authentication
    SECRET_KEY: str = environ["SECRET_KEY"]  # secrets.token_urlsafe(64)
    SECURITY_BYPASS: bool = True  # For the exercise, let's bypass authentication

    # Logging
    LOG_LEVEL: str = environ["LOG_LEVEL"]
    ROOT_LOG_LEVEL = "ERROR" if getattr(AppEnvironmentEnum, ENV_NAME.upper()) == "prod" else "WARNING"

    class Config:
        case_sensitive = True


settings = Settings()
