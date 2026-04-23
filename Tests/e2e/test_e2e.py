from playwright.sync_api import Page, expect
from app import app as my_app
import pytest



@pytest.fixture(scope="session")
def app():
    return my_app


def xtest_heading_text_exists(page: Page, live_server):
    page.goto(live_server.url())
    expect(page.get_by_role("heading", name="Apprentice Duties")).to_contain_text('Apprentice Duties')

def xtest_home_page_is_reachable():
    with my_app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_add_new_duties_button_is_visible(page: Page, live_server):
    page.goto(live_server.url())
    expect(page.get_by_role("button", name="Add New Duty")).to_be_visible()