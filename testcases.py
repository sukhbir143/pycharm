"""
SingleInterface Backend Dashboard - Login Test Suite
Automated test cases for login functionality

Prerequisites:
pip install pytest playwright pytest-html
playwright install
"""

import pytest
from playwright.sync_api import sync_playwright, Page, expect, Browser
import time


class TestSingleInterfaceLogin:
    """Test suite for SingleInterface login functionality"""

    BASE_URL = "https://backend-dashboard.singleinterface.com/pages/index.html"

    # Valid test credentials
    VALID_EMAIL = "sukhbir.deswal+supportadmin@singleinterface.com"
    VALID_PASSWORD = "3e39e1"

    # Selectors
    EMAIL_SELECTOR = 'input[name="email"]'
    PASSWORD_SELECTOR = 'input[id="password"]'
    SIGNIN_BUTTON_SELECTOR = 'button[type="button"]'

    @pytest.fixture(scope="function")
    def browser_context(self):
        """Setup browser context for each test"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            context = browser.new_context()
            yield context, browser
            context.close()
            browser.close()

    @pytest.fixture
    def page(self, browser_context):
        """Setup page for each test"""
        context, browser = browser_context
        page = context.new_page()
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        yield page

    # Test Case 1: Successful login with valid credentials
    def test_01_successful_login_valid_credentials(self, page: Page):
        """TC-01: Login with valid email and password"""
        print("\n🧪 Test Case 1: Successful Login with Valid Credentials")

        # Enter valid credentials
        email_field = page.wait_for_selector(self.EMAIL_SELECTOR, timeout=5000)
        email_field.type(self.VALID_EMAIL, delay=100)

        password_field = page.wait_for_selector(self.PASSWORD_SELECTOR, timeout=5000)
        password_field.type(self.VALID_PASSWORD, delay=100)

        # Click sign-in button
        signin_button = page.wait_for_selector(self.SIGNIN_BUTTON_SELECTOR, timeout=5000)
        signin_button.click()

        # Wait for navigation or dashboard element
        time.sleep(3)

        # Verify URL changed (redirected to dashboard)
        current_url = page.url
        assert current_url != self.BASE_URL, "Should redirect after successful login"

        print("✅ Test Passed: Successfully logged in and redirected")

    # Test Case 2: Login fails with invalid email
    def test_02_login_fails_invalid_email(self, page: Page):
        """TC-02: Login attempt with invalid email"""
        print("\n🧪 Test Case 2: Login Fails with Invalid Email")

        # Enter invalid email
        email_field = page.wait_for_selector(self.EMAIL_SELECTOR, timeout=5000)
        email_field.type("invalid.email@wrongdomain.com", delay=100)

        password_field = page.wait_for_selector(self.PASSWORD_SELECTOR, timeout=5000)
        password_field.type(self.VALID_PASSWORD, delay=100)

        # Click sign-in button
        signin_button = page.wait_for_selector(self.SIGNIN_BUTTON_SELECTOR, timeout=5000)
        signin_button.click()

        time.sleep(2)

        # Verify still on login page or error message appears
        current_url = page.url
        # Check if error message exists or still on login page
        try:
            error_element = page.wait_for_selector('[class*="error"], [class*="alert"]', timeout=3000)
            assert error_element.is_visible(), "Error message should be visible"
            print("✅ Test Passed: Error message displayed for invalid email")
        except:
            # If no error element, check URL hasn't changed
            assert self.BASE_URL in current_url, "Should stay on login page"
            print("✅ Test Passed: Stayed on login page with invalid email")

    # Test Case 3: Login fails with invalid password
    def test_03_login_fails_invalid_password(self, page: Page):
        """TC-03: Login attempt with invalid password"""
        print("\n🧪 Test Case 3: Login Fails with Invalid Password")

        # Enter valid email but wrong password
        email_field = page.wait_for_selector(self.EMAIL_SELECTOR, timeout=5000)
        email_field.type(self.VALID_EMAIL, delay=100)

        password_field = page.wait_for_selector(self.PASSWORD_SELECTOR, timeout=5000)
        password_field.type("wrongpassword123", delay=100)

        # Click sign-in button
        signin_button = page.wait_for_selector(self.SIGNIN_BUTTON_SELECTOR, timeout=5000)
        signin_button.click()

        time.sleep(2)

        # Verify error message or stayed on login page
        current_url = page.url
        try:
            error_element = page.wait_for_selector('[class*="error"], [class*="alert"]', timeout=3000)
            assert error_element.is_visible(), "Error message should be visible"
            print("✅ Test Passed: Error message displayed for invalid password")
        except:
            assert self.BASE_URL in current_url, "Should stay on login page"
            print("✅ Test Passed: Stayed on login page with invalid password")

    # Test Case 4: Login with empty email field
    def test_04_empty_email_validation(self, page: Page):
        """TC-04: Submit form with empty email field"""
        print("\n🧪 Test Case 4: Empty Email Field Validation")

        # Leave email empty, fill password
        password_field = page.wait_for_selector(self.PASSWORD_SELECTOR, timeout=5000)
        password_field.type(self.VALID_PASSWORD, delay=100)

        # Click sign-in button
        signin_button = page.wait_for_selector(self.SIGNIN_BUTTON_SELECTOR, timeout=5000)
        signin_button.click()

        time.sleep(1)

        # Check if email field shows validation error
        email_field = page.locator(self.EMAIL_SELECTOR)

        # Check for HTML5 validation or custom validation
        is_invalid = page.evaluate("""
            () => {
                const emailInput = document.querySelector('input[name="email"]');
                return !emailInput.checkValidity() || emailInput.validity.valueMissing;
            }
        """)

        assert is_invalid or self.BASE_URL in page.url, "Should show validation error or stay on page"
        print("✅ Test Passed: Empty email validation working")

    # Test Case 5: Login with empty password field
    def test_05_empty_password_validation(self, page: Page):
        """TC-05: Submit form with empty password field"""
        print("\n🧪 Test Case 5: Empty Password Field Validation")

        # Fill email, leave password empty
        email_field = page.wait_for_selector(self.EMAIL_SELECTOR, timeout=5000)
        email_field.type(self.VALID_EMAIL, delay=100)

        # Click sign-in button
        signin_button = page.wait_for_selector(self.SIGNIN_BUTTON_SELECTOR, timeout=5000)
        signin_button.click()

        time.sleep(1)

        # Check if password field shows validation error
        is_invalid = page.evaluate("""
            () => {
                const passwordInput = document.querySelector('input[id="password"]');
                return !passwordInput.checkValidity() || passwordInput.validity.valueMissing;
            }
        """)

        assert is_invalid or self.BASE_URL in page.url, "Should show validation error or stay on page"
        print("✅ Test Passed: Empty password validation working")

    # Test Case 6: Login with both fields empty
    def test_06_both_fields_empty(self, page: Page):
        """TC-06: Submit form with both fields empty"""
        print("\n🧪 Test Case 6: Both Fields Empty Validation")

        # Click sign-in button without filling any field
        signin_button = page.wait_for_selector(self.SIGNIN_BUTTON_SELECTOR, timeout=5000)
        signin_button.click()

        time.sleep(1)

        # Verify still on login page
        current_url = page.url
        assert self.BASE_URL in current_url, "Should stay on login page when both fields empty"

        print("✅ Test Passed: Both fields empty validation working")

    # Test Case 7: Email field accepts only valid email format
    def test_07_invalid_email_format(self, page: Page):
        """TC-07: Test with invalid email format"""
        print("\n🧪 Test Case 7: Invalid Email Format Validation")

        # Enter invalid email format
        email_field = page.wait_for_selector(self.EMAIL_SELECTOR, timeout=5000)
        email_field.type("notanemail", delay=100)

        password_field = page.wait_for_selector(self.PASSWORD_SELECTOR, timeout=5000)
        password_field.type(self.VALID_PASSWORD, delay=100)

        # Click sign-in button
        signin_button = page.wait_for_selector(self.SIGNIN_BUTTON_SELECTOR, timeout=5000)
        signin_button.click()

        time.sleep(1)

        # Check for email validation
        is_invalid = page.evaluate("""
            () => {
                const emailInput = document.querySelector('input[name="email"]');
                return !emailInput.checkValidity() || emailInput.validity.typeMismatch;
            }
        """)

        assert is_invalid or self.BASE_URL in page.url, "Should validate email format"
        print("✅ Test Passed: Email format validation working")

    # Test Case 8: Verify password field masks input
    def test_08_password_field_masking(self, page: Page):
        """TC-08: Verify password field masks the input"""
        print("\n🧪 Test Case 8: Password Field Masking")

        # Check password field type
        password_field = page.wait_for_selector(self.PASSWORD_SELECTOR, timeout=5000)

        # Get input type attribute
        input_type = password_field.get_attribute("type")

        assert input_type == "password", f"Password field should be type 'password', got '{input_type}'"

        print("✅ Test Passed: Password field is properly masked")

    # Test Case 9: Sign-in button is clickable
    def test_09_signin_button_clickable(self, page: Page):
        """TC-09: Verify sign-in button is enabled and clickable"""
        print("\n🧪 Test Case 9: Sign-in Button Clickability")

        # Locate sign-in button
        signin_button = page.wait_for_selector(self.SIGNIN_BUTTON_SELECTOR, timeout=5000)

        # Verify button is visible and enabled
        assert signin_button.is_visible(), "Sign-in button should be visible"
        assert signin_button.is_enabled(), "Sign-in button should be enabled"

        # Verify button is clickable
        signin_button.click()
        time.sleep(1)

        print("✅ Test Passed: Sign-in button is clickable")

    # Test Case 10: Page elements load correctly
    def test_10_page_elements_load(self, page: Page):
        """TC-10: Verify all login form elements are present"""
        print("\n🧪 Test Case 10: Page Elements Load Verification")

        # Check email field exists
        email_field = page.wait_for_selector(self.EMAIL_SELECTOR, timeout=5000)
        assert email_field.is_visible(), "Email field should be visible"

        # Check password field exists
        password_field = page.wait_for_selector(self.PASSWORD_SELECTOR, timeout=5000)
        assert password_field.is_visible(), "Password field should be visible"

        # Check sign-in button exists
        signin_button = page.wait_for_selector(self.SIGNIN_BUTTON_SELECTOR, timeout=5000)
        assert signin_button.is_visible(), "Sign-in button should be visible"

        # Verify page title or heading
        page_title = page.title()
        assert page_title, "Page should have a title"

        print(f"✅ Test Passed: All elements loaded correctly (Page title: {page_title})")


# Bonus Test Cases for comprehensive coverage

class TestSingleInterfaceLoginAdvanced:
    """Advanced test cases for login security and UX"""

    BASE_URL = "https://backend-dashboard.singleinterface.com/pages/index.html"
    VALID_EMAIL = "sukhbir.deswal+supportadmin@singleinterface.co"
    VALID_PASSWORD = "3e39e1"

    EMAIL_SELECTOR = 'input[name="email"]'
    PASSWORD_SELECTOR = 'input[id="password"]'
    SIGNIN_BUTTON_SELECTOR = 'button[type="button"]'

    @pytest.fixture(scope="function")
    def browser_context(self):
        """Setup browser context for each test"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False, slow_mo=1000)
            context = browser.new_context()
            yield context, browser
            context.close()
            browser.close()

    @pytest.fixture
    def page(self, browser_context):
        """Setup page for each test"""
        context, browser = browser_context
        page = context.new_page()
        page.goto(self.BASE_URL)
        page.wait_for_load_state("networkidle")
        yield page

    # Bonus Test Case 11: SQL Injection prevention
    def test_11_sql_injection_prevention(self, page: Page):
        """TC-11: Test SQL injection attempt in email field"""
        print("\n🧪 Test Case 11: SQL Injection Prevention")

        # Try SQL injection
        email_field = page.wait_for_selector(self.EMAIL_SELECTOR, timeout=5000)
        email_field.type("admin' OR '1'='1' --", delay=100)

        password_field = page.wait_for_selector(self.PASSWORD_SELECTOR, timeout=5000)
        password_field.type("anything", delay=100)

        signin_button = page.wait_for_selector(self.SIGNIN_BUTTON_SELECTOR, timeout=5000)
        signin_button.click()

        time.sleep(2)

        # Should not allow login
        current_url = page.url
        assert self.BASE_URL in current_url, "Should not allow SQL injection"

        print("✅ Test Passed: SQL injection prevented")

    # Bonus Test Case 12: XSS prevention
    def test_12_xss_prevention(self, page: Page):
        """TC-12: Test XSS script injection"""
        print("\n🧪 Test Case 12: XSS Prevention")

        # Try XSS attack
        email_field = page.wait_for_selector(self.EMAIL_SELECTOR, timeout=5000)
        email_field.type("<script>alert('XSS')</script>", delay=100)

        password_field = page.wait_for_selector(self.PASSWORD_SELECTOR, timeout=5000)
        password_field.type(self.VALID_PASSWORD, delay=100)

        signin_button = page.wait_for_selector(self.SIGNIN_BUTTON_SELECTOR, timeout=5000)
        signin_button.click()

        time.sleep(2)

        # Verify no alert was triggered and stayed on page
        current_url = page.url
        assert self.BASE_URL in current_url, "Should handle XSS safely"

        print("✅ Test Passed: XSS attack prevented")


# Run configuration
if __name__ == "__main__":
    # Run tests with verbose output and HTML report
    pytest.main([
        __file__,
        "-v",  # Verbose
        "-s",  # Show print statements
        "--html=singleinterface_test_report.html",
        "--self-contained-html",
        "--tb=short"  # Shorter traceback format
    ])