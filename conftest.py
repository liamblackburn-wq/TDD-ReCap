import pytest
import uuid

@pytest.fixture(scope='session', autouse=True)
def setup_test_database_tables():
    from src.db import db
    from src.models import Duty


    getattr(Duty, '_meta').table_name = 'tdd-safari-test_duties'

    db.connect(reuse_if_open=True)

    db.drop_tables([Duty])
    db.create_tables([Duty])

    yield

    db.drop_tables([Duty])
    db.close()

@pytest.fixture
def client():
    from app import app

    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@pytest.fixture
def test_duty():
    from src.models import Duty
    Duty.delete().where(Duty.name == 'DUTY_TEST').execute()
    # ARRANGE: Create the test duty with an uuid
    test_duty = Duty.create(id=uuid.uuid4(), name='DUTY_TEST', description='TEST DESCRIPTION')
    yield test_duty

    Duty.delete().where(Duty.id == test_duty.id).execute()