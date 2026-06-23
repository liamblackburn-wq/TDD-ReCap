import pytest
import uuid
from src.models import Duty, Coin, CoinsDutiesJunction


def test_coin_features():
    test_coin = Coin(
        id=uuid.uuid4(),
        name="Automate!",
    )
    assert test_coin.name ==  "Automate!"

def test_coins_with_same_features_are_equal():
    coin_1 = Coin(
        id=uuid.uuid4(),
        name="Automate!",
    )
    coin_2 = Coin(
        id=uuid.uuid4(),
        name="Automate!",
    )
    assert coin_1 == coin_2

def test_coins_with_different_features_are_not_equal():
    coin_1 = Coin(
        id=uuid.uuid4(),
        name="Automate!",
    )
    coin_2 = Coin(
        id=uuid.uuid4(),
        name="Going Deeper",
    )

    assert coin_1 != coin_2

def test_invalid_coin_raises_error():
    error_message = "Coin names can not contain numbers."
    invalid_coin = Coin(
        id=uuid.uuid4(),
        name="Coin 12345",
    )

    with pytest.raises(ValueError, match=error_message):
        invalid_coin.validate()

def test_coin_status_is_in_progress_if_specific_duties_are_incomplete(client):
    coin = Coin.create(name="Test Coin")
    duty_a = Duty.create(id=uuid.uuid4(), name="Duty 1", description="Test description 1")
    duty_b = Duty.create(id=uuid.uuid4(), name="Duty 2", description="Test description 2")

    CoinsDutiesJunction.create(coin=coin, duty=duty_a, is_complete=True)
    CoinsDutiesJunction.create(coin=coin, duty=duty_b, is_complete=False)

    assert coin.status == "IN_PROGRESS"

def test_coin_status_is_in_progress_if_specific_duties_are_complete(client):
    coin = Coin.create(name="Test Coin")
    duty_a = Duty.create(id=uuid.uuid4(), name="Duty 1", description="Test description 1")
    duty_b = Duty.create(id=uuid.uuid4(), name="Duty 2", description="Test description 2")

    CoinsDutiesJunction.create(coin=coin, duty=duty_a, is_complete=True)
    CoinsDutiesJunction.create(coin=coin, duty=duty_b, is_complete=True)

    assert coin.status == "COMPLETED"