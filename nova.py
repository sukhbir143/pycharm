from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=5000)
    context = browser.new_context()
    page = browser.new_page()
    page.goto("https://backend-dashboard.singleinterface.com/pages/index.html")
    emailid = page.wait_for_selector('input[name="email"]')
    emailid.type('sukhbir.deswal+supportadmin@singleinterface.com')
    password = page.wait_for_selector('input[id="password"]')
    password.type('3e39e1')
    signin = page.wait_for_selector('button[type="button"]')
    signin.click()
    elements = page.query_selector_all('h6')
    print(len(elements))
    for i in elements:
        print(i.text_content())
    search = page.wait_for_selector('input[type="text"]')
    search.type('Sangeetha')
    click = page.wait_for_selector('a[class="client_link"]')
    click.click()
    filter_button = page.wait_for_selector("//span[@class='Alt-din-font filter-class-btn']")
    filter_button.click()


