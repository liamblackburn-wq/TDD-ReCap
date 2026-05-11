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

def test_home_page_is_reachable():
    with my_app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200

def test_heading_text_exists(homepage: Page):
    expect(homepage.get_by_role("heading", name="Apprentice Duties")).to_contain_text('Apprentice Duties')

def test_add_duties_button_is_visible_and_reveals_form_when_clicked(homepage: Page):
    add_duties_button = homepage.get_by_role("button", name="Add Duties")
    expect(add_duties_button).to_be_visible()
    add_duties_button.click()
    expect(homepage.get_by_role("form", name="Add Duty Form" )).to_be_visible()

def test_correct_amount_of_duty_checkboxes(revealed_form: Page):
    checkboxes = revealed_form.get_by_role("checkbox")
    expect(checkboxes).to_have_count(13)

def test_individual_duty_exists_and_checked(revealed_form: Page):
    duty_5 = revealed_form.get_by_label("Duty 5")
    duty_5.check()
    expect(duty_5).to_be_checked()

def test_submit_button(revealed_form: Page):
    automate_duties_list = revealed_form.get_by_role("list", name="Automate Duties List")
    submit_button = revealed_form.get_by_role("button", name="Submit")
    duty_5 = revealed_form.get_by_label("Duty 5")

    duty_5.check()

    expect(automate_duties_list).to_be_attached()
    expect(automate_duties_list).to_be_empty()
    expect(submit_button).to_be_visible()

    submit_button.click()

    expect(automate_duties_list).to_contain_text("Duty 5")
    expect(revealed_form.get_by_role("form", name="Add Duty Form" )).not_to_be_visible()
