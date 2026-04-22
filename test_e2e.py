from playwright.sync_api import Page, expect

def test_response_returns_ok(page: Page):
    response = page.request.get("http://127.0.0.1:5000")
    expect(response).to_be_ok()

