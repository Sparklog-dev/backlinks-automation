import warnings
import logging
import time

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# SILENCE UNDETECTED-CHROMEDRIVER CLEANUP ERROR
# ============================================================

def silent_del(self):
    pass


uc.Chrome.__del__ = silent_del


# ============================================================
# Y2MAP DETAILS
# ============================================================

TOOL_NAME = "Y2Map"

WEBSITE_URL = "https://y2map.com"

CATEGORY = "AI Productivity"

DESCRIPTION = (
    "Y2Map is an AI-powered learning tool that turns YouTube videos, PDFs, "
    "books, and research content into visual mind maps. It helps students, "
    "researchers, founders, educators, and lifelong learners understand "
    "complex information faster, organize key ideas, and build stronger "
    "mental models."
)

CONTACT_NAME = "Nikhil"

CONTACT_EMAIL = "sparklog.marketing@gmail.com"


# ============================================================
# START BROWSER
# ============================================================

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    options=options,
    version_main=152
)

wait = WebDriverWait(driver, 20)


try:

    # ========================================================
    # STEP 1 — OPEN HOMEPAGE
    # ========================================================

    print("STEP 1 — OPEN AI TOOLS FINDER PRO HOMEPAGE")
    print()

    driver.get("https://aitoolsfinderpro.com/")

    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//body"
            )
        )
    )

    time.sleep(2)

    print("[PASS] Homepage loaded.")
    print(f"Current URL: {driver.current_url}")
    print()


    # ========================================================
    # STEP 2 — FIND ACTUAL SUBMISSION LINK
    # ========================================================

    print("STEP 2 — FIND ACTUAL SUBMISSION LINK")
    print()

    submit_link = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//a[contains(normalize-space(.), 'Submit/Suggest Tool')]"
            )
        )
    )

    print("[PASS] 'Submit/Suggest Tool' link found.")

    driver.execute_script(
        "arguments[0].click();",
        submit_link
    )

    time.sleep(3)

    print(f"Current URL: {driver.current_url}")
    print()


    # ========================================================
    # STEP 3 — FIND "SUBMIT YOUR TOOL"
    # ========================================================

    print("STEP 3 — FIND 'SUBMIT YOUR TOOL'")
    print()

    submit_your_tool = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[normalize-space(.)='Submit Your Tool']"
            )
        )
    )

    print("[PASS] 'Submit Your Tool' button found.")

    driver.execute_script(
        "arguments[0].click();",
        submit_your_tool
    )

    time.sleep(2)

    print("[PASS] 'Submit Your Tool' clicked.")
    print("[PASS] AI tool submission form is visible.")
    print()


    # ========================================================
    # STEP 4 — TOOL NAME
    # ========================================================

    print("STEP 4 — TOOL NAME")

    tool_name_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@name='toolName']"
            )
        )
    )

    tool_name_field.click()
    tool_name_field.send_keys(TOOL_NAME)

    print(f"[PASS] Tool Name: {TOOL_NAME}")
    print()


    # ========================================================
    # STEP 5 — WEBSITE URL
    # ========================================================

    print("STEP 5 — WEBSITE URL")

    website_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@name='websiteUrl']"
            )
        )
    )

    website_field.click()
    website_field.send_keys(WEBSITE_URL)

    print(f"[PASS] Website URL: {WEBSITE_URL}")
    print()


    # ========================================================
    # STEP 6 — CATEGORY
    # ========================================================

    print("STEP 6 — CATEGORY")

    category_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//select[@name='category']"
            )
        )
    )

    category_select = Select(category_field)

    category_select.select_by_visible_text(CATEGORY)

    selected_category = category_select.first_selected_option.text.strip()

    print(f"Selected Category: {selected_category}")

    if selected_category != CATEGORY:
        raise Exception(
            f"Category verification failed. "
            f"Expected '{CATEGORY}', got '{selected_category}'"
        )

    print(f"[PASS] Category: {selected_category}")
    print()


    # ========================================================
    # STEP 7 — DESCRIPTION
    # ========================================================

    print("STEP 7 — DESCRIPTION")

    description_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//textarea[@name='description']"
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        description_field
    )

    time.sleep(1)

    description_field.click()
    description_field.send_keys(DESCRIPTION)

    print("[PASS] Description entered.")
    print()


    # ========================================================
    # STEP 8 — CONTACT NAME
    # ========================================================

    print("STEP 8 — CONTACT NAME")

    contact_name_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@name='contactName']"
            )
        )
    )

    contact_name_field.click()
    contact_name_field.send_keys(CONTACT_NAME)

    print(f"[PASS] Contact Name: {CONTACT_NAME}")
    print()


    # ========================================================
    # STEP 9 — CONTACT EMAIL
    # ========================================================

    print("STEP 9 — CONTACT EMAIL")

    contact_email_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@name='contactEmail']"
            )
        )
    )

    contact_email_field.click()
    contact_email_field.send_keys(CONTACT_EMAIL)

    print(f"[PASS] Contact Email: {CONTACT_EMAIL}")
    print()

    # ========================================================
    # STEP 10 — VERIFY ACTUAL DOM VALUES
    # ========================================================

    print("STEP 10 — VERIFY ACTUAL FORM VALUES")
    print()

    tool_name_element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@name='toolName']"
            )
        )
    )
    actual_tool_name = tool_name_element.get_attribute("value")

    website_element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@name='websiteUrl']"
            )
        )
    )
    actual_website_url = website_element.get_attribute("value")

    category_element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//select[@name='category']"
            )
        )
    )

    actual_category_value = Select(
        category_element
    ).first_selected_option.text.strip()

    description_element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//textarea[@name='description']"
            )
        )
    )
    actual_description = description_element.get_attribute("value")

    contact_name_element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@name='contactName']"
            )
        )
    )
    actual_contact_name = contact_name_element.get_attribute("value")

    contact_email_element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@name='contactEmail']"
            )
        )
    )
    actual_contact_email = contact_email_element.get_attribute("value")

    # ========================================================
    # STEP 11 — DISPLAY VERIFICATION
    # ========================================================

    print("=" * 70)
    print("FORM FILLED - VERIFICATION")
    print("=" * 70)

    print(f"Tool Name      : {actual_tool_name}")
    print(f"Website URL    : {actual_website_url}")
    print(f"Category       : {actual_category_value}")
    print(f"Description    : {actual_description}")
    print(f"Contact Name   : {actual_contact_name}")
    print(f"Contact Email  : {actual_contact_email}")

    print("=" * 70)


    # ========================================================
    # STEP 12 — VERIFY ALL VALUES
    # ========================================================

    print("STEP 12 — FINAL VALUE CHECK")
    print()

    verification_passed = True

    checks = [
        ("Tool Name", actual_tool_name, TOOL_NAME),
        ("Website URL", actual_website_url, WEBSITE_URL),
        ("Category", actual_category_value, CATEGORY),
        ("Description", actual_description, DESCRIPTION),
        ("Contact Name", actual_contact_name, CONTACT_NAME),
        ("Contact Email", actual_contact_email, CONTACT_EMAIL),
    ]

    for field_name, actual_value, expected_value in checks:

        if actual_value == expected_value:
            print(f"[PASS] {field_name} verified.")
        else:
            print(
                f"[FAIL] {field_name} mismatch."
            )
            print(f"       Expected: {expected_value}")
            print(f"       Actual  : {actual_value}")

            verification_passed = False


    if not verification_passed:
        raise Exception(
            "Final form verification failed."
        )


    # ========================================================
    # FINAL STATUS
    # ========================================================

    print()
    print("=" * 70)
    print("AI TOOLS FINDER PRO — MAPPING COMPLETE")
    print("=" * 70)
    print("[PASS] Y2Map information filled.")
    print("[PASS] All mapped fields verified.")
    print("[STOP] No Submit button clicked.")
    print("[STOP] No form submission performed.")
    print("[STOP] Browser remains open for inspection.")
    print("=" * 70)
    print()

    input("Press ENTER to close the browser...")


except Exception as e:

    print()
    print("=" * 70)
    print("ERROR")
    print("=" * 70)
    print(type(e).__name__)
    print(str(e))
    print("=" * 70)
    print()
    print("Browser will remain open for inspection.")
    input("Press ENTER to close the browser...")


finally:

    try:
        driver.quit()
    except Exception:
        pass