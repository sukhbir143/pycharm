from playwright.sync_api import sync_playwright
import time

with (sync_playwright() as p):
    browser = p.chromium.launch(headless=False, slow_mo=2000)
    page = browser.new_page()
    # ====================
    # STEP 1: LOGIN
    # ====================
    page.goto('https://dev-backend-dashboard.singleinterface.com/pages/index.html')
    emailid  = page.wait_for_selector('#email')
    emailid.type('sukhbir.deswal+supportadmin@singleinterface.com')
    Password = page.wait_for_selector("#password")
    Password.type("3e39e1")
    signin = page.wait_for_selector('#loginBtn')
    signin.click()
    # ====================
    # STEP 2: SELECT CLIENT
    # ====================
    searchbox = page.wait_for_selector('#clientSerch')
    searchbox.type('sangeet')
    clientlink = page.wait_for_selector('a[class="client_link"]')
    clientlink.click()
    # ====================
    # STEP 3: NAVIGATE TO REVIEW INSIGHTS
    # ====================
    insight = page.wait_for_selector("//img[@src='../assets/img/ic-insight.svg']")
    insight.click()
    review = page.wait_for_selector('a:has-text("reviewsReview Insights")')
    review.click()
    # ====================
    # STEP 4: APPLY FILTER
    # ====================
    Filter = page.wait_for_selector("//span[@class='Alt-din-font filter-class-btn']")
    Filter.click()
    radio_button = page.query_selector('//input[@value="last_week"]')
    radio_button.click()
    Apply = page.wait_for_selector("//button[@class='btn btn-apply changeable-button apply_global_filter']")
    Apply.click()

    Filter = page.wait_for_selector("//span[@class='Alt-din-font filter-class-btn']")
    Filter.click()
    financialyear = page.wait_for_selector('//input[@value="last_financial_year"]')
    financialyear.click()
    Apply = page.wait_for_selector("//button[@class='btn btn-apply changeable-button apply_global_filter']")
    Apply.click()

    Filter = page.wait_for_selector("//span[@class='Alt-din-font filter-class-btn']")
    Filter.click()

    print("\n✅ Script completed! Browser will remain open.")
    print("Press Ctrl+C in terminal to close the browser.")

    input("Or press Enter here to close...")

    # ====================
    # STEP 5: VERIFY WIDGETS
    # ====================
    print("\n" + "=" * 60)
    print("🔍 WIDGET DATA VERIFICATION")
    print("=" * 60)

    # Common widget selectors to check
    widget_selectors = {
        # Common patterns for widgets
        'cards': [
            '.card',
            '.widget',
            '.dashboard-card',
            '[class*="widget"]',
            '[class*="card"]',
        ],
        'numbers': [
            '[class*="count"]',
            '[class*="value"]',
            '[class*="number"]',
            '.metric',
            '.stat-value',
        ],
        'charts': [
            'canvas',
            'svg',
            '[class*="chart"]',
        ],
    }

    # ====================
    # TEST 1: Check if widgets are visible
    # ====================
    print("\n📋 Test 1: Checking widget visibility...")

    # Find all card/widget containers
    widget_containers = page.locator('.card, .widget, [class*="widget"], [class*="card"]').all()

    if len(widget_containers) > 0:
        print(f"✅ Found {len(widget_containers)} widget containers")
        ['passed'].append(f"Widget visibility: {len(widget_containers)} widgets found")
    else:
        print("❌ No widget containers found!")
        ['failed'].append("Widget visibility: No widgets found")

        # ====================
        # TEST 2: Verify data in numeric widgets
        # ====================
        print("\n🔢 Test 2: Verifying numeric data...")

        # Look for elements with numbers
        numeric_elements = page.locator(
            '[class*="count"], [class*="value"], [class*="number"], .metric, .stat-value').all()

        empty_widgets = 0
        widgets_with_data = 0

        for i, element in enumerate(numeric_elements):
            try:
                text = element.inner_text().strip()

                # Check if element has numeric data
                if text and text != '0' and text != '-' and text != 'N/A':
                    # Check if it contains any digit
                    if re.search(r'\d', text):
                        widgets_with_data += 1
                        print(f"  ✅ Widget {i + 1}: {text}")
                    else:
                        print(f"  ⚠️  Widget {i + 1}: {text} (no numeric data)")
                else:
                    empty_widgets += 1
                    print(f"  ❌ Widget {i + 1}: Empty or zero value")
            except:
                print(f"  ⚠️  Widget {i + 1}: Could not read data")

        if widgets_with_data > 0:
            ['passed'].append(f"Numeric data: {widgets_with_data} widgets have data")
        if empty_widgets > 0:
            ['warnings'].append(f"Numeric data: {empty_widgets} widgets are empty")

            # ====================
            # TEST 3: Verify charts are rendered
            # ====================
            print("\n📊 Test 3: Verifying charts...")

            charts = page.locator('canvas, svg, [class*="chart"]').all()

            if len(charts) > 0:
                print(f"✅ Found {len(charts)} chart elements")
                ['passed'].append(f"Charts: {len(charts)} charts found")

                # Check if charts have data
                for i, chart in enumerate(charts):
                    try:
                        # For canvas elements
                        if chart.evaluate('el => el.tagName') == 'CANVAS':
                            # Check if canvas is not empty
                            is_empty = chart.evaluate('''(canvas) => {
                                           const ctx = canvas.getContext('2d');
                                           const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                                           return !imageData.data.some(channel => channel !== 0);
                                       }''')
                            if not is_empty:
                                print(f"  ✅ Chart {i + 1}: Has rendered data")
                            else:
                                print(f"  ⚠️  Chart {i + 1}: Appears empty")
                    except:
                        print(f"  ⚠️  Chart {i + 1}: Could not verify")
            else:
                print("⚠️  No charts found")
                ['warnings'].append("Charts: No chart elements found")
                # ====================
                # TEST 4: Check for loading indicators (should be gone)
                # ====================
                print("\n⏳ Test 4: Checking for loading indicators...")

                loading_indicators = page.locator('[class*="loading"], [class*="spinner"], .loader').all()

                if len(loading_indicators) == 0:
                    print("✅ No loading indicators present (data loaded)")
                    ['passed'].append("Loading state: Data fully loaded")
                else:
                    visible_loaders = sum(1 for loader in loading_indicators if loader.is_visible())
                    if visible_loaders > 0:
                        print(f"⚠️  {visible_loaders} loading indicators still visible")
                        ['warnings'].append(f"Loading state: {visible_loaders} loaders still visible")
                    else:
                        print("✅ Loading indicators hidden")
                        ['passed'].append("Loading state: Data fully loaded")

                        # ====================
                        # TEST 5: Check for error messages
                        # ====================
                        print("\n❌ Test 5: Checking for error messages...")

                        error_selectors = [
                            '[class*="error"]',
                            '[class*="alert-danger"]',
                            '.error-message',
                            '[class*="no-data"]',
                        ]

                        errors_found = False
                        for selector in error_selectors:
                            error_elements = page.locator(selector).all()
                            visible_errors = [e for e in error_elements if e.is_visible()]

                            if visible_errors:
                                errors_found = True
                                for error in visible_errors:
                                    error_text = error.inner_text()
                                    print(f"  ❌ Error found: {error_text}")
                                    ['failed'].append(f"Error message: {error_text}")

                        if not errors_found:
                            print("✅ No error messages found")
                            ['passed'].append("Error check: No errors displayed")

                        # ====================
                        # TEST 6: Verify specific widget types
                        # ====================
                        print("\n📈 Test 6: Verifying specific widget types...")

                        # Check for common review dashboard widgets
                        widget_checks = {
                            "Total Reviews": '//div[contains(text(), "Total") or contains(text(), "total")]',
                            "Average Rating": '//div[contains(text(), "Rating") or contains(text(), "rating")]',
                            "Review Trend": '//div[contains(text(), "Trend") or contains(text(), "trend")]',
                            "Sentiment": '//div[contains(text(), "Sentiment") or contains(text(), "sentiment")]',
                        }

                        for widget_name, selector in widget_checks.items():
                            try:
                                element = page.locator(selector).first
                                if element.is_visible():
                                    parent = element.locator(
                                        'xpath=ancestor::div[contains(@class, "card") or contains(@class, "widget")]').first
                                    widget_text = parent.inner_text()

                                    # Check if has numeric data
                                    has_data = bool(re.search(r'\d', widget_text))
                                    if has_data:
                                        print(f"  ✅ {widget_name}: Data present")
                                        ['passed'].append(f"{widget_name}: Has data")
                                    else:
                                        print(f"  ⚠️  {widget_name}: No numeric data")
                                        ['warnings'].append(f"{widget_name}: No data")
                            except:
                                print(f"  ⚠️  {widget_name}: Not found or not accessible")

                        # ====================
                        # TEST 7: Verify filter is applied (check UI)
                        # ====================
                        print("\n✓ Test 7: Verifying filter application...")

                        try:
                            # Check if the filter button shows the selected filter
                            filter_button = page.locator("//span[@class='Alt-din-font filter-class-btn']")
                            filter_text = filter_button.inner_text()

                            if 'last week' in filter_text.lower() or 'week' in filter_text.lower():
                                print(f"✅ Filter applied: {filter_text}")
                                ['passed'].append(f"Filter state: {filter_text}")
                            else:
                                print(f"⚠️  Filter text: {filter_text}")
                                ['warnings'].append(f"Filter state unclear: {filter_text}")
                        except:
                            print("⚠️  Could not verify filter state")


                            class Car:
                                def __int__(self, brand ,model):
                                    self.brand = brand
                                    self.model = model























