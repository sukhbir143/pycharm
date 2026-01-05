from playwright.sync_api import sync_playwright
import time

with (sync_playwright() as p):
    browser = p.chromium.launch(headless=False, slow_mo=5000)
    page = browser.new_page()
    # login in demo
    page.goto('https://demo-nova.singleinterface.com/login')
    email = page.wait_for_selector("//input[@placeholder='Enter your email']")
    email.type("super_admin_hdfcLife@singleinterface.com")
    password = page.wait_for_selector("//input[@placeholder='Enter your password']")
    password.type("password123")
    signin = page.wait_for_selector("//button[normalize-space()='Sign In']")
    signin.click()


    # competitor ai dashboard

    competitorAI = page.wait_for_selector("//span[@class='ml-3'][normalize-space()='Competitor AI']")
    competitorAI.click()
    searchbrand = page.wait_for_selector("//input[@placeholder='Search by name or address...']")
    searchbrand.click()

    #select brand form list
    slebrand = page.wait_for_selector("body > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > main:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > button:nth-child(1)")
    slebrand.click()

    # My Competitors list
    threedots = page.locator("(//i)[33]")
    threedots.click()

    # edit button
    editbutton= page.locator("(//button)[20]")
    editbutton.click()

    # Edit Business Location
    searchbrand = page.wait_for_selector("//input[@id='location-search']")
    searchbrand.type("tata motors")

    sellocation = page.wait_for_selector("body > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > main:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > button:nth-child(1) > div:nth-child(1) > p:nth-child(2)")
    sellocation.click()

    updatelocations = page.wait_for_selector("//button[normalize-space()='Update Location']")
    updatelocations.click()

    # cancel button
    cancelbutton = page .wait_for_selector("//button[normalize-space()='Cancel']")
    cancelbutton.click()

    # Business Info
    Businessinfo = page.wait_for_selector("//span[normalize-space()='Business Info']")
    Businessinfo.click()

    # Attributes
    Attributes = page.wait_for_selector("//span[normalize-space()='Attributes']")
    Attributes.click()


    # three dots
    threedots = page.locator("(//i)[33]")
    threedots.click()

    comparewithme = page.locator("(//span[contains(text(),'Compare with Me')])[1]")
    comparewithme.click()

    # Competitor Comparison
    businessinfo = page.wait_for_selector("(//span[contains(text(),'Business Info')])[1]")
    businessinfo.click()

    Att = page.wait_for_selector("(//span[contains(text(),'Attributes')])[1]")
    Att.click()

    close = page.wait_for_selector("//button[normalize-space()='Close']")
    close.click()

    # three dots
    threedots = page.locator("(//i)[33]")
    threedots.click()

    # View on Google
    viewongoogle = page.wait_for_selector("(//span[contains(text(),'View on Google')])[1]")
    viewongoogle.click()

    # Map rank Tracker
    mapranktracker = page.wait_for_selector("//span[normalize-space()='Map Rank Tracker']")
    mapranktracker.click()

    # new scan
    Newscan = page.wait_for_selector("//span[normalize-space()='New Scan']")
    Newscan.click()

    # Search box
    searchbox = page.wait_for_selector("//input[contains(@placeholder,'Search by Name, Id, Address, Pincode...')]")
    searchbox.type("hdfc")


    # select brand
    Selbrand = page.wait_for_selector("//p[normalize-space()='1st Floor, Balurghat, West Bengal']")
    Selbrand.click()

    # select keyword
    AIkeywords = page.wait_for_selector("//span[normalize-space()='Cafe service']")
    AIkeywords.click()

    # Scan Now
    Scannow = page.wait_for_selector("//span[normalize-space()='Scan Now']")
    Scannow.click()

    # dashboard again
    dashborad = page.wait_for_selector("//a[@href='/dashboard-competition'][normalize-space()='Dashboard']")
    dashborad.click()

    with page.expect_download() as download:
        page.click("text=Export Data")
    download.value.save_as("file.pdf")

















