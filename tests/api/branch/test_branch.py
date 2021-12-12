from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from app.domain.models.branch import Branch

TEST_API_VERSION = "/api/branch/v1"


def test_get_one_branch(client: TestClient, branch: Branch) -> None:
    expected_branch = branch.dict(exclude_none=True)

    response = client.get(f"{TEST_API_VERSION}/branches/{branch.branch_id}")

    response_branch = response.json()
    assert response.status_code == 200, response.text
    assert response_branch == jsonable_encoder(expected_branch)


def test_create_branch(client: TestClient) -> None:
    new_branch_id = "818beb63-9a78-423b-9b28-5f5e0d0824f6"
    new_crm_id = "00Q4x000008tONdEAM"
    new_branch = dict(
        branch_id=new_branch_id,
        crm_id=new_crm_id,
    )

    response = client.post(f"{TEST_API_VERSION}/branches/", json=new_branch)

    response_branch_created = response.json()
    response_branch_created.pop("created_on")
    new_branch.update(created_by="1")
    assert response.status_code == 201, response.text
    assert response_branch_created == new_branch


def test_update_branch(client: TestClient, branch: Branch) -> None:
    update_branch = dict(
        external_payments_card_id="cus_KNGEt7NfzitisQ",
        external_ledger_id="20-1000159x",
    )
    expected_branch = branch.dict(exclude_none=True)
    expected_branch.update(**update_branch, updated_by="1")

    response = client.put(
        f"{TEST_API_VERSION}/branches/{branch.branch_id}",
        json=update_branch,
    )

    response_branch_updated = response.json()
    response_branch_updated.pop("updated_on")
    assert response.status_code == 200, response.text
    assert response_branch_updated == jsonable_encoder(expected_branch)
