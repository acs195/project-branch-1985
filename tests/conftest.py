"""This is the main conftest module"""

from typing import Any

import boto3
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import create_app
from app.repos.db.database import get_db

DB = boto3.resource("dynamodb", endpoint_url="http://localhost:4567")


def get_test_db() -> Any:
    """Get a local DDB resource"""
    try:
        yield DB
    except Exception as e:
        raise e


@pytest.fixture(scope="session")
def db(client: TestClient) -> Any:
    DB.create_table(
        TableName="project-branch-1985",
        AttributeDefinitions=[
            {"AttributeName": "branch_id", "AttributeType": "S"},
            {"AttributeName": "data", "AttributeType": "S"},
        ],
        KeySchema=[
            {"AttributeName": "branch_id", "KeyType": "HASH"},
            {"AttributeName": "data", "KeyType": "RANGE"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    )
    try:
        yield DB
    finally:
        for table in DB.tables.iterator():
            table.delete()


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_db] = get_test_db
    yield app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    yield TestClient(app)
