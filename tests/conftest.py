"""This is the main conftest module"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app = create_app()
    yield app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    yield TestClient(app)
