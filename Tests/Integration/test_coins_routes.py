import uuid
from src.models import Coin, Duty, CoinsDutiesJunction


def test_get_coins_endpoint(client, test_coin):
    # ACT: Hit the Flask endpoint. Hit it HARD
    response = client.get("/coins")
    assert response.status_code == 200

    # ASSERT: Gimme data, verify it matches
    data = response.get_json()
    print(data)
    returned_coin = next(item for item in data if item["id"] == str(test_coin.id))

    assert returned_coin["id"] == str(test_coin.id)
    assert returned_coin["name"] == "COIN_TEST"


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


def test_add_coin(admin_client):
    payload = {"id": str(uuid.uuid4()), "name": "POST_COIN_TEST"}

    response = admin_client.post("/coins", json=payload)
    assert response.status_code == 201

    data = response.get_json()
    print(data)
    assert data["name"] == "POST_COIN_TEST"
    assert data["id"] == str(payload["id"])


def test_coin_post_request_returns_409_for_duplicate_coin(admin_client, test_coin):

    payload = {"id": str(uuid.uuid4()), "name": "COIN_TEST"}

    response = admin_client.post("/coins", json=payload)
    data = response.get_json()
    assert response.status_code == 409
    assert data["error"] == "Coin already exists"


def test_coin_put_request_returns_409_for_duplicate_coin(admin_client, test_coin):

    second_test_coin = Coin.create(id=uuid.uuid4(), name="COIN_TEST_2")
    response = admin_client.put(
        f"/coins/{second_test_coin.id}", json={"name": "COIN_TEST"}
    )
    data = response.get_json()
    assert response.status_code == 409
    assert data["error"] == "Coin already exists"


def test_coin_post_request_returns_400_for_invalid_name(admin_client):

    payload = {"id": str(uuid.uuid4()), "name": "COIN_TEST_123"}

    response = admin_client.post("/coins", json=payload)
    data = response.get_json()
    assert response.status_code == 400
    assert data["error"] == "Coin names cannot contain numbers."


def test_coin_put_request_returns_400_for_invalid_name(admin_client, test_coin):
    response = admin_client.put(f"/coins/{test_coin.id}", json={"name": "Coin 123"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "Coin names cannot contain numbers."


def test_unauthenticated_user_returns_401_for_coin_put_request(client):
    response = client.put(f"/coins/{uuid.uuid4()}")
    assert response.status_code == 401


def test_unauthenticated_user_returns_401_for_coin_post_request(client):
    response = client.post("/coins")
    assert response.status_code == 401


def test_unauthenticated_user_returns_401_for_coin_delete_request(client):
    response = client.delete(f"/coins/{uuid.uuid4()}")
    assert response.status_code == 401


def test_unauthorised_user_returns_403_for_coin_post_request(user_client):
    response = user_client.post("/coins")
    assert response.status_code == 403


def test_unauthorised_user_returns_403_for_coin_delete_request(user_client):
    response = user_client.delete(f"/coins/{uuid.uuid4()}")
    assert response.status_code == 403


def test_delete_coin_successfully(admin_client):
    coin = Coin.create(name="COIN_TEST")

    response = admin_client.delete(f"/coins/{coin.id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Coin deleted successfully"

    assert Coin.select().where(Coin.id == coin.id).count() == 0


def test_delete_coin_endpoint_returns_404(admin_client):
    response = admin_client.delete(f"/coins/{uuid.uuid4()}")

    data = response.get_json()
    assert response.status_code == 404

    assert data["error"] == "Coin does not exist"


def test_put_request_updates_coin_name(user_client):
    coin = Coin.create(name="COIN_TEST")

    json_payload = {"name": "NIOC_TSET"}

    response = user_client.put(f"/coins/{coin.id}", json=json_payload)
    data = response.get_json()

    db_coin = Coin.get_by_id(coin.id)

    assert response.status_code == 200
    assert data["name"] == "NIOC_TSET"
    assert db_coin.name == "NIOC_TSET"


def test_update_coin_endpoint_returns_404_if_uuid_not_found(user_client):
    random_uuid = uuid.uuid4()
    payload = {"name": "NON_EXISTENT_COIN"}

    response = user_client.put(f"/coins/{random_uuid}", json=payload)
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Coin does not exist"
