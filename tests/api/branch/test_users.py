from fastapi.testclient import TestClient

from app.domain.models.other_service import Company
from app.domain.models.branch import User

TEST_API_VERSION = "/api/auth/v1"


def test_read_main(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Welcome": "to the machine"}


def test_login(client: TestClient, user: User, company: Company) -> None:
    credentials = {"username": user.username, "password": "password"}

    response = client.post(f"{TEST_API_VERSION}/auth/token", json=credentials)
    response_data = response.json()

    assert response.status_code == 200, response.text
    assert response_data["access_token"]
    assert response_data["msg"] == "User successfully authenticated"


def test_login_wrong_password(client: TestClient, user: User) -> None:
    credentials = {"username": user.username, "password": "wrong-password"}

    response = client.post(f"{TEST_API_VERSION}/auth/token", json=credentials)

    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Incorrect username or password"


def test_logout(client: TestClient) -> None:
    response = client.post(f"{TEST_API_VERSION}/auth/logout")

    assert response.status_code == 204, response.text
