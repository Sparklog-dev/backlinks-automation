import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# BAI.tools - Y2Map submission mapping
# Filename: baitools_auto.py
#
# IMPORTANT:
# - XPath only for Selenium element selection
# - Does NOT click the final "Submit your AI Tool" button
# ============================================================


HOME_URL = "https://bai.tools/"

TOOL_NAME = "Y2Map"
WEBSITE_URL = "https://y2map.com"


def visible_element(driver, xpath, timeout=10):
    """Return the first visible element matching an XPath."""
    end_time = time.time() + timeout

    while time.time() < end_time:
        elements = driver.find_elements(By.XPATH, xpath)

        for element in elements:
            try:
                if element.is_displayed() and element.is_enabled():
                    return element
            except Exception:
                pass

        time.sleep(0.3)

    return None


def click_xpath(driver, xpath, description, timeout=10):
    """Click a visible element using XPath only."""
    element = visible_element(driver, xpath, timeout)

    if not element:
        raise Exception(f"Could not find clickable element: {description}")

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        element
    )

    time.sleep(0.5)

    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)

    print(f"✓ Clicked: {description}")
    return element


def fill_field(driver, xpath, value, description, timeout=10):
    """Fill an input using XPath only."""
    element = visible_element(driver, xpath, timeout)

    if not element:
        raise Exception(f"Could not find field: {description}")

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        element
    )

    time.sleep(0.3)

    element.click()
    element.send_keys(Keys.CONTROL, "a")
    element.send_keys(value)

    actual_value = element.get_attribute("value")

    if actual_value == value:
        print(f"✓ {description}: filled and verified")
    else:
        print(f"✗ {description}: verification failed")
        print(f"  Expected: {value}")
        print(f"  Actual:   {actual_value}")

    return element


# ============================================================
# Chrome setup
# ============================================================

options = uc.ChromeOptions()

options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

driver = uc.Chrome(
    version_main=152,
    options=options
)

# Prevent noisy undetected_chromedriver destructor error
try:
    uc.Chrome.__del__ = lambda self: None
except Exception:
    pass


wait = WebDriverWait(driver, 15)


try:

    # ========================================================
    # STEP 1 — Open homepage
    # ========================================================

    print("\nOpening BAI.tools homepage...")
    driver.get(HOME_URL)

    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//body")
        )
    )

    time.sleep(3)

    print(f"✓ Homepage opened")
    print(f"  URL: {driver.current_url}")
    print(f"  Title: {driver.title}")


    # ========================================================
    # STEP 2 — Click +Submit AI
    # ========================================================

    submit_link_xpath = (
        "//a["
        "contains(normalize-space(.), 'Submit AI')"
        "or "
        "contains(@href, '/submit-ai-tools')"
        "]"
    )

    click_xpath(
        driver,
        submit_link_xpath,
        "+Submit AI link"
    )

    time.sleep(3)

    print(f"✓ Submission page opened")
    print(f"  URL: {driver.current_url}")


    # ========================================================
    # STEP 3 — Confirm submission page
    # ========================================================

    page_text = driver.find_element(
        By.XPATH,
        "//body"
    ).text

    if "Submit AI Tools" in page_text:
        print("✓ Confirmed: Submit AI Tools page")

    if "FREE LISTING" in page_text:
        print("✓ FREE LISTING option detected")

    if "Submit without backlink for free" in page_text:
        print("✓ Free listing does NOT require backlink")

    if "$29.9" in page_text:
        print("✓ Paid Pro option detected — not selected")

    if "$19.9" in page_text:
        print("✓ Paid Standard option detected — not selected")


    # ========================================================
    # STEP 4 — Locate Tool Name field
    # ========================================================

    # First try semantic XPath.
    tool_name_xpath = (
        "//input["
        "contains(translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'tool name')"
        "or "
        "contains(translate(@name,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'tool')"
        "or "
        "contains(translate(@id,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'tool')"
        "]"
    )

    tool_name = visible_element(
        driver,
        tool_name_xpath,
        timeout=5
    )

    # Fallback: use the first visible non-hidden input.
    if not tool_name:
        print("⚠ Semantic Tool Name XPath did not match.")
        print("  Using first visible form input as fallback.")

        tool_name_xpath = (
            "(//input["
            "not(@type='hidden')"
            "and "
            "not(@disabled)"
            "and "
            "not(@readonly)"
            "])[1]"
        )

    fill_field(
        driver,
        tool_name_xpath,
        TOOL_NAME,
        "AI Tool Name"
    )


    # ========================================================
    # STEP 5 — Locate Website URL field
    # ========================================================

    website_xpath = (
        "//input["
        "@type='url'"
        "or "
        "contains(translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'website')"
        "or "
        "contains(translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'url')"
        "or "
        "contains(translate(@name,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'url')"
        "or "
        "contains(translate(@name,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'website')"
        "or "
        "contains(translate(@id,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'url')"
        "or "
        "contains(translate(@id,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
        "'website')"
        "]"
    )

    website_field = visible_element(
        driver,
        website_xpath,
        timeout=5
    )

    # Fallback: use the second visible non-hidden input.
    if not website_field:
        print("⚠ Semantic Website XPath did not match.")
        print("  Using second visible form input as fallback.")

        website_xpath = (
            "(//input["
            "not(@type='hidden')"
            "and "
            "not(@disabled)"
            "and "
            "not(@readonly)"
            "])[2]"
        )

    fill_field(
        driver,
        website_xpath,
        WEBSITE_URL,
        "Website URL"
    )


    # ========================================================
    # STEP 6 — Final verification
    # ========================================================

    print("\n" + "=" * 55)
    print("FINAL VERIFICATION")
    print("=" * 55)

    tool_name_value = visible_element(
        driver,
        tool_name_xpath
    ).get_attribute("value")

    website_value = visible_element(
        driver,
        website_xpath
    ).get_attribute("value")

    print(f"Tool Name : {tool_name_value}")
    print(f"Website   : {website_value}")

    if tool_name_value == TOOL_NAME:
        print("✓ Tool name PASS")
    else:
        print("✗ Tool name FAIL")

    if website_value == WEBSITE_URL:
        print("✓ Website URL PASS")
    else:
        print("✗ Website URL FAIL")


    # ========================================================
    # IMPORTANT — DO NOT SUBMIT
    # ========================================================

    final_button_xpath = (
        "//button["
        "normalize-space()='Submit your AI Tool'"
        "]"
    )

    final_button = visible_element(
        driver,
        final_button_xpath,
        timeout=5
    )

    if final_button:
        print("\n✓ Final 'Submit your AI Tool' button detected")
        print("✓ Final button was NOT clicked")
        print("✓ Safe stop — no submission performed")
    else:
        print("\n⚠ Final submission button was not detected")


    print("\n" + "=" * 55)
    print("BAI.tools mapping complete")
    print("Browser will remain open for manual inspection.")
    print("=" * 55)


    input("\nPress ENTER to close the browser...")


finally:

    try:
        driver.quit()
    except Exception:
        pass