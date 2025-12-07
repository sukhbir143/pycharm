from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=2000)
    page = browser.new_page()

    page.goto('https://dev-backend-dashboard.singleinterface.com/pages/index.html')

    # Login
    page.fill('#email', 'sukhbir.deswal+supportadmin@singleinterface.com')
    page.fill('#password', '3e39e1')
    page.click('#loginBtn')
    page.wait_for_load_state('networkidle')

    # Search client
    page.fill('#clientSerch', 'sangeet')
    time.sleep(1)
    page.click('a.client_link')
    page.wait_for_load_state('networkidle')

    # Click insight
    page.click("//img[@src='../assets/img/ic-insight.svg']")
    time.sleep(1)

    # Click review - FIXED
    page.click("(//a[@class='dropdown-item'])[13]")
    page.wait_for_load_state('networkidle')

    # Click filter - FIXED
    page.click('i.material-icons-outlined.drop-arrow.ms-1')

    time.sleep(3)
    browser.close()