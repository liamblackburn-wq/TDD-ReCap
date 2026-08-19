import uuid
from unittest.mock import patch

from peewee import DatabaseError

from src.models import Duty


def test_get_duties_endpoint(client, test_duty):

    # ACT: Hit the Flask endpoint. Hit it HARD
    response = client.get("/duties")
    assert response.status_code == 200

    # ASSERT: Gimme data, verify it matches
    data = response.get_json()
    print(data)
    returned_duty = next(item for item in data if item["id"] == str(test_duty.id))

    assert returned_duty["name"] == "Duty 1"
    assert returned_duty["description"] == "TEST DESCRIPTION"


def test_create_duty_returns_201(admin_client):

    payload = {
        "id": str(uuid.uuid4()),
        "name": "Duty 1",
        "description": "TEST DESCRIPTION",
    }

    response = admin_client.post("/duties", json=payload)
    data = response.get_json()
    assert response.status_code == 201
    assert data["name"] == "Duty 1"


def test_invalid_duty_returns_400(admin_client):
    payload = {
        "id": str(uuid.uuid4()),
        "name": "TEAPOT",
        "description": "TEST DESCRIPTION",
    }

    response = admin_client.post("/duties", json=payload)
    data = response.get_json()

    assert response.status_code == 400
    assert "Duty name must start with 'Duty' followed by a number." in data["error"]


def test_duplicate_duty_returns_409(admin_client, test_duty):
    # first duty created in pytest test_duty fixture
    payload = {
        "id": str(uuid.uuid4()),
        "name": "Duty 1",
        "description": "TEST DESCRIPTION",
    }

    response = admin_client.post("/duties", json=payload)
    data = response.get_json()

    assert response.status_code == 409
    assert data["error"] == "Duty already exists"


def test_unauthorised_user_returns_403_for_duty_post_request(user_client):
    response = user_client.post("/duties")
    assert response.status_code == 403


def test_unauthorised_user_returns_403_for_duty_delete_request(user_client):
    response = user_client.delete(f"/duties/{uuid.uuid4()}")
    assert response.status_code == 403


def test_unauthenticated_user_returns_401_for_duty_post_request(client):
    response = client.post("/duties")
    assert response.status_code == 401


def test_unauthenticated_user_returns_401_for_duty_delete_request(client):
    response = client.delete(f"/duties/{uuid.uuid4()}")
    assert response.status_code == 401


def test_duty_delete_endpoint_returns_200(admin_client):

    duty_1_id = uuid.uuid4()
    Duty.create(id=duty_1_id, name="Duty 1", description="DESCRIPTION")

    response = admin_client.delete(f"/duties/{duty_1_id}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Duty deleted successfully"


def test_delete_duty_returns_404_if_id_does_not_exist(admin_client):

    non_existent_id = uuid.uuid4()

    response = admin_client.delete(f"/duties/{non_existent_id}")

    assert response.status_code == 404

    json_data = response.get_json()
    assert json_data["error"] == "Duty does not exist"

def test_delete_duty_returns_500_on_database_error(admin_client, test_duty):
    with patch("src.models.Duty.delete") as mock_delete:
        mock_delete.side_effect = DatabaseError("Database connection failed")
        response = admin_client.delete(f"/duties/{uuid.uuid4()}")
    assert response.status_code == 500
    assert response.json["error"] == "An internal server error occurred"

