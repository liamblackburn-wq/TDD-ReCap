from unittest.mock import patch

import uuid


def test_coin_duties_returns_500_on_database_error(admin_client, assigned_duty):
    with patch("src.models.CoinsDutiesJunction.delete") as mock_delete:
        mock_delete.side_effect = Exception("Database connection failed")
        response = admin_client.delete(f"/coin-duties/{uuid.uuid4()}")
    assert response.status_code == 500
    assert response.json["error"] == "Database connection failed"


def test_update_coin_duties_returns_500_on_database_error(admin_client, assigned_duty):
    with patch("src.models.CoinsDutiesJunction.update") as mock_save:
        mock_save.side_effect = Exception("Database connection failed")
        response = admin_client.put(
            f"/coin-duties/{assigned_duty.id}",
            json={"is_complete": True},
        )
    assert response.status_code == 500
    assert response.json["error"] == "Database connection failed"
