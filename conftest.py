import os
import uuid
import pytest

from src.models import CoinsDutiesJunction, Coin

os.environ['TESTING'] = 'True'

@pytest.fixture(scope='session', autouse=True)
def setup_test_database_tables():
    from src.db import db
    from src.models import Duty

    db.connect(reuse_if_open=True)

    db.execute_sql('CREATE SCHEMA IF NOT EXISTS coins_test;')

    db.drop_tables([Coin, Duty, CoinsDutiesJunction], safe=True)
    db.create_tables([Coin, Duty, CoinsDutiesJunction], safe=False)

    yield

    db.drop_tables([Coin, Duty, CoinsDutiesJunction])
    db.close()

@pytest.fixture(scope='session')
def app():
    from app import app as flask_app
    flask_app.config['TESTING'] = True
    return flask_app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_duty():
    from src.models import Duty
    Duty.delete().where(Duty.name == 'Duty 1').execute()
    # ARRANGE: Create the test duty with an uuid
    test_duty = Duty.create(id=uuid.uuid4(), name='Duty 1', description='TEST DESCRIPTION')
    yield test_duty

    Duty.delete().where(Duty.id == test_duty.id).execute()

@pytest.fixture
def test_coin():
    from src.models import Coin
    # ARRANGE: Create the test coin with an uuid
    test_coin = Coin.create(id=uuid.uuid4(), name='COIN_TEST')
    yield test_coin
    Coin.delete().where(Coin.id == test_coin.id).execute()


@pytest.fixture(scope='session')
def live_server():
    class ExternalServer:
        def url(self, path=""):
            # Point this to whatever port your local Flask app is running on
            return f"http://127.0.0.1:5000{path}"
    return ExternalServer()