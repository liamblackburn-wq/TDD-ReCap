from playwright.sync_api import Page, expect
from app import app as my_app
import pytest



@pytest.fixture(scope="session")
def app():
    return my_app


def test_heading_text_exists(page: Page, live_server):
    page.goto(live_server.url())
    expect(page.get_by_role("heading", name="Apprentice Duties")).to_contain_text('Apprentice Duties')

def test_home_page_is_reachable():
    with my_app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

# def test_response_returns_ok(page: Page):
#     response = test_app.get("http://127.0.0.1:5000")
#     expect(response).to_be_ok()
