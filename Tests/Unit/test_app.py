import uuid

from app import load_user
from src.models import User
from unittest.mock import patch


def test_load_user_returns_user_for_valid_id(user_client):
    seeded_user = User.get(User.username == "user")

    result = load_user(str(seeded_user.id))

    assert result is not None
    assert result.username == "user"


def test_load_user_returns_none_for_invalid_uuid_string():
    result = load_user("invalid-uuid-string")
    assert result is None


def test_load_user_returns_none_for_invalid_type():
    result = load_user(None)
    assert result is None


def test_delete_coin_returns_500_on_database_error(admin_client, test_coin):
    with patch("src.models.Coin.delete") as mock_delete:
        mock_delete.side_effect = Exception("Database connection failed")
        response = admin_client.delete(f"/coins/{uuid.uuid4()}")
    assert response.status_code == 500
    assert response.json["error"] == "Database connection failed"


def test_update_coin_returns_500_on_database_error(admin_client, test_coin):
    with patch("src.models.Coin.update") as mock_save:
        mock_save.side_effect = Exception("Database connection failed")
        response = admin_client.put(
            f"/coins/{test_coin.id}",
            json={"name": "New name"},
        )
    assert response.status_code == 500
    assert response.json["error"] == "Database connection failed"
