"""This is the logger module"""

import logging
import logging.config

from app.core.config import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} - {levelname} - {name} - {module}.{funcName}:{lineno} - {message}",
            "style": "{",
        }
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "verbose"}},
    "root": {"handlers": ["console"], "level": settings.ROOT_LOG_LEVEL},
    "loggers": {
        settings.PROJECT_NAME: {
            "handlers": ["console"],
            "level": settings.LOG_LEVEL,
            "propagate": False,
        }
    },
}


def get_logger() -> logging.Logger:
    """Get custom logger"""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(settings.PROJECT_NAME)
    return logger


logger = get_logger()
