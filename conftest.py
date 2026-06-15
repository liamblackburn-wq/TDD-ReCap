import os
import uuid
import pytest

os.environ['TESTING'] = 'True'

@pytest.fixture(scope='session', autouse=True)
def setup_test_database_tables():
    from src.db import db
    from src.models import Duty

    db.connect(reuse_if_open=True)

    db.drop_tables([Duty], safe=True)
    db.create_tables([Duty], safe=True)

    yield

    db.drop_tables([Duty])
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

@pytest.fixture(scope='session')
def live_server():
    class ExternalServer:
        def url(self, path=""):
            # Point this to whatever port your local Flask app is running on
            return f"http://127.0.0.1:5000{path}"
    return ExternalServer()