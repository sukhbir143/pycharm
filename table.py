import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.parametrize("my_browser",["chromium", "firefox"])
@pytest.mark.parametrize(
    "username, password",
    [
        ("student", "Password123"),
        ("students", "Password123"),
    ]
)
def test_cross_browser(my_browser, username, password):
    with sync_playwright() as p:
       browser = getattr(p, my_browser).launch(headless=False, slow_mo=2000)
       page = browser.new_page()
       page.goto("https://practicetestautomation.com/practice-test-login/")
       page.fill("#username", "username")
       page.fill("#password", "password")

       browser.close()