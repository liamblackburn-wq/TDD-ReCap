import uuid
from src.models import Duty, Coin, CoinsDutiesJunction


def test_home_route_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_coins_endpoint_returns_assigned_duties_status(client):
    coin = Coin.create(id=uuid.uuid4(), name="Test Coin")
    duty = Duty.create(id=uuid.uuid4(), name="Duty 1", description="Test Description")
    CoinsDutiesJunction.create(coin=coin, duty=duty, is_complete=False)

    response = client.get("/coins")
    data = response.get_json()

    assert response.status_code == 200

    target_coin = next((coin for coin in data if coin["name"] == "Test Coin"), None)

    assert target_coin is not None
    assert target_coin["status"] == "IN_PROGRESS"


def test_duty_delete_endpoint_returns_200(client):
    duty_1_id = uuid.uuid4()
    Duty.create(id=duty_1_id, name="Duty 1", description="DESCRIPTION")

    response = client.delete(f"/duties/{duty_1_id}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Duty deleted successfully"


def test_delete_duty_returns_404_if_id_does_not_exist(client):
    non_existent_id = uuid.uuid4()

    response = client.delete(f"/duties/{non_existent_id}")

    assert response.status_code == 404

    json_data = response.get_json()
    assert json_data["error"] == "Duty does not exist"
