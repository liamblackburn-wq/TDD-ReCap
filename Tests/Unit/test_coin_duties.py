import uuid
import pytest
from peewee import IntegrityError
from src.models import Coin, CoinsDutiesJunction


def test_junction_creation_defaults_is_complete_to_false(test_coin, test_duty):
    link = CoinsDutiesJunction.create(coin=test_coin, duty=test_duty)

    assert link.is_complete is False


def test_junction_establishes_foreign_key_relationships(test_coin, test_duty):
    link = CoinsDutiesJunction.create(coin=test_coin, duty=test_duty)

    assert link.coin.id == test_coin.id
    assert link.duty.id == test_duty.id

    assert link in list(test_coin.assigned_duties)
    assert link in list(test_duty.assigned_coins)


def test_junction_enforces_unique_coin_and_duty_constraint(test_coin, test_duty):
    CoinsDutiesJunction.create(coin=test_coin, duty=test_duty)

    with pytest.raises(IntegrityError):
        CoinsDutiesJunction.create(coin=test_coin, duty=test_duty)


def test_cascade_delete_removes_junction_on_coin_deletion(test_duty):
    coin = Coin.create(id=uuid.uuid4(), name="COIN_CASCADE_TEST")
    link = CoinsDutiesJunction.create(coin=coin, duty=test_duty)

    coin.delete_instance(recursive=True)

    assert CoinsDutiesJunction.get_or_none(CoinsDutiesJunction.id == link.id) is None