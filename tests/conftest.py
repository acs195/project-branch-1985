"""This is the main conftest module"""

from typing import Any

import boto3
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import create_app
from app.repos.db.database import get_db

TABLE_NAME = "project-branch-1985"


def create_branch_table(db: Any) -> None:
    try:
        db.create_table(
            TableName=TABLE_NAME,
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
        waiter = db.get_waiter('table_exists')
        waiter.wait(TableName=TABLE_NAME, WaiterConfig={'Delay': 1, 'MaxAttempts': 3})
    except Exception:
        pass


def delete_branch_table(db: Any) -> None:
    try:
        db.delete_table(TableName=TABLE_NAME)
        waiter = db.get_waiter('table_not_exists')
        waiter.wait(TableName=TABLE_NAME, WaiterConfig={'Delay': 1, 'MaxAttempts': 3})
    except Exception:
        pass


def get_test_db() -> Any:
    """Get a local DDB resource"""
    db = boto3.client("dynamodb", endpoint_url="http://localhost:4567")
    create_branch_table(db)
    try:
        yield db
    except Exception as e:
        raise e
    finally:
        delete_branch_table(db)


@pytest.fixture
def db() -> Any:
    db = boto3.client("dynamodb", endpoint_url="http://localhost:4567")
    create_branch_table(db)
    yield db
    delete_branch_table(db)


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_db] = get_test_db
    yield app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    yield TestClient(app)
