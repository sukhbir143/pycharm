import pytest

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=3000)
    page = browser.new_page()
    page.goto("https://www.amazon.com/")

    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.locator("//a[normalize-space()='Amazon Devices']").click()

    browser.close()