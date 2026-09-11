import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# CONFIGURATION
# ============================================================

TOOL_NAME = "Y2Map"
TOOL_URL = "https://y2map.com"
COMPANY = "Y2Map"
CONTACT_EMAIL = "sparklog.marketing@gmail.com"

SHORT_DESCRIPTION = (
    "Y2Map is an AI tool that turns YouTube videos and PDFs into visual mind maps."
)

CATEGORY = "Education"
PRICING_TYPE = "freemium"

HOMEPAGE_URL = "https://aitoolsboard.com/"
SUBMIT_URL = "https://aitoolsboard.com/submit"


# ============================================================
# SILENCE UNDETECTED_CHROMEDRIVER CLEANUP ERROR
# ============================================================

def silent_del(self):
    try:
        pass
    except Exception:
        pass


uc.Chrome.__del__ = silent_del


# ============================================================
# START CHROME
# ============================================================

print()
print("Starting Chrome...")

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

wait = WebDriverWait(driver, 20)


try:

    # ========================================================
    # OPEN HOMEPAGE
    # ========================================================

    print()
    print("Opening AI Tools Board homepage...")

    driver.get(HOMEPAGE_URL)

    wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    time.sleep(2)

    print("Homepage loaded.")
    print("Current URL:", driver.current_url)


    # ========================================================
    # OPEN SUBMISSION PAGE
    # ========================================================

    print()
    print("Opening Submit Your Tool page directly...")

    driver.get(SUBMIT_URL)

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "form[action='/submit']")
        )
    )

    time.sleep(2)

    print("Submission page opened.")
    print("Current URL:", driver.current_url)
    print("Page title:", driver.title)


    # ========================================================
    # CHECK SUBMISSION FORM
    # ========================================================

    print()
    print("Checking submission form...")

    submission_form = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "form[action='/submit']")
        )
    )

    if submission_form.is_displayed():

        print("✓ Submission form confirmed.")

    else:

        raise Exception("Submission form is not visible.")


    # ========================================================
    # TOOL NAME
    # ========================================================

    print()
    print("Filling Tool Name...")

    name_field = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "name")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        name_field
    )

    time.sleep(0.5)

    name_field.click()
    name_field.clear()
    name_field.send_keys(TOOL_NAME)

    print("✓ Tool Name filled.")


    # ========================================================
    # WEBSITE URL
    # ========================================================

    print("Filling Website URL...")

    website_field = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "website_url")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        website_field
    )

    time.sleep(0.5)

    website_field.click()
    website_field.clear()
    website_field.send_keys(TOOL_URL)

    print("✓ Website URL filled.")


    # ========================================================
    # SHORT DESCRIPTION
    # ========================================================

    print()
    print("Filling Short Description...")

    description_field = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "textarea[name='description']")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        description_field
    )

    time.sleep(1)

    print("Description textarea located.")
    print("Displayed :", description_field.is_displayed())
    print("Enabled   :", description_field.is_enabled())

    description_field.click()
    description_field.clear()
    description_field.send_keys(SHORT_DESCRIPTION)

    time.sleep(1)

    # ========================================================
    # DESCRIPTION VERIFICATION
    # ========================================================

    actual_description = description_field.get_attribute("value") or ""

    print()
    print("DESCRIPTION VERIFICATION")
    print("Expected characters :", len(SHORT_DESCRIPTION))
    print("Actual characters   :", len(actual_description))
    print("Description         :", actual_description)

    if actual_description == SHORT_DESCRIPTION:

        print("✓ Short description verified.")

    else:

        raise Exception(
            "Short description verification failed."
        )


    # ========================================================
    # COMPANY
    # ========================================================

    print()
    print("Filling Company...")

    company_field = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "company")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        company_field
    )

    time.sleep(0.5)

    company_field.click()
    company_field.clear()
    company_field.send_keys(COMPANY)

    print("✓ Company filled.")


    # ========================================================
    # SUBMITTER EMAIL
    # ========================================================

    print("Filling Submitter Email...")

    email_field = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "submitter_email")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        email_field
    )

    time.sleep(0.5)

    email_field.click()
    email_field.clear()
    email_field.send_keys(CONTACT_EMAIL)

    print("✓ Submitter email filled.")


    # ========================================================
    # CATEGORY
    # ========================================================

    print()
    print("Selecting Category...")

    category_select = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "category_id")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        category_select
    )

    time.sleep(0.5)

    category_dropdown = Select(category_select)

    category_dropdown.select_by_visible_text(CATEGORY)

    selected_category = category_dropdown.first_selected_option.text.strip()

    print("Selected category:", selected_category)

    if selected_category == CATEGORY:

        print("✓ Category verified.")

    else:

        raise Exception(
            f"Category verification failed. "
            f"Expected: {CATEGORY}, "
            f"Actual: {selected_category}"
        )


    # ========================================================
    # PRICING TYPE
    # ========================================================

    print()
    print("Selecting Pricing Type...")

    pricing_select = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "pricing_type")
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        pricing_select
    )

    time.sleep(0.5)

    pricing_dropdown = Select(pricing_select)

    pricing_dropdown.select_by_value(PRICING_TYPE)

    selected_pricing = (
        pricing_dropdown.first_selected_option.get_attribute("value")
    )

    selected_pricing_text = (
        pricing_dropdown.first_selected_option.text.strip()
    )

    print("Selected pricing:", selected_pricing_text)

    if selected_pricing == PRICING_TYPE:

        print("✓ Pricing type verified.")

    else:

        raise Exception(
            f"Pricing verification failed. "
            f"Expected: {PRICING_TYPE}, "
            f"Actual: {selected_pricing}"
        )


    # ========================================================
    # OPTIONAL FIELDS
    # ========================================================

    print()
    print("=" * 60)
    print("OPTIONAL FIELDS")
    print("=" * 60)

    print("Affiliate URL      : SKIPPED")
    print("Full Description   : SKIPPED")
    print("Twitter            : SKIPPED")
    print("GitHub             : SKIPPED")
    print("LinkedIn           : SKIPPED")
    print("YouTube            : SKIPPED")
    print("Market Segment     : SKIPPED")
    print("Price Segment      : SKIPPED")
    print("Starting Price     : SKIPPED")
    print("Features           : SKIPPED")
    print("Fast Track Review  : SKIPPED")


    # ========================================================
    # FINAL FORM VERIFICATION
    # ========================================================

    print()
    print("=" * 60)
    print("FINAL FORM VERIFICATION")
    print("=" * 60)


    # Re-read all required fields from the live form

    final_name = (
        name_field.get_attribute("value") or ""
    )

    final_website = (
        website_field.get_attribute("value") or ""
    )

    final_description = (
        description_field.get_attribute("value") or ""
    )

    final_company = (
        company_field.get_attribute("value") or ""
    )

    final_email = (
        email_field.get_attribute("value") or ""
    )

    final_category = (
        category_dropdown.first_selected_option.text.strip()
    )

    final_pricing = (
        pricing_dropdown.first_selected_option.get_attribute("value")
        or ""
    )


    # ========================================================
    # PRINT FINAL VALUES
    # ========================================================

    print("Tool Name    :", final_name)
    print("Website URL  :", final_website)
    print("Description  :", len(final_description), "characters")
    print("Description  :", final_description)
    print("Company      :", final_company)
    print("Email        :", final_email)
    print("Category     :", final_category)
    print("Pricing      :", final_pricing)


    # ========================================================
    # VERIFY REQUIRED VALUES
    # ========================================================

    print()
    print("Checking required field values...")

    verification_passed = True


    if final_name != TOOL_NAME:

        print("✗ Tool Name mismatch.")
        verification_passed = False

    else:

        print("✓ Tool Name correct.")


    if final_website != TOOL_URL:

        print("✗ Website URL mismatch.")
        verification_passed = False

    else:

        print("✓ Website URL correct.")


    if final_description != SHORT_DESCRIPTION:

        print("✗ Description mismatch.")
        verification_passed = False

    else:

        print("✓ Description correct.")


    if final_company != COMPANY:

        print("✗ Company mismatch.")
        verification_passed = False

    else:

        print("✓ Company correct.")


    if final_email != CONTACT_EMAIL:

        print("✗ Email mismatch.")
        verification_passed = False

    else:

        print("✓ Email correct.")


    if final_category != CATEGORY:

        print("✗ Category mismatch.")
        verification_passed = False

    else:

        print("✓ Category correct.")


    if final_pricing != PRICING_TYPE:

        print("✗ Pricing mismatch.")
        verification_passed = False

    else:

        print("✓ Pricing correct.")


    if not verification_passed:

        raise Exception(
            "FINAL FORM VERIFICATION FAILED."
        )


    print()
    print("✓ ALL REQUIRED FIELDS VERIFIED SUCCESSFULLY.")


    # ========================================================
    # FIND SUBMIT BUTTON
    # ========================================================

    print()
    print("=" * 60)
    print("SUBMISSION CONTROL CHECK")
    print("=" * 60)

    submit_button = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//button[@type='submit' and "
                "contains(normalize-space(), "
                "'Submit Tool for Review')]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        submit_button
    )

    time.sleep(1)

    print("✓ Submit Tool for Review button found.")
    print("Button text :", submit_button.text.strip())
    print("Button type :", submit_button.get_attribute("type"))

    print()
    print("⚠ SUBMIT BUTTON WILL NOT BE CLICKED.")


    # ========================================================
    # FINAL STOP POINT
    # ========================================================

    print()
    print("=" * 60)
    print("AUTOMATION STOP POINT")
    print("=" * 60)

    print("✓ Homepage opened")
    print("✓ Submission page opened")
    print("✓ Submission form confirmed")
    print("✓ Tool Name filled and verified")
    print("✓ Website URL filled and verified")
    print("✓ Short Description filled and verified")
    print("✓ Company filled and verified")
    print("✓ Submitter Email filled and verified")
    print("✓ Category selected and verified")
    print("✓ Pricing Type selected and verified")
    print("✓ Optional fields intentionally left empty")
    print("✓ Submit button identified")
    print("✓ NO SUBMISSION PERFORMED")

    print()
    print("Browser will remain open for inspection.")
    print("Press ENTER to close...")

    input()


except Exception as e:

    print()
    print("=" * 60)
    print("AUTOMATION ERROR")
    print("=" * 60)

    print(type(e).__name__ + ":", e)

    print()
    print("Browser will remain open for inspection.")
    print("Press ENTER to close...")

    input()


finally:

    try:
        driver.quit()
    except Exception:
        pass