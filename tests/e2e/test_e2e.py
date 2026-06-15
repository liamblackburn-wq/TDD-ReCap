from playwright.sync_api import Page, expect
import pytest

@pytest.fixture
def homepage(page: Page, live_server):
    page.goto(live_server.url())
    return page

@pytest.fixture
def revealed_form(homepage: Page):
    homepage.get_by_role("button", name="Add Duty").click()
    return homepage
#
# @pytest.fixture
# def setup_duty(revealed_form: Page):
#

def test_home_page_is_reachable(page: Page, live_server):
    response = page.goto(live_server.url())
    assert response.status == 200

def test_heading_text_exists(homepage: Page):
    expect(homepage.get_by_role("heading", name="Apprentice Duties")).to_contain_text('Apprentice Duties')

def test_add_duties_button_is_visible_and_reveals_form_when_clicked(homepage: Page):
    add_duties_button = homepage.get_by_role("button", name="Add Duty")
    expect(add_duties_button).to_be_visible()
    add_duties_button.click()
    expect(homepage.get_by_role("form", name="Add Duty Form" )).to_be_visible()


def test_submit_button_creates_and_renders_duty(revealed_form: Page):
    automate_duties_list = revealed_form.get_by_role("list", name="Automate Duties List")
    submit_button = revealed_form.get_by_role("button", name="Submit")

    revealed_form.get_by_label("Duty Name:", exact=True).fill("Duty 5")
    revealed_form.get_by_label("Duty Description:").fill("Test description")

    expect(automate_duties_list).to_be_attached()
    expect(submit_button).to_be_visible()

    submit_button.click()

    expect(automate_duties_list).to_contain_text("Duty 5")
    expect(automate_duties_list).to_contain_text("Test description")
    expect(revealed_form.get_by_role("form", name="Add Duty Form" )).not_to_be_visible()

def test_remove_duties_button(revealed_form: Page):
    automate_duties_list = revealed_form.get_by_role("list", name="Automate Duties List")
    submit_button = revealed_form.get_by_role("button", name="Submit")

    revealed_form.get_by_label("Duty Name:", exact=True).fill("Duty 5")
    revealed_form.get_by_label("Duty Description:").fill("Test description")

    expect(automate_duties_list).to_be_attached()
    expect(submit_button).to_be_visible()

    submit_button.click()

    list_items = automate_duties_list.get_by_role("listitem")
    expect(list_items).to_have_count(1)

    duty_5_list_item = list_items.filter(has_text="Duty 5")

    remove_duty_5_button = duty_5_list_item.get_by_role("button", name="X")
    remove_duty_5_button.click()

    expect(list_items).to_have_count(0)
    expect(automate_duties_list).not_to_contain_text("Duty 5")
