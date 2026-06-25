from src.models import CoinsDutiesJunction


def test_associate_duty_to_coin(test_coin, test_duty, client):
    payload = {
        "coin_id": str(test_coin.id),
        "duty_id": str(test_duty.id)
    }

    response = client.post('/coin-duties', json=payload)
    assert response.status_code == 201

    associated_ids = CoinsDutiesJunction.select().where(
        CoinsDutiesJunction.coin == test_coin.id,
        CoinsDutiesJunction.duty == test_duty.id
    ).exists()

    assert associated_ids == True

def test_duplicate_duty_returns_409(test_coin, test_duty, client):

    CoinsDutiesJunction.create(coin=test_coin.id, duty=test_duty.id)

    duplicate_payload = {
        "coin_id": str(test_coin.id),
        "duty_id": str(test_duty.id)
    }

    response = client.post('/coin-duties', json=duplicate_payload)

    assert response.status_code == 409
    assert response.json['error'] == 'Duty is already assigned to coin'