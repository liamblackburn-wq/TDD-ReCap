import uuid
from unittest.mock import patch

from peewee import DatabaseError

from src.models import CoinsDutiesJunction


def test_coin_duties_returns_200(client, test_coin, test_duty):
    response = client.get("/coin-duties")
    assert response.status_code == 200


def test_associate_duty_to_coin(test_coin, test_duty, admin_client):
    payload = {"coin_id": str(test_coin.id), "duty_id": str(test_duty.id)}

    response = admin_client.post("/coin-duties", json=payload)
    assert response.status_code == 201


    assert CoinsDutiesJunction.select().where(
            CoinsDutiesJunction.coin == test_coin.id,
            CoinsDutiesJunction.duty == test_duty.id,
        ).exists()

def test_coin_duties_delete_request_returns_200(admin_client, assigned_duty):
    response = admin_client.delete(f"/coin-duties/{assigned_duty.id}")
    assert response.status_code == 200
    assert response.json["message"] == "Duty unlinked successfully"


def test_coin_duties_delete_request_returns_404_for_invalid_link_id(admin_client):
    response = admin_client.delete(f"/coin-duties/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json["error"] == "Link does not exist"


def test_duplicate_duty_returns_409(test_coin, test_duty, client):
    client.post("/api/login", json={"username": "admin", "password": "admin123"})

    CoinsDutiesJunction.create(coin=test_coin.id, duty=test_duty.id)

    duplicate_payload = {"coin_id": str(test_coin.id), "duty_id": str(test_duty.id)}

    response = client.post("/coin-duties", json=duplicate_payload)

    assert response.status_code == 409
    assert response.json["error"] == "Duty is already assigned to coin"


def test_missing_coin_returns_404(client, test_duty):
    client.post("/api/login", json={"username": "admin", "password": "admin123"})

    random_coin_uuid = uuid.uuid4()

    payload = {"coin_id": str(random_coin_uuid), "duty_id": str(test_duty.id)}

    response = client.post("/coin-duties", json=payload)

    assert response.status_code == 404
    assert response.json["error"] == "Coin does not exist"


def test_missing_duty_returns_404(client, test_coin):
    client.post("/api/login", json={"username": "admin", "password": "admin123"})

    random_duty_uuid = uuid.uuid4()

    payload = {"coin_id": str(test_coin.id), "duty_id": str(random_duty_uuid)}

    response = client.post("/coin-duties", json=payload)

    assert response.status_code == 404
    assert response.json["error"] == "Duty does not exist"


def test_duty_complete_returns_200(client, test_coin, test_duty):
    client.post("/api/login", json={"username": "user", "password": "user123"})

    link = CoinsDutiesJunction.create(coin=test_coin.id, duty=test_duty.id)

    payload = {
        "is_complete": True,
    }

    response = client.put(f"/coin-duties/{link.id}", json=payload)

    updated_link = CoinsDutiesJunction.get_by_id(link.id)
    assert response.status_code == 200
    assert updated_link.is_complete is True


def test_put_request_with_missing_link_returns_404(client, test_coin, test_duty):
    client.post("/api/login", json={"username": "user", "password": "user123"})

    random_link_uuid = uuid.uuid4()

    payload = {
        "is_complete": True,
    }

    response = client.put(f"/coin-duties/{random_link_uuid}", json=payload)
    assert response.status_code == 404
    assert response.json["error"] == "Link does not exist"


def test_unauthenticated_user_returns_401_for_coin_duties_post_request(client):
    response = client.post("/coin-duties")
    assert response.status_code == 401


def test_unauthenticated_user_returns_401_for_coin_duties_delete_request(client):
    response = client.delete(f"/coin-duties/{uuid.uuid4()}")
    assert response.status_code == 401


def test_unauthenticated_user_returns_401_for_coin_duties_put_request(client):
    response = client.put(f"/coin-duties/{uuid.uuid4()}")
    assert response.status_code == 401


def test_unauthorised_user_returns_403_for_coin_duties_post_request(user_client):
    response = user_client.post("/coin-duties")
    assert response.status_code == 403


def test_unauthorised_user_returns_403_for_coin_duty_delete_request(user_client):
    response = user_client.delete(f"/coin-duties/{uuid.uuid4()}")
    assert response.status_code == 403

def test_coin_duties_returns_500_on_database_error(admin_client, assigned_duty):
    with patch("src.models.CoinsDutiesJunction.delete") as mock_delete:
        mock_delete.side_effect = DatabaseError("Database connection failed")
        response = admin_client.delete(f"/coin-duties/{assigned_duty.id}")
    assert response.status_code == 500
    assert response.json["error"] == "An internal server error occurred"


def test_update_coin_duties_returns_500_on_database_error(admin_client, assigned_duty):
    with patch("src.models.CoinsDutiesJunction.save") as mock_save:
        mock_save.side_effect = DatabaseError("Database connection failed")
        response = admin_client.put(
            f"/coin-duties/{assigned_duty.id}",
            json={"is_complete": True},
        )
    assert response.status_code == 500
    assert response.json["error"] == "An internal server error occurred"
