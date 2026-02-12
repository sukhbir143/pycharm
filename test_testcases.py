import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.parametrize("username,password", [
    ("sukhbir.deswal+support@singleinterface.com", "1aac080a3729BC"),
    ("sukhbir.deswal@singleinterface.com", "616e0f")
])
def test_demo_nova(username, password):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://backend-dashboard.singleinterface.com/pages/index.html")
        page.wait_for_load_state("networkidle")

        page.locator("input[type='email']").fill(username)
        page.locator("input[type='password']").fill(password)
        page.locator("button:has-text('Sign In')").click()

        page.wait_for_timeout(3000)
        browser.close()

