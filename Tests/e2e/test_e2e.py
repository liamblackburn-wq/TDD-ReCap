from playwright.sync_api import Page, expect
from app import app as my_app
import pytest



@pytest.fixture(scope="session")
def app():
    return my_app

@pytest.fixture
def homepage(page: Page, live_server):
    page.goto(live_server.url())
    return page

@pytest.fixture
def revealed_form(homepage: Page):
    homepage.get_by_role("button", name="Add Duties").click()
    return homepage

def xtest_home_page_is_reachable():
    with my_app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_heading_text_exists(homepage: Page):
    expect(homepage.get_by_role("heading", name="Apprentice Duties")).to_contain_text('Apprentice Duties')

def test_add_duties_button_is_visible_and_clickable(homepage: Page):

    add_duties_button = homepage.get_by_role("button", name="Add Duties")
    expect(add_duties_button).to_be_visible()
    add_duties_button.click()
    expect(homepage.get_by_role("form", name="Add Duty Form" )).to_be_visible()

def test_correct_amount_of_duty_checkboxes(revealed_form: Page):
    checkboxes = revealed_form.get_by_role("checkbox")
    expect(checkboxes).to_have_count(13)

def test_individual_duty_exists_and_checked(revealed_form: Page):
    duty_5_check = revealed_form.get_by_label("Duty 5")
    duty_5_check.check()
    expect(duty_5_check).to_be_checked()