"""This is the DDB module"""

from typing import Any

import boto3


def get_db() -> Any:
    """Get a DDB resource"""
    db = boto3.client("dynamodb")
    try:
        yield db
    except Exception as e:
        raise e
