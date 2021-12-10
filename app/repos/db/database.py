"""This is the DDB module"""

from typing import Any

import boto3


def get_db() -> Any:
    """Get a DDB resource"""
    db = boto3.resource("dynamodb", endpoint_url="http://localhost:4567")
    try:
        yield db
    except Exception as e:
        raise e
