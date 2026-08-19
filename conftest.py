import os
import threading

from werkzeug.serving import make_server

os.environ["TESTING"] = "True"
import uuid
import pytest
from playwright.sync_api import Page

from src.models import CoinsDutiesJunction, Coin, User, RequestLog, Duty


@pytest.fixture(scope="session", autouse=True)
def setup_test_database_tables():
    from src.db import db
    from src.models import Duty

    db.connect(reuse_if_open=True)

    db.execute_sql("CREATE SCHEMA IF NOT EXISTS coins_test;")

    db.drop_tables([Coin, Duty, CoinsDutiesJunction, User, RequestLog], safe=True)
    db.create_tables([Coin, Duty, CoinsDutiesJunction, User, RequestLog], safe=False)

    yield

    db.drop_tables([Coin, Duty, CoinsDutiesJunction, User, RequestLog])
    db.close()


@pytest.fixture(scope="session")
def app():
    from app import app as flask_app

    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def admin_client(client):
    client.post("/api/login", json={"username": "admin", "password": "admin123"})
    return client


@pytest.fixture
def user_client(client):
    client.post("/api/login", json={"username": "user", "password": "user123"})
    return client


@pytest.fixture
def test_duty():
    from src.models import Duty

    Duty.delete().where(Duty.name == "Duty 1").execute()
    test_duty = Duty.create(
        id=uuid.uuid4(), name="Duty 1", description="TEST DESCRIPTION"
    )
    yield test_duty

    Duty.delete().where(Duty.id == test_duty.id).execute()


@pytest.fixture
def test_coin():
    from src.models import Coin

    test_coin = Coin.create(id=uuid.uuid4(), name="COIN_TEST")
    yield test_coin
    Coin.delete().where(Coin.id == test_coin.id).execute()


@pytest.fixture
def assigned_duty(test_coin, test_duty):
    return CoinsDutiesJunction.create(coin=test_coin, duty=test_duty)


@pytest.fixture(autouse=True)
def clean_database_and_seed_users_between_tests():
    CoinsDutiesJunction.delete().execute()
    Coin.delete().execute()
    Duty.delete().execute()
    User.delete().execute()

    # Seed test users into database with hashed passwords
    admin = User(username="admin", role="admin")
    admin.set_password("admin123")
    admin.save(force_insert=True)

    user = User(username="user", role="user")
    user.set_password("user123")
    user.save(force_insert=True)

    yield


@pytest.fixture(scope="session")
def live_server(app):
    # Start the Flask app in a background server thread on port 5000
    server = make_server("127.0.0.1", 5000, app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    class ExternalServer:
        def __init__(self, flask_app):
            self.app = flask_app

        def url(self, path=""):
            return f"http://127.0.0.1:5000{path}"

    yield ExternalServer(app)
    server.shutdown()
    thread.join()


@pytest.fixture
def admin_page(page: Page, live_server):
    page.goto(live_server.url("/"))
    username_field = page.get_by_label("Username")
    password_field = page.get_by_label("Password")
    login_button = page.locator("#login-button")

    username_field.fill("admin")
    password_field.fill("admin123")
    login_button.click()

    page.wait_for_url("**/apprenticeduties")
    yield page


@pytest.fixture
def user_page(page: Page, live_server):
    page.goto(live_server.url("/"))
    username_field = page.get_by_label("Username")
    password_field = page.get_by_label("Password")
    login_button = page.locator("#login-button")
    username_field.fill("user")
    password_field.fill("")

    username_field.fill("user")
    password_field.fill("user123")
    login_button.click()
    yield page
