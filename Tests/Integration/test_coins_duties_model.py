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

    CoinsDutiesJunction.delete().where(
        CoinsDutiesJunction.coin == test_coin.id,
        CoinsDutiesJunction.duty == test_duty.id
    ).execute()