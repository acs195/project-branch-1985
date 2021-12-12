"""This is the DDB module"""

from typing import Any

import boto3


def get_db() -> Any:
    """Get a DDB resource"""
    # TODO: delete the endpoint_url (it was for testing purposes only)
    # db = boto3.client("dynamodb", endpoint_url="http://localhost:4567")
    db = boto3.client("dynamodb")
    try:
        yield db
    except Exception as e:
        raise e
