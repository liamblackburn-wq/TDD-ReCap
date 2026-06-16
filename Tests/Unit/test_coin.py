import pytest
import uuid
from src.models import Duty

def test_coin_features():
    test_coin = Coin(
        id=uuid.uuid4(),
        name="Coin 1",
        description="Test Description"
    )
    assert test_coin.name ==  "Coin 1"
    assert test_coin.description == "Test Description"

def test_coins_with_same_features_are_equal():
    coin_1 = Coin(
        id=uuid.uuid4(),
        name="Coin 5",
        description="CI/CD"
    )
    coin_2 = Coin(
        id=uuid.uuid4(),
        name="Coin 5",
        description="CI/CD"
    )

    assert coin_1 == coin_2

def test_coins_with_different_features_are_not_equal():
    coin_1 = Coin(
        id=uuid.uuid4(),
        name="Coin 5",
        description="CI/CD"
    )
    coin_2 = Coin(
        id=uuid.uuid4(),
        name="Coin 5",
        description="Different Description"
    )

    coin_3 = Coin(
        id=uuid.uuid4(),
        name="Coin 5",
        description="CI/CD"
    )
    coin_4 = Coin(
        id=uuid.uuid4(),
        name="Coin 6",
        description="CI/CD"
    )

    assert coin_1 != coin_2
    assert coin_3 != coin_4

def test_invalid_coin_raises_error():
    error_message = "Coin name must start with 'Coin' followed by a number."
    invalid_coin = Coin(
        id=uuid.uuid4(),
        name="WRONG",
        description="WRONG"
    )

    with pytest.raises(ValueError, match=error_message):
        invalid_coin.validate()