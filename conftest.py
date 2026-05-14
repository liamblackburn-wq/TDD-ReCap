import os

os.environ['TEST_DATABASE_PATH'] = 'test_duties.db'

import pytest
from seed_db import setup_database
from app import app as my_app


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    test_db = os.environ['TEST_DATABASE_PATH']

    setup_database(test_db)
    print("Database setup complete.")

    yield

    if os.path.exists(test_db):
        os.remove(test_db)


@pytest.fixture(scope="session")
def app():
    return my_app