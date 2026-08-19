from playwright.sync_api import Page, expect
import pytest


@pytest.fixture
def homepage(page: Page, live_server):
    page.goto(live_server.url())
    return page


@pytest.fixture
def revealed_form(admin_page: Page):
    admin_page.get_by_role("button", name="Create Duty").click()
    yield admin_page


def test_login_page_is_reachable(page: Page, live_server):
    page.goto(live_server.url("/"))
    expect(page.locator("#login-view")).to_be_visible()


def test_login_page_heading_text_exists(homepage: Page):
    expect(homepage.get_by_role("heading", name="Apprentice Duties")).to_contain_text(
        "Apprentice Duties"
    )


def test_add_duties_button_is_visible_and_reveals_form_when_clicked(
    revealed_form: Page,
):
    add_duties_button = revealed_form.get_by_role("button", name="Create Duty")
    expect(add_duties_button).to_be_visible()
    add_duties_button.click()
    expect(revealed_form.get_by_role("form", name="Create Duty Form")).to_be_visible()


def test_submit_button_creates_and_renders_duty_in_dropdown(
    revealed_form: Page, test_coin
):
    duty_form = revealed_form.locator("#duty-form")
    submit_button = duty_form.get_by_role("button", name="Submit")

    duty_form.get_by_label("Duty Name:", exact=True).fill("Duty 5")
    duty_form.get_by_label("Duty Description:").fill("Test description")

    expect(submit_button).to_be_visible()
    submit_button.click()

    expect(duty_form).not_to_be_visible()
    expect(revealed_form.locator(".duty-option")).to_contain_text("Duty 5")


def test_remove_duties_button(admin_page: Page, assigned_duty):

    duty_item = admin_page.locator(".listed-duty", has_text="Duty 1")
    duty_item.get_by_role("button", name="Unassign").click()

    expect(duty_item).not_to_be_visible()

def test_admin_dashboard_loads(admin_page):
    expect(admin_page.locator('#admin-view')).to_be_visible()