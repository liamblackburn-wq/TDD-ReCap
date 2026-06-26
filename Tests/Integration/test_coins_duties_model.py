import uuid

from src.models import CoinsDutiesJunction


def test_associate_duty_to_coin(test_coin, test_duty, client):
    payload = {"coin_id": str(test_coin.id), "duty_id": str(test_duty.id)}

    response = client.post("/coin-duties", json=payload)
    assert response.status_code == 201

    associated_ids = (
        CoinsDutiesJunction.select()
        .where(
            CoinsDutiesJunction.coin == test_coin.id,
            CoinsDutiesJunction.duty == test_duty.id,
        )
        .exists()
    )

    assert associated_ids is True


def test_duplicate_duty_returns_409(test_coin, test_duty, client):

    CoinsDutiesJunction.create(coin=test_coin.id, duty=test_duty.id)

    duplicate_payload = {"coin_id": str(test_coin.id), "duty_id": str(test_duty.id)}

    response = client.post("/coin-duties", json=duplicate_payload)

    assert response.status_code == 409
    assert response.json["error"] == "Duty is already assigned to coin"


def test_missing_coin_returns_404(client, test_duty):
    random_coin_uuid = uuid.uuid4()

    payload = {"coin_id": str(random_coin_uuid), "duty_id": str(test_duty.id)}

    response = client.post("/coin-duties", json=payload)

    assert response.status_code == 404
    assert response.json["error"] == "Coin does not exist"


def test_missing_duty_returns_404(client, test_coin):
    random_duty_uuid = uuid.uuid4()

    payload = {"coin_id": str(test_coin.id), "duty_id": str(random_duty_uuid)}

    response = client.post("/coin-duties", json=payload)

    assert response.status_code == 404
    assert response.json["error"] == "Duty does not exist"


def test_duty_complete_returns_200(client, test_coin, test_duty):

    link = CoinsDutiesJunction.create(coin=test_coin.id, duty=test_duty.id)

    payload = {
        "is_complete": True,
    }

    response = client.put(f"/coin-duties/{link.id}", json=payload)

    updated_link = CoinsDutiesJunction.get_by_id(link.id)
    assert response.status_code == 200
    assert updated_link.is_complete is True


def test_put_request_with_missing_link_returns_404(client, test_coin, test_duty):
    random_link_uuid = uuid.uuid4()

    payload = {
        "is_complete": True,
    }

    response = client.put(f"/coin-duties/{random_link_uuid}", json=payload)
    assert response.status_code == 404
    assert response.json["error"] == "Link does not exist"
