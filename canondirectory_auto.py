import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# CANON DIRECTORY — Y2Map submission mapping
# ============================================================

HOMEPAGE = "https://canondirectory.com/"
SUBMIT_URL = "https://canondirectory.com/register.html"

PRODUCT_NAME = "Y2Map"
WEBSITE_URL = "https://y2map.com"
EMAIL = "sparklog.marketing@gmail.com"

DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that transforms "
    "YouTube videos, PDFs, books, and research content into easy-to-understand "
    "visual mind maps. It helps users understand complex topics faster by "
    "organizing important ideas, concepts, summaries, references, and related "
    "information into a structured visual format."
)


# ============================================================
# Helpers
# ============================================================

def wait_for_element(driver, xpath, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def click_xpath(driver, xpath, timeout=20):
    element = wait_for_element(driver, xpath, timeout)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )

    time.sleep(1)

    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        ).click()
    except Exception:
        driver.execute_script(
            "arguments[0].click();",
            element
        )

    return element


def fill_field(driver, xpath, value, field_name):
    element = wait_for_element(driver, xpath)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )

    time.sleep(0.5)

    element.click()
    element.clear()
    element.send_keys(value)

    time.sleep(0.8)

    actual_value = element.get_attribute("value")

    if actual_value == value:
        print(f"[OK] {field_name} successfully typed.")
        return True

    # JS fallback if Selenium typing did not stick
    print(f"[WARNING] {field_name} did not match after typing.")
    print("[INFO] Trying JavaScript value setter...")

    driver.execute_script(
        """
        const element = arguments[0];
        const value = arguments[1];

        const setter = Object.getOwnPropertyDescriptor(
            HTMLInputElement.prototype,
            'value'
        ).set;

        setter.call(element, value);

        element.dispatchEvent(
            new Event('input', { bubbles: true })
        );

        element.dispatchEvent(
            new Event('change', { bubbles: true })
        );
        """,
        element,
        value
    )

    time.sleep(0.8)

    actual_value = element.get_attribute("value")

    if actual_value == value:
        print(f"[OK] {field_name} successfully typed using fallback.")
        return True

    print(f"[FAILED] {field_name} could not be entered.")
    print("Actual browser value:", actual_value)

    return False


# ============================================================
# Chrome setup
# ============================================================

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

# Prevent undetected_chromedriver destructor WinError 6 noise
uc.Chrome.__del__ = lambda self: None


try:

    # ========================================================
    # STEP 1 — Open homepage
    # ========================================================

    print("\n[1] Opening CANON Directory homepage...")

    driver.get(HOMEPAGE)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//body")
        )
    )

    time.sleep(2)

    print("Homepage:", driver.current_url)
    print("Title:", driver.title)


    # ========================================================
    # STEP 2 — Find actual Submit New link
    # ========================================================

    print("\n[2] Finding actual Submit New link...")

    submit_link_xpath = (
        "//a[contains(@href, '/register.html')]"
    )

    submit_link = wait_for_element(
        driver,
        submit_link_xpath
    )

    discovered_href = submit_link.get_attribute("href")

    print("[OK] Submit New link found")
    print("Discovered href:", discovered_href)


    # ========================================================
    # STEP 3 — Click Submit New
    # ========================================================

    print("\n[3] Clicking Submit New...")

    try:
        click_xpath(
            driver,
            submit_link_xpath
        )

    except Exception as e:
        print("[WARNING] Normal click failed.")
        print("[INFO] Error:", e)

        print("[INFO] Opening discovered href as fallback...")

        driver.get(discovered_href)


    # Wait for register page
    WebDriverWait(driver, 20).until(
        lambda d: "/register.html" in d.current_url
    )

    time.sleep(2)

    print("Current URL:", driver.current_url)
    print("Title:", driver.title)


    # ========================================================
    # STEP 4 — Confirm actual form
    # ========================================================

    print("\n[4] Confirming CANON form fields...")

    name_xpath = "//input[@id='aiToolNameInput']"
    url_xpath = "//input[@id='aiToolInput']"
    description_xpath = "//input[@id='descriptionInput']"
    email_xpath = "//input[@id='emailInput']"

    wait_for_element(driver, name_xpath)
    wait_for_element(driver, url_xpath)
    wait_for_element(driver, description_xpath)
    wait_for_element(driver, email_xpath)

    print("[OK] All 4 required fields detected.")


    # ========================================================
    # STEP 5 — Tool Name
    # ========================================================

    print("\n[5] Filling Tool Name...")

    name_success = fill_field(
        driver,
        name_xpath,
        PRODUCT_NAME,
        "Tool Name"
    )


    # ========================================================
    # STEP 6 — Website URL
    # ========================================================

    print("\n[6] Filling Website URL...")

    url_success = fill_field(
        driver,
        url_xpath,
        WEBSITE_URL,
        "Website URL"
    )


    # ========================================================
    # STEP 7 — Description
    # ========================================================

    print("\n[7] Filling Description...")

    # CANON uses:
    # <input type="text" id="descriptionInput">
    #
    # It is NOT a textarea.

    description_success = fill_field(
        driver,
        description_xpath,
        DESCRIPTION,
        "Description"
    )


    # ========================================================
    # STEP 8 — Email
    # ========================================================

    print("\n[8] Filling Email...")

    email_success = fill_field(
        driver,
        email_xpath,
        EMAIL,
        "Email"
    )


    # ========================================================
    # STEP 9 — Final verification
    # ========================================================

    print("\n[9] Reading values directly from Chrome...")

    actual_name = driver.find_element(
        By.XPATH,
        name_xpath
    ).get_attribute("value")

    actual_url = driver.find_element(
        By.XPATH,
        url_xpath
    ).get_attribute("value")

    actual_description = driver.find_element(
        By.XPATH,
        description_xpath
    ).get_attribute("value")

    actual_email = driver.find_element(
        By.XPATH,
        email_xpath
    ).get_attribute("value")


    print("\n" + "-" * 60)
    print("BROWSER VALUES")
    print("-" * 60)

    print("Tool Name   :", actual_name)
    print("Website URL :", actual_url)
    print("Description :", actual_description)
    print("Email       :", actual_email)


    # ========================================================
    # STEP 10 — Verify everything
    # ========================================================

    all_correct = (
        actual_name == PRODUCT_NAME
        and actual_url == WEBSITE_URL
        and actual_description == DESCRIPTION
        and actual_email == EMAIL
    )


    print("\n" + "=" * 60)

    if all_correct:
        print("CANON DIRECTORY — FORM MAPPING VERIFIED")
        print("=" * 60)

        print("Homepage flow     : PASS")
        print("Submit New link   : PASS")
        print("Tool Name         : PASS")
        print("Website URL       : PASS")
        print("Description       : PASS")
        print("Email             : PASS")
        print("Final Submit      : NOT CLICKED")

    else:
        print("CANON DIRECTORY — VERIFICATION FAILED")
        print("=" * 60)

        print("Tool Name correct   :", actual_name == PRODUCT_NAME)
        print("URL correct          :", actual_url == WEBSITE_URL)
        print("Description correct :", actual_description == DESCRIPTION)
        print("Email correct       :", actual_email == EMAIL)

        print("\nDO NOT submit. Inspect the browser first.")


    # ========================================================
    # IMPORTANT — NEVER SUBMIT AUTOMATICALLY
    # ========================================================

    print("\nThe final Submit button has NOT been clicked.")
    print("Browser will remain open for manual inspection.")

    input("\nPress ENTER to close the browser...")


finally:

    try:
        driver.quit()
    except Exception:
        pass