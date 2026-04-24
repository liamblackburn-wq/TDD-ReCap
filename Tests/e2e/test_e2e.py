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

def xtest_add_duties_button_is_visible_and_clickable(page: Page, live_server):
    page.goto(live_server.url())

    add_duties_button = page.get_by_role("button", name="Add Duties")
    expect(add_duties_button).to_be_visible()
    add_duties_button.click()
    expect(page.get_by_role("form", name="Add Duty Form" )).to_be_visible()

def test_correct_amount_of_duties_in_dropdown(page: Page, live_server):
    page.goto(live_server.url())
    add_duties_button = page.get_by_role("button", name="Add Duties")
    add_duties_button.click()
    checkboxes = page.get_by_role("checkbox")
    expect(checkboxes).to_have_count(13)