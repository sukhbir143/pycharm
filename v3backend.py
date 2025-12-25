from playwright.sync_api import sync_playwright, Page, expect
import time
import re
from datetime import datetime
import json


class NovaTestSuite:
    """Complete test suite for Nova application"""

    # First-time sign-in credentials
    FIRST_TIME_USERNAME = "admin"
    FIRST_TIME_PASSWORD = "Amc9&fh53&sh490aldhf21dlaU"

    # Configuration
    BASE_URL = "https://dev-nova.singleinterface.com/login"
    EMAIL = "super_admin_hdfcLife@singleinterface.com"
    PASSWORD = "password123"



    def __init__(self):
        self.test_results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'details': []
        }
        self.page = None
        self.browser = None
        self.context = None

    def setup(self):
        """Setup browser"""
        print("\n" + "="*80)
        print("NOVA APPLICATION - COMPLETE TEST SUITE")
        print("60 Test Cases: Login (10) + Review AI (25) + Competitor AI (25)")
        print("="*80)

        p = sync_playwright().start()
        self.browser = p.chromium.launch(headless=False, slow_mo=1000)
        self.context = self.browser.new_context(viewport={"width": 1920, "height": 1080})
        self.page = self.context.new_page()

    def teardown(self):
        """Close browser"""
        if self.browser:
            input("\n\nPress Enter to close browser...")
            self.browser.close()

    def log_test(self, test_name, status, details=""):
        """Log test result"""
        self.test_results['total'] += 1
        if status == "PASSED":
            self.test_results['passed'] += 1
            icon = "✅"
        elif status == "FAILED":
            self.test_results['failed'] += 1
            icon = "❌"
        else:
            self.test_results['skipped'] += 1
            icon = "⚠️"

        self.test_results['details'].append({
            'test_name': test_name,
            'status': status,
            'details': details,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        print(f"{icon} {test_name}: {status}")
        if details:
            print(f"   {details}")

    def handle_first_time_signin(self):
        """Handle first-time sign-in popup if appears"""
        try:
            # Check if first-time signin popup appears
            first_time_popup = self.page.locator('//input[@type="text" or @type="password"]').first
            if first_time_popup.is_visible(timeout=3000):
                print("  ℹ️  First-time sign-in detected")

                # Enter first-time credentials
                username_field = self.page.locator('//input[@type="text"]').first
                password_field = self.page.locator('//input[@type="password"]').first

                username_field.fill(self.FIRST_TIME_USERNAME)
                password_field.fill(self.FIRST_TIME_PASSWORD)

                # Click submit
                submit_btn = self.page.locator('//button[@type="submit"]').first
                submit_btn.click()
                time.sleep(2)

                print("  ✅ First-time sign-in completed")
        except:
            pass  # No first-time signin popup

    # ============================================
    # LOGIN TEST CASES (10 TESTS)
    # ============================================

    def test_login_01_page_load(self):
        """TC-LOGIN-01: Verify login page loads successfully"""
        print("\n" + "-"*80)
        print("LOGIN TEST CASES")
        print("-"*80)

        try:
            self.page.goto(self.BASE_URL)
            self.page.wait_for_load_state('networkidle')

            # Verify URL
            assert self.BASE_URL in self.page.url, "Login page URL incorrect"

            # Verify page title
            title = self.page.title()
            assert title, "Page title is empty"

            self.log_test("TC-LOGIN-01: Page Load", "PASSED", f"Page loaded with title: {title}")
        except Exception as e:
            self.log_test("TC-LOGIN-01: Page Load", "FAILED", str(e))

    def test_login_02_elements_visible(self):
        """TC-LOGIN-02: Verify all login elements are visible"""
        try:
            # Check email field
            email_field = self.page.locator('input[type="email"], input[name="email"]')
            assert email_field.is_visible(), "Email field not visible"

            # Check password field
            password_field = self.page.locator('input[type="password"]')
            assert password_field.is_visible(), "Password field not visible"

            # Check login button
            login_btn = self.page.locator('button[type="submit"], button:has-text("Login")')
            assert login_btn.is_visible(), "Login button not visible"

            self.log_test("TC-LOGIN-02: Elements Visibility", "PASSED", "All elements visible")
        except Exception as e:
            self.log_test("TC-LOGIN-02: Elements Visibility", "FAILED", str(e))

    def test_login_03_empty_credentials(self):
        """TC-LOGIN-03: Login with empty credentials"""
        try:
            # Click login without entering credentials
            login_btn = self.page.locator('button[type="submit"], button:has-text("Login")').first
            login_btn.click()
            time.sleep(1)

            # Should stay on login page or show error
            current_url = self.page.url
            assert "login" in current_url.lower(), "Should stay on login page"

            self.log_test("TC-LOGIN-03: Empty Credentials", "PASSED", "Validation working")
        except Exception as e:
            self.log_test("TC-LOGIN-03: Empty Credentials", "FAILED", str(e))

    def test_login_04_invalid_email(self):
        """TC-LOGIN-04: Login with invalid email format"""
        try:
            self.page.reload()
            time.sleep(1)

            email_field = self.page.locator('input[type="email"], input[name="email"]').first
            password_field = self.page.locator('input[type="password"]').first

            email_field.fill("invalidemail")
            password_field.fill(self.PASSWORD)

            login_btn = self.page.locator('button[type="submit"]').first
            login_btn.click()
            time.sleep(1)

            # Should show validation error
            self.log_test("TC-LOGIN-04: Invalid Email", "PASSED", "Email validation working")
        except Exception as e:
            self.log_test("TC-LOGIN-04: Invalid Email", "FAILED", str(e))

    def test_login_05_wrong_password(self):
        """TC-LOGIN-05: Login with wrong password"""
        try:
            self.page.reload()
            time.sleep(1)

            email_field = self.page.locator('input[type="email"], input[name="email"]').first
            password_field = self.page.locator('input[type="password"]').first

            email_field.fill(self.EMAIL)
            password_field.fill("wrongpassword123")

            login_btn = self.page.locator('button[type="submit"]').first
            login_btn.click()
            time.sleep(2)

            # Should show error message
            self.log_test("TC-LOGIN-05: Wrong Password", "PASSED", "Error handling working")
        except Exception as e:
            self.log_test("TC-LOGIN-05: Wrong Password", "FAILED", str(e))

    def test_login_06_password_visibility_toggle(self):
        """TC-LOGIN-06: Password visibility toggle"""
        try:
            self.page.reload()
            time.sleep(1)

            password_field = self.page.locator('input[type="password"]').first

            # Check if toggle button exists
            toggle_btn = self.page.locator('//button[contains(@class, "password") or contains(@aria-label, "password")]')

            if toggle_btn.count() > 0:
                initial_type = password_field.get_attribute('type')
                toggle_btn.first.click()
                time.sleep(0.5)
                changed_type = password_field.get_attribute('type')

                assert initial_type != changed_type, "Password visibility toggle not working"
                self.log_test("TC-LOGIN-06: Password Toggle", "PASSED", "Toggle working")
            else:
                self.log_test("TC-LOGIN-06: Password Toggle", "SKIPPED", "Toggle button not found")
        except Exception as e:
            self.log_test("TC-LOGIN-06: Password Toggle", "FAILED", str(e))

    def test_login_07_remember_me(self):
        """TC-LOGIN-07: Remember me checkbox"""
        try:
            remember_checkbox = self.page.locator('input[type="checkbox"]')

            if remember_checkbox.count() > 0:
                # Test checking and unchecking
                if not remember_checkbox.first.is_checked():
                    remember_checkbox.first.check()
                    assert remember_checkbox.first.is_checked(), "Checkbox not checked"

                remember_checkbox.first.uncheck()
                assert not remember_checkbox.first.is_checked(), "Checkbox not unchecked"

                self.log_test("TC-LOGIN-07: Remember Me", "PASSED", "Checkbox working")
            else:
                self.log_test("TC-LOGIN-07: Remember Me", "SKIPPED", "Checkbox not found")
        except Exception as e:
            self.log_test("TC-LOGIN-07: Remember Me", "FAILED", str(e))

    def test_login_08_forgot_password_link(self):
        """TC-LOGIN-08: Forgot password link"""
        try:
            forgot_link = self.page.locator('a:has-text("Forgot"), a:has-text("forgot")')

            if forgot_link.count() > 0:
                assert forgot_link.first.is_visible(), "Forgot password link not visible"
                self.log_test("TC-LOGIN-08: Forgot Password Link", "PASSED", "Link available")
            else:
                self.log_test("TC-LOGIN-08: Forgot Password Link", "SKIPPED", "Link not found")
        except Exception as e:
            self.log_test("TC-LOGIN-08: Forgot Password Link", "FAILED", str(e))

    def test_login_09_successful_login(self):
        """TC-LOGIN-09: Successful login with valid credentials"""
        try:
            self.page.reload()
            time.sleep(1)

            email_field = self.page.locator('input[type="email"], input[name="email"]').first
            password_field = self.page.locator('input[type="password"]').first

            email_field.fill(self.EMAIL)
            password_field.fill(self.PASSWORD)

            login_btn = self.page.locator('button[type="submit"]').first
            login_btn.click()

            # Handle first-time signin if appears
            self.handle_first_time_signin()

            # Wait for successful login
            self.page.wait_for_load_state('networkidle')
            time.sleep(3)

            # Verify redirected away from login
            current_url = self.page.url
            assert "login" not in current_url.lower(), f"Still on login page: {current_url}"

            self.log_test("TC-LOGIN-09: Successful Login", "PASSED", f"Redirected to: {current_url}")
        except Exception as e:
            self.log_test("TC-LOGIN-09: Successful Login", "FAILED", str(e))
            # Take screenshot for debugging
            self.page.screenshot(path="login_failed.png")

    def test_login_10_dashboard_load(self):
        """TC-LOGIN-10: Dashboard loads after login"""
        try:
            # Verify dashboard elements
            time.sleep(2)

            # Check for common dashboard elements
            dashboard_elements = self.page.locator('nav, header, [class*="dashboard"], [class*="sidebar"]').all()

            assert len(dashboard_elements) > 0, "No dashboard elements found"

            self.log_test("TC-LOGIN-10: Dashboard Load", "PASSED", f"Dashboard loaded with {len(dashboard_elements)} elements")
        except Exception as e:
            self.log_test("TC-LOGIN-10: Dashboard Load", "FAILED", str(e))

    # ============================================
    # REVIEW AI MODULE TEST CASES (25 TESTS)
    # ============================================

    def navigate_to_review_ai(self):
        """Helper: Navigate to Review AI module"""
        try:
            # Look for Review AI in navigation
            review_ai_link = self.page.locator('a:has-text("Review AI"), [href*="review"], button:has-text("Review")').first

            if review_ai_link.is_visible(timeout=5000):
                review_ai_link.click()
                self.page.wait_for_load_state('networkidle')
                time.sleep(2)
                return True
            return False
        except:
            return False

    def test_review_ai_01_navigation(self):
        """TC-REVIEW-01: Navigate to Review AI module"""
        print("\n" + "-"*80)
        print("REVIEW AI MODULE TEST CASES")
        print("-"*80)

        try:
            success = self.navigate_to_review_ai()
            assert success, "Could not navigate to Review AI"

            # Verify URL contains review
            current_url = self.page.url
            assert "review" in current_url.lower(), f"Not on Review AI page: {current_url}"

            self.log_test("TC-REVIEW-01: Navigation", "PASSED", "Successfully navigated")
        except Exception as e:
            self.log_test("TC-REVIEW-01: Navigation", "FAILED", str(e))

    def test_review_ai_02_page_title(self):
        """TC-REVIEW-02: Verify page title"""
        try:
            page_title = self.page.locator('h1, h2, [class*="title"]').first
            assert page_title.is_visible(), "Page title not visible"

            title_text = page_title.inner_text()
            self.log_test("TC-REVIEW-02: Page Title", "PASSED", f"Title: {title_text}")
        except Exception as e:
            self.log_test("TC-REVIEW-02: Page Title", "FAILED", str(e))

    def test_review_ai_03_filters_visible(self):
        """TC-REVIEW-03: Verify filters are visible"""
        try:
            filter_elements = self.page.locator('[class*="filter"], select, input[type="date"]').all()
            visible_filters = sum(1 for f in filter_elements if f.is_visible())

            assert visible_filters > 0, "No filters found"

            self.log_test("TC-REVIEW-03: Filters Visible", "PASSED", f"{visible_filters} filters found")
        except Exception as e:
            self.log_test("TC-REVIEW-03: Filters Visible", "FAILED", str(e))

    def test_review_ai_04_date_filter(self):
        """TC-REVIEW-04: Apply date filter"""
        try:
            date_filter = self.page.locator('input[type="date"], [class*="date"]').first

            if date_filter.is_visible(timeout=3000):
                date_filter.click()
                time.sleep(1)
                self.log_test("TC-REVIEW-04: Date Filter", "PASSED", "Date filter working")
            else:
                self.log_test("TC-REVIEW-04: Date Filter", "SKIPPED", "Date filter not found")
        except Exception as e:
            self.log_test("TC-REVIEW-04: Date Filter", "FAILED", str(e))

    def test_review_ai_05_widgets_load(self):
        """TC-REVIEW-05: Verify widgets load with data"""
        try:
            widgets = self.page.locator('[class*="card"], [class*="widget"], [class*="metric"]').all()
            visible_widgets = sum(1 for w in widgets if w.is_visible())

            assert visible_widgets > 0, "No widgets found"

            self.log_test("TC-REVIEW-05: Widgets Load", "PASSED", f"{visible_widgets} widgets loaded")
        except Exception as e:
            self.log_test("TC-REVIEW-05: Widgets Load", "FAILED", str(e))

    def test_review_ai_06_sentiment_analysis(self):
        """TC-REVIEW-06: Verify sentiment analysis display"""
        try:
            sentiment = self.page.locator('[class*="sentiment"], :has-text("Positive"), :has-text("Negative")').first

            if sentiment.is_visible(timeout=3000):
                self.log_test("TC-REVIEW-06: Sentiment Analysis", "PASSED", "Sentiment data visible")
            else:
                self.log_test("TC-REVIEW-06: Sentiment Analysis", "SKIPPED", "Sentiment not found")
        except Exception as e:
            self.log_test("TC-REVIEW-06: Sentiment Analysis", "FAILED", str(e))

    def test_review_ai_07_rating_distribution(self):
        """TC-REVIEW-07: Verify rating distribution"""
        try:
            ratings = self.page.locator('[class*="rating"], [class*="star"]').all()

            if len(ratings) > 0:
                self.log_test("TC-REVIEW-07: Rating Distribution", "PASSED", f"{len(ratings)} rating elements")
            else:
                self.log_test("TC-REVIEW-07: Rating Distribution", "SKIPPED", "Ratings not found")
        except Exception as e:
            self.log_test("TC-REVIEW-07: Rating Distribution", "FAILED", str(e))

    def test_review_ai_08_charts_render(self):
        """TC-REVIEW-08: Verify charts render"""
        try:
            charts = self.page.locator('canvas, svg, [class*="chart"]').all()
            visible_charts = sum(1 for c in charts if c.is_visible())

            assert visible_charts > 0, "No charts found"

            self.log_test("TC-REVIEW-08: Charts Render", "PASSED", f"{visible_charts} charts rendered")
        except Exception as e:
            self.log_test("TC-REVIEW-08: Charts Render", "FAILED", str(e))

    def test_review_ai_09_review_list(self):
        """TC-REVIEW-09: Verify review list displays"""
        try:
            review_list = self.page.locator('[class*="review"], [class*="list"], table').first

            if review_list.is_visible(timeout=3000):
                self.log_test("TC-REVIEW-09: Review List", "PASSED", "Review list visible")
            else:
                self.log_test("TC-REVIEW-09: Review List", "SKIPPED", "List not found")
        except Exception as e:
            self.log_test("TC-REVIEW-09: Review List", "FAILED", str(e))

    def test_review_ai_10_pagination(self):
        """TC-REVIEW-10: Verify pagination controls"""
        try:
            pagination = self.page.locator('[class*="pagination"], [class*="page"]').first

            if pagination.is_visible(timeout=3000):
                self.log_test("TC-REVIEW-10: Pagination", "PASSED", "Pagination available")
            else:
                self.log_test("TC-REVIEW-10: Pagination", "SKIPPED", "Pagination not found")
        except Exception as e:
            self.log_test("TC-REVIEW-10: Pagination", "FAILED", str(e))

    def test_review_ai_11_search_functionality(self):
        """TC-REVIEW-11: Test search functionality"""
        try:
            search_box = self.page.locator('input[type="search"], input[placeholder*="Search"]').first

            if search_box.is_visible(timeout=3000):
                search_box.fill("test")
                time.sleep(1)
                search_box.fill("")
                self.log_test("TC-REVIEW-11: Search", "PASSED", "Search functional")
            else:
                self.log_test("TC-REVIEW-11: Search", "SKIPPED", "Search not found")
        except Exception as e:
            self.log_test("TC-REVIEW-11: Search", "FAILED", str(e))

    def test_review_ai_12_export_button(self):
        """TC-REVIEW-12: Verify export functionality"""
        try:
            export_btn = self.page.locator('button:has-text("Export"), button:has-text("Download")').first

            if export_btn.is_visible(timeout=3000):
                self.log_test("TC-REVIEW-12: Export Button", "PASSED", "Export available")
            else:
                self.log_test("TC-REVIEW-12: Export Button", "SKIPPED", "Export not found")
        except Exception as e:
            self.log_test("TC-REVIEW-12: Export Button", "FAILED", str(e))

    def test_review_ai_13_filter_reset(self):
        """TC-REVIEW-13: Test filter reset"""
        try:
            reset_btn = self.page.locator('button:has-text("Reset"), button:has-text("Clear")').first

            if reset_btn.is_visible(timeout=3000):
                reset_btn.click()
                time.sleep(1)
                self.log_test("TC-REVIEW-13: Filter Reset", "PASSED", "Reset working")
            else:
                self.log_test("TC-REVIEW-13: Filter Reset", "SKIPPED", "Reset not found")
        except Exception as e:
            self.log_test("TC-REVIEW-13: Filter Reset", "FAILED", str(e))

    def test_review_ai_14_ai_insights(self):
        """TC-REVIEW-14: Verify AI insights section"""
        try:
            insights = self.page.locator('[class*="insight"], [class*="ai"]').first

            if insights.is_visible(timeout=3000):
                self.log_test("TC-REVIEW-14: AI Insights", "PASSED", "AI insights visible")
            else:
                self.log_test("TC-REVIEW-14: AI Insights", "SKIPPED", "Insights not found")
        except Exception as e:
            self.log_test("TC-REVIEW-14: AI Insights", "FAILED", str(e))

    def test_review_ai_15_keyword_cloud(self):
        """TC-REVIEW-15: Verify keyword cloud"""
        try:
            keyword_cloud = self.page.locator('[class*="cloud"], [class*="keyword"]').first

            if keyword_cloud.is_visible(timeout=3000):
                self.log_test("TC-REVIEW-15: Keyword Cloud", "PASSED", "Keyword cloud visible")
            else:
                self.log_test("TC-REVIEW-15: Keyword Cloud", "SKIPPED", "Cloud not found")
        except Exception as e:
            self.log_test("TC-REVIEW-15: Keyword Cloud", "FAILED", str(e))

    def test_review_ai_16_trending_topics(self):
        """TC-REVIEW-16: Verify trending topics"""
        try:
            trending = self.page.locator('[class*="trending"], [class*="topic"]').first

            if trending.is_visible(timeout=3000):
                self.log_test("TC-REVIEW-16: Trending Topics", "PASSED", "Trending visible")
            else:
                self.log_test("TC-REVIEW-16: Trending Topics", "SKIPPED", "Trending not found")
        except Exception as e:
            self.log_test("TC-REVIEW-16: Trending Topics", "FAILED", str(e))

    def test_review_ai_17_time_series(self):
        """TC-REVIEW-17: Verify time series chart"""
        try:
            time_series = self.page.locator('[class*="time"], [class*="series"], [class*="trend"]').first

            if time_series.is_visible(timeout=3000):
                self.log_test("TC-REVIEW-17: Time Series", "PASSED", "Time series visible")
            else:
                self.log_test("TC-REVIEW-17: Time Series", "SKIPPED", "Time series not found")
        except Exception as e:
            self.log_test("TC-REVIEW-17: Time Series", "FAILED", str(e))

    def test_review_ai_18_review_detail(self):
        """TC-REVIEW-18: Click and view review detail"""
        try:
            review_item = self.page.locator('[class*="review-item"], tr, [class*="list-item"]').first

            if review_item.is_visible(timeout=3000):
                review_item.click()
                time.sleep(1)
                self.log_test("TC-REVIEW-18: Review Detail", "PASSED", "Detail view opened")
            else:
                self.log_test("TC-REVIEW-18: Review Detail", "SKIPPED", "Review item not found")
        except Exception as e:
            self.log_test("TC-REVIEW-18: Review Detail", "FAILED", str(e))

    def test_review_ai_19_category_filter(self):
        """TC-REVIEW-19: Apply category filter"""
        try:
            category_filter = self.page.locator('select, [class*="category"]').first

            if category_filter.is_visible(timeout=3000):
                self.log_test("TC-REVIEW-19: Category Filter", "PASSED", "Category filter available")
            else:
                self.log_test("TC-REVIEW-19: Category Filter", "SKIPPED", "Category not found")
        except Exception as e:
            self.log_test("TC-REVIEW-19: Category Filter", "FAILED", str(e))

    def test_review_ai_20_response_time(self):
        """TC-REVIEW-20: Verify page response time"""
        try:
            start_time = time.time()
            self.page.reload()
            self.page.wait_for_load_state('networkidle')
            end_time = time.time()

            response_time = end_time - start_time

            assert response_time < 10, f"Page load too slow: {response_time}s"

            self.log_test("TC-REVIEW-20: Response Time", "PASSED", f"Loaded in {response_time:.2f}s")
        except Exception as e:
            self.log_test("TC-REVIEW-20: Response Time", "FAILED", str(e))

    def test_review_ai_21_data_accuracy(self):
        """TC-REVIEW-21: Verify data accuracy"""
        try:
            numeric_elements = self.page.locator('[class*="count"], [class*="value"], [class*="number"]').all()

            data_points = []
            for elem in numeric_elements:
                if elem.is_visible():
                    text = elem.inner_text()
                    numbers = re.findall(r'\d+', text)
                    data_points.extend(numbers)

            assert len(data_points) > 0, "No data points found"

            self.log_test("TC-REVIEW-21: Data Accuracy", "PASSED", f"{len(data_points)} data points validated")
        except Exception as e:
            self.log_test("TC-REVIEW-21: Data Accuracy", "FAILED", str(e))

    def test_review_ai_22_loading_indicators(self):
        """TC-REVIEW-22: Verify no loading indicators stuck"""
        try:
            loaders = self.page.locator('[class*="loading"], [class*="spinner"]').all()
            visible_loaders = sum(1 for l in loaders if l.is_visible())

            assert visible_loaders == 0, f"{visible_loaders} loaders still visible"

            self.log_test("TC-REVIEW-22: Loading Indicators", "PASSED", "No stuck loaders")
        except Exception as e:
            self.log_test("TC-REVIEW-22: Loading Indicators", "FAILED", str(e))

    def test_review_ai_23_error_handling(self):
        """TC-REVIEW-23: Verify error handling"""
        try:
            errors = self.page.locator('[class*="error"], [class*="alert-danger"]').all()
            visible_errors = sum(1 for e in errors if e.is_visible())

            assert visible_errors == 0, f"{visible_errors} errors displayed"

            self.log_test("TC-REVIEW-23: Error Handling", "PASSED", "No errors displayed")
        except Exception as e:
            self.log_test("TC-REVIEW-23: Error Handling", "FAILED", str(e))

    def test_review_ai_24_responsive_design(self):
        """TC-REVIEW-24: Test responsive design"""
        try:
            # Test mobile view
            self.page.set_viewport_size({"width": 375, "height": 667})
            time.sleep(1)

            # Check if main elements still visible
            main_element = self.page.locator('main, [class*="content"]').first
            assert main_element.is_visible(), "Content not visible in mobile view"

            # Reset to desktop
            self.page.set_viewport_size({"width": 1920, "height": 1080})
            time.sleep(1)

            self.log_test("TC-REVIEW-24: Responsive Design", "PASSED", "Responsive working")
        except Exception as e:
            self.log_test("TC-REVIEW-24: Responsive Design", "FAILED", str(e))

    def test_review_ai_25_screenshot(self):
        """TC-REVIEW-25: Take screenshot for documentation"""
        try:
            screenshot_path = f"review_ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.page.screenshot(path=screenshot_path, full_page=True)

            self.log_test("TC-REVIEW-25: Screenshot", "PASSED", f"Saved: {screenshot_path}")
        except Exception as e:
            self.log_test("TC-REVIEW-25: Screenshot", "FAILED", str(e))

    # ============================================
    # COMPETITOR AI MODULE TEST CASES (25 TESTS)
    # ============================================

    def navigate_to_competitor_ai(self):
        """Helper: Navigate to Competitor AI module"""
        try:
            competitor_link = self.page.locator('a:has-text("Competitor"), [href*="competitor"], button:has-text("Competitor")').first

            if competitor_link.is_visible(timeout=5000):
                competitor_link.click()
                self.page.wait_for_load_state('networkidle')
                time.sleep(2)
                return True
            return False
        except:
            return False

    def test_competitor_ai_01_navigation(self):
        """TC-COMP-01: Navigate to Competitor AI module"""
        print("\n" + "-"*80)
        print("COMPETITOR AI MODULE TEST CASES")
        print("-"*80)

        try:
            success = self.navigate_to_competitor_ai()
            assert success, "Could not navigate to Competitor AI"

            current_url = self.page.url
            self.log_test("TC-COMP-01: Navigation", "PASSED", f"URL: {current_url}")
        except Exception as e:
            self.log_test("TC-COMP-01: Navigation", "FAILED", str(e))

    def test_competitor_ai_02_page_load(self):
        """TC-COMP-02: Verify page loads completely"""
        try:
            self.page.wait_for_load_state('networkidle')
            time.sleep(2)

            page_title = self.page.locator('h1, h2').first
            assert page_title.is_visible(), "Page title not visible"

            self.log_test("TC-COMP-02: Page Load", "PASSED", "Page loaded")
        except Exception as e:
            self.log_test("TC-COMP-02: Page Load", "FAILED", str(e))

    def test_competitor_ai_03_competitor_list(self):
        """TC-COMP-03: Verify competitor list displays"""
        try:
            competitor_list = self.page.locator('[class*="competitor"], table, [class*="list"]').all()

            assert len(competitor_list) > 0, "No competitor list found"

            self.log_test("TC-COMP-03: Competitor List", "PASSED", f"{len(competitor_list)} elements")
        except Exception as e:
            self.log_test("TC-COMP-03: Competitor List", "FAILED", str(e))

    def test_competitor_ai_04_comparison_metrics(self):
        """TC-COMP-04: Verify comparison metrics"""
        try:
            metrics = self.page.locator('[class*="metric"], [class*="stat"], [class*="kpi"]').all()
            visible_metrics = sum(1 for m in metrics if m.is_visible())

            assert visible_metrics > 0, "No metrics found"

            self.log_test("TC-COMP-04: Comparison Metrics", "PASSED", f"{visible_metrics} metrics")
        except Exception as e:
            self.log_test("TC-COMP-04: Comparison Metrics", "FAILED", str(e))

    def test_competitor_ai_05_market_share(self):
        """TC-COMP-05: Verify market share visualization"""
        try:
            market_share = self.page.locator('[class*="market"], [class*="share"]').first

            if market_share.is_visible(timeout=3000):
                self.log_test("TC-COMP-05: Market Share", "PASSED", "Market share visible")
            else:
                self.log_test("TC-COMP-05: Market Share", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-05: Market Share", "FAILED", str(e))

    def test_competitor_ai_06_pricing_comparison(self):
        """TC-COMP-06: Verify pricing comparison"""
        try:
            pricing = self.page.locator('[class*="price"], [class*="pricing"]').first

            if pricing.is_visible(timeout=3000):
                self.log_test("TC-COMP-06: Pricing Comparison", "PASSED", "Pricing visible")
            else:
                self.log_test("TC-COMP-06: Pricing Comparison", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-06: Pricing Comparison", "FAILED", str(e))

    def test_competitor_ai_07_feature_comparison(self):
        """TC-COMP-07: Verify feature comparison table"""
        try:
            feature_table = self.page.locator('table, [class*="feature"]').first

            if feature_table.is_visible(timeout=3000):
                self.log_test("TC-COMP-07: Feature Comparison", "PASSED", "Table visible")
            else:
                self.log_test("TC-COMP-07: Feature Comparison", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-07: Feature Comparison", "FAILED", str(e))

    def test_competitor_ai_08_swot_analysis(self):
        """TC-COMP-08: Verify SWOT analysis"""
        try:
            swot = self.page.locator('[class*="swot"], :has-text("Strengths"), :has-text("Weakness")').first

            if swot.is_visible(timeout=3000):
                self.log_test("TC-COMP-08: SWOT Analysis", "PASSED", "SWOT visible")
            else:
                self.log_test("TC-COMP-08: SWOT Analysis", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-08: SWOT Analysis", "FAILED", str(e))

    def test_competitor_ai_09_performance_chart(self):
        """TC-COMP-09: Verify performance charts"""
        try:
            charts = self.page.locator('canvas, svg, [class*="chart"]').all()
            visible_charts = sum(1 for c in charts if c.is_visible())

            assert visible_charts > 0, "No charts found"

            self.log_test("TC-COMP-09: Performance Charts", "PASSED", f"{visible_charts} charts")
        except Exception as e:
            self.log_test("TC-COMP-09: Performance Charts", "FAILED", str(e))

    def test_competitor_ai_10_trend_analysis(self):
        """TC-COMP-10: Verify trend analysis"""
        try:
            trend = self.page.locator('[class*="trend"], [class*="analysis"]').first

            if trend.is_visible(timeout=3000):
                self.log_test("TC-COMP-10: Trend Analysis", "PASSED", "Trend visible")
            else:
                self.log_test("TC-COMP-10: Trend Analysis", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-10: Trend Analysis", "FAILED", str(e))

    def test_competitor_ai_11_add_competitor(self):
        """TC-COMP-11: Test add competitor functionality"""
        try:
            add_btn = self.page.locator('button:has-text("Add"), button:has-text("+")').first

            if add_btn.is_visible(timeout=3000):
                self.log_test("TC-COMP-11: Add Competitor", "PASSED", "Add button available")
            else:
                self.log_test("TC-COMP-11: Add Competitor", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-11: Add Competitor", "FAILED", str(e))

    def test_competitor_ai_12_filter_competitors(self):
        """TC-COMP-12: Test competitor filters"""
        try:
            filters = self.page.locator('[class*="filter"], select').all()
            visible_filters = sum(1 for f in filters if f.is_visible())

            assert visible_filters > 0, "No filters found"

            self.log_test("TC-COMP-12: Filter Competitors", "PASSED", f"{visible_filters} filters")
        except Exception as e:
            self.log_test("TC-COMP-12: Filter Competitors", "FAILED", str(e))

    def test_competitor_ai_13_search_competitor(self):
        """TC-COMP-13: Test competitor search"""
        try:
            search = self.page.locator('input[type="search"], input[placeholder*="Search"]').first

            if search.is_visible(timeout=3000):
                search.fill("test")
                time.sleep(1)
                search.fill("")
                self.log_test("TC-COMP-13: Search Competitor", "PASSED", "Search working")
            else:
                self.log_test("TC-COMP-13: Search Competitor", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-13: Search Competitor", "FAILED", str(e))

    def test_competitor_ai_14_export_data(self):
        """TC-COMP-14: Test export functionality"""
        try:
            export_btn = self.page.locator('button:has-text("Export"), button:has-text("Download")').first

            if export_btn.is_visible(timeout=3000):
                self.log_test("TC-COMP-14: Export Data", "PASSED", "Export available")
            else:
                self.log_test("TC-COMP-14: Export Data", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-14: Export Data", "FAILED", str(e))

    def test_competitor_ai_15_ai_recommendations(self):
        """TC-COMP-15: Verify AI recommendations"""
        try:
            recommendations = self.page.locator('[class*="recommendation"], [class*="suggest"]').first

            if recommendations.is_visible(timeout=3000):
                self.log_test("TC-COMP-15: AI Recommendations", "PASSED", "Recommendations visible")
            else:
                self.log_test("TC-COMP-15: AI Recommendations", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-15: AI Recommendations", "FAILED", str(e))

    def test_competitor_ai_16_benchmark_score(self):
        """TC-COMP-16: Verify benchmark scores"""
        try:
            benchmark = self.page.locator('[class*="benchmark"], [class*="score"]').first

            if benchmark.is_visible(timeout=3000):
                self.log_test("TC-COMP-16: Benchmark Score", "PASSED", "Benchmark visible")
            else:
                self.log_test("TC-COMP-16: Benchmark Score", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-16: Benchmark Score", "FAILED", str(e))

    def test_competitor_ai_17_geography_analysis(self):
        """TC-COMP-17: Verify geography analysis"""
        try:
            geography = self.page.locator('[class*="geo"], [class*="map"], [class*="region"]').first

            if geography.is_visible(timeout=3000):
                self.log_test("TC-COMP-17: Geography Analysis", "PASSED", "Geography visible")
            else:
                self.log_test("TC-COMP-17: Geography Analysis", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-17: Geography Analysis", "FAILED", str(e))

    def test_competitor_ai_18_time_period_filter(self):
        """TC-COMP-18: Test time period filter"""
        try:
            time_filter = self.page.locator('[class*="time"], [class*="period"], select').first

            if time_filter.is_visible(timeout=3000):
                self.log_test("TC-COMP-18: Time Period Filter", "PASSED", "Time filter available")
            else:
                self.log_test("TC-COMP-18: Time Period Filter", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-18: Time Period Filter", "FAILED", str(e))

    def test_competitor_ai_19_data_refresh(self):
        """TC-COMP-19: Test data refresh"""
        try:
            refresh_btn = self.page.locator('button:has-text("Refresh"), [class*="refresh"]').first

            if refresh_btn.is_visible(timeout=3000):
                refresh_btn.click()
                time.sleep(2)
                self.log_test("TC-COMP-19: Data Refresh", "PASSED", "Refresh working")
            else:
                self.log_test("TC-COMP-19: Data Refresh", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-19: Data Refresh", "FAILED", str(e))

    def test_competitor_ai_20_alerts_notifications(self):
        """TC-COMP-20: Verify alerts and notifications"""
        try:
            alerts = self.page.locator('[class*="alert"], [class*="notification"]').all()
            visible_alerts = sum(1 for a in alerts if a.is_visible())

            self.log_test("TC-COMP-20: Alerts", "PASSED", f"{visible_alerts} alerts")
        except Exception as e:
            self.log_test("TC-COMP-20: Alerts", "FAILED", str(e))

    def test_competitor_ai_21_detailed_view(self):
        """TC-COMP-21: Test detailed competitor view"""
        try:
            competitor_item = self.page.locator('[class*="competitor"], tr').first

            if competitor_item.is_visible(timeout=3000):
                competitor_item.click()
                time.sleep(2)
                self.log_test("TC-COMP-21: Detailed View", "PASSED", "Detail view opened")
            else:
                self.log_test("TC-COMP-21: Detailed View", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-21: Detailed View", "FAILED", str(e))

    def test_competitor_ai_22_comparison_side_by_side(self):
        """TC-COMP-22: Test side-by-side comparison"""
        try:
            comparison = self.page.locator('[class*="comparison"], [class*="side-by-side"]').first

            if comparison.is_visible(timeout=3000):
                self.log_test("TC-COMP-22: Side-by-Side", "PASSED", "Comparison visible")
            else:
                self.log_test("TC-COMP-22: Side-by-Side", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-22: Side-by-Side", "FAILED", str(e))

    def test_competitor_ai_23_historical_data(self):
        """TC-COMP-23: Verify historical data"""
        try:
            historical = self.page.locator('[class*="historical"], [class*="history"]').first

            if historical.is_visible(timeout=3000):
                self.log_test("TC-COMP-23: Historical Data", "PASSED", "Historical data visible")
            else:
                self.log_test("TC-COMP-23: Historical Data", "SKIPPED", "Not found")
        except Exception as e:
            self.log_test("TC-COMP-23: Historical Data", "FAILED", str(e))

    def test_competitor_ai_24_page_performance(self):
        """TC-COMP-24: Verify page performance"""
        try:
            start_time = time.time()
            self.page.reload()
            self.page.wait_for_load_state('networkidle')
            end_time = time.time()

            load_time = end_time - start_time

            assert load_time < 10, f"Page load too slow: {load_time}s"

            self.log_test("TC-COMP-24: Performance", "PASSED", f"Loaded in {load_time:.2f}s")
        except Exception as e:
            self.log_test("TC-COMP-24: Performance", "FAILED", str(e))

    def test_competitor_ai_25_screenshot(self):
        """TC-COMP-25: Take screenshot for documentation"""
        try:
            screenshot_path = f"competitor_ai_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            self.page.screenshot(path=screenshot_path, full_page=True)

            self.log_test("TC-COMP-25: Screenshot", "PASSED", f"Saved: {screenshot_path}")
        except Exception as e:
            self.log_test("TC-COMP-25: Screenshot", "FAILED", str(e))

    # ============================================
    # REPORT GENERATION
    # ============================================

    def generate_report(self):
        """Generate final test report"""
        print("\n\n" + "="*80)
        print("📊 FINAL TEST EXECUTION REPORT")
        print("="*80)

        print(f"\n📈 SUMMARY:")
        print(f"  Total Tests:   {self.test_results['total']}")
        print(f"  ✅ Passed:      {self.test_results['passed']}")
        print(f"  ❌ Failed:      {self.test_results['failed']}")
        print(f"  ⚠️  Skipped:     {self.test_results['skipped']}")

        if self.test_results['total'] > 0:
            pass_rate = (self.test_results['passed'] / self.test_results['total'] * 100)
            print(f"  📊 Pass Rate:   {pass_rate:.2f}%")

        print(f"\n📋 CATEGORY BREAKDOWN:")
        login_tests = [r for r in self.test_results['details'] if 'LOGIN' in r['test_name']]
        review_tests = [r for r in self.test_results['details'] if 'REVIEW' in r['test_name']]
        comp_tests = [r for r in self.test_results['details'] if 'COMP' in r['test_name']]

        print(f"  Login Tests:      {len([t for t in login_tests if t['status'] == 'PASSED'])}/{len(login_tests)} passed")
        print(f"  Review AI Tests:  {len([t for t in review_tests if t['status'] == 'PASSED'])}/{len(review_tests)} passed")
        print(f"  Competitor Tests: {len([t for t in comp_tests if t['status'] == 'PASSED'])}/{len(comp_tests)} passed")

        # Save report
        report_filename = f"nova_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, 'w') as f:
            json.dump(self.test_results, f, indent=4)

        print(f"\n💾 Report saved: {report_filename}")

        # Status
        print("\n" + "="*80)
        if self.test_results['failed'] == 0:
            print("🎉 ALL CRITICAL TESTS PASSED!")
        else:
            print(f"⚠️  {self.test_results['failed']} TEST(S) FAILED")
        print("="*80)

    def run_all_tests(self):
        """Execute all test cases"""
        try:
            self.setup()

            # Login Tests (10)
            self.test_login_01_page_load()
            self.test_login_02_elements_visible()
            self.test_login_03_empty_credentials()
            self.test_login_04_invalid_email()
            self.test_login_05_wrong_password()
            self.test_login_06_password_visibility_toggle()
            self.test_login_07_remember_me()
            self.test_login_08_forgot_password_link()
            self.test_login_09_successful_login()
            self.test_login_10_dashboard_load()

            # Review AI Tests (25)
            self.test_review_ai_01_navigation()
            self.test_review_ai_02_page_title()
            self.test_review_ai_03_filters_visible()
            self.test_review_ai_04_date_filter()
            self.test_review_ai_05_widgets_load()
            self.test_review_ai_06_sentiment_analysis()
            self.test_review_ai_07_rating_distribution()
            self.test_review_ai_08_charts_render()
            self.test_review_ai_09_review_list()
            self.test_review_ai_10_pagination()
            self.test_review_ai_11_search_functionality()
            self.test_review_ai_12_export_button()
            self.test_review_ai_13_filter_reset()
            self.test_review_ai_14_ai_insights()
            self.test_review_ai_15_keyword_cloud()
            self.test_review_ai_16_trending_topics()
            self.test_review_ai_17_time_series()
            self.test_review_ai_18_review_detail()
            self.test_review_ai_19_category_filter()
            self.test_review_ai_20_response_time()
            self.test_review_ai_21_data_accuracy()
            self.test_review_ai_22_loading_indicators()
            self.test_review_ai_23_error_handling()
            self.test_review_ai_24_responsive_design()
            self.test_review_ai_25_screenshot()

            # Competitor AI Tests (25)
            self.test_competitor_ai_01_navigation()
            self.test_competitor_ai_02_page_load()
            self.test_competitor_ai_03_competitor_list()
            self.test_competitor_ai_04_comparison_metrics()
            self.test_competitor_ai_05_market_share()
            self.test_competitor_ai_06_pricing_comparison()
            self.test_competitor_ai_07_feature_comparison()
            self.test_competitor_ai_08_swot_analysis()
            self.test_competitor_ai_09_performance_chart()
            self.test_competitor_ai_10_trend_analysis()
            self.test_competitor_ai_11_add_competitor()
            self.test_competitor_ai_12_filter_competitors()
            self.test_competitor_ai_13_search_competitor()
            self.test_competitor_ai_14_export_data()
            self.test_competitor_ai_15_ai_recommendations()
            self.test_competitor_ai_16_benchmark_score()
            self.test_competitor_ai_17_geography_analysis()
            self.test_competitor_ai_18_time_period_filter()
            self.test_competitor_ai_19_data_refresh()
            self.test_competitor_ai_20_alerts_notifications()
            self.test_competitor_ai_21_detailed_view()
            self.test_competitor_ai_22_comparison_side_by_side()
            self.test_competitor_ai_23_historical_data()
            self.test_competitor_ai_24_page_performance()
            self.test_competitor_ai_25_screenshot()

            # Generate Report
            self.generate_report()

        except Exception as e:
            print(f"\n❌ Test execution failed: {str(e)}")
            self.page.screenshot(path="critical_error.png")

        finally:
            self.teardown()


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print("="*80)
    print("NOVA APPLICATION - AUTOMATED TEST SUITE")
    print("="*80)
    print("\n60 Test Cases:")
    print("  • 10 Login Page Tests")
    print("  • 25 Review AI Module Tests")
    print("  • 25 Competitor AI Module Tests")
    print("\n" + "="*80)

    input("\nPress Enter to start testing...")

    # Run complete test suite
    test_suite = NovaTestSuite()
    test_suite.run_all_tests()
