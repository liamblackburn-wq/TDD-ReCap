from playwright.sync_api import Page, expect
from app import app as flask_app
import pytest

test_app = flask_app.test_client()

test_app.get('/')

@pytest.fixture(scope="session")
def app():
    return flask_app

def test_header_exists(page: Page, live_server):
    page.goto(live_server.url())
    expect(page.get_by_role("heading", name="Apprentice Duties")).to_contain_text('Apprentice Duties')

def test_home_page_is_reachable():
    response = test_app.get('/')
    assert response.status_code is 200

# def test_response_returns_ok(page: Page):
#     response = page.request.get("http://127.0.0.1:5000")
#     expect(response).to_be_ok()
