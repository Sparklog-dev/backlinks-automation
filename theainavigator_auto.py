import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# SILENCE undetected_chromedriver CLEANUP ERROR
# ============================================================

def silent_del(self):
    try:
        pass
    except Exception:
        pass


uc.Chrome.__del__ = silent_del


# ============================================================
# CONFIG
# ============================================================

HOMEPAGE = "https://www.theainavigator.com/"

TOOL_NAME = "Y2Map"
TOOL_URL = "https://y2map.com"

DESCRIPTION = (
    "Y2Map is an AI tool that turns YouTube videos and PDFs "
    "into visual mind maps."
)

YOUR_NAME = "Nikhil"
EMAIL = "sparklog.marketing@gmail.com"


# ============================================================
# START CHROME
# ============================================================

print("\nStarting Chrome...")

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

wait = WebDriverWait(driver, 20)


try:

    # ========================================================
    # STEP 1 — OPEN HOMEPAGE
    # ========================================================

    print("\nOpening The AI Navigator homepage...")

    driver.get(HOMEPAGE)

    time.sleep(4)

    print("Homepage loaded.")
    print("Current URL :", driver.current_url)
    print("Page title  :", driver.title)


    # ========================================================
    # STEP 2 — FIND SUBMISSION LINK
    # ========================================================

    print("\n" + "=" * 70)
    print("FINDING SUBMISSION LINK")
    print("=" * 70)

    submission_links = driver.find_elements(
        By.XPATH,
        "//a[contains("
        "translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'submit an ai tool')]"
    )

    if not submission_links:

        submission_links = driver.find_elements(
            By.XPATH,
            "//a[contains("
            "translate(@href,"
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            "'abcdefghijklmnopqrstuvwxyz'),"
            "'submit-an-ai-tool')]"
        )


    if not submission_links:
        raise Exception(
            "Could not find the 'Submit an AI tool' link."
        )


    submission_link = submission_links[0]

    print("\n✓ Submission link found.")

    print(
        "Text :",
        repr(submission_link.text.strip())
    )

    print(
        "HREF :",
        submission_link.get_attribute("href")
    )


    # ========================================================
    # STEP 3 — OPEN SUBMISSION PAGE
    # ========================================================

    print("\nOpening submission page...")

    href = submission_link.get_attribute("href")

    if href:
        driver.get(href)
    else:
        submission_link.click()

    time.sleep(4)

    print("\nSubmission page opened.")
    print("Current URL :", driver.current_url)
    print("Page title  :", driver.title)


    # ========================================================
    # STEP 4 — WAIT FOR FORM
    # ========================================================

    print("\n" + "=" * 70)
    print("WAITING FOR FORM")
    print("=" * 70)

    tool_name_field = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='name of the AI tool']"
            )
        )
    )

    print("\n✓ Tool Name field detected.")
    print("✓ Custom form rendered successfully.")


    # ========================================================
    # STEP 5 — TOOL NAME
    # ========================================================

    print("\n" + "=" * 70)
    print("FILLING REQUIRED FIELDS")
    print("=" * 70)

    print("\nFilling Tool Name...")

    tool_name_field.click()
    tool_name_field.clear()
    tool_name_field.send_keys(TOOL_NAME)

    print("✓ Tool Name filled.")


    # ========================================================
    # STEP 6 — TOOL URL
    # ========================================================

    print("\nFilling Tool URL...")

    tool_url_field = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='start with https://']"
            )
        )
    )

    tool_url_field.click()
    tool_url_field.clear()
    tool_url_field.send_keys(TOOL_URL)

    print("✓ Tool URL filled.")


    # ========================================================
    # STEP 7 — DESCRIPTION
    # ========================================================

    print("\nFilling Description...")

    description_field = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//textarea[@placeholder='In simple and clear wording']"
            )
        )
    )

    description_field.click()
    description_field.clear()
    description_field.send_keys(DESCRIPTION)

    print("✓ Description filled.")


    # ========================================================
    # STEP 8 — YOUR NAME
    # ========================================================

    print("\nFilling Your Name...")

    name_field = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@name='$item1606282593441#shortText']"
            )
        )
    )

    name_field.click()
    name_field.clear()
    name_field.send_keys(YOUR_NAME)

    print("✓ Your Name filled.")


    # ========================================================
    # STEP 9 — EMAIL
    # ========================================================

    print("\nFilling Email...")

    email_field = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@name='$item1606282596776#email']"
            )
        )
    )

    email_field.click()
    email_field.clear()
    email_field.send_keys(EMAIL)

    print("✓ Email filled.")


    # ========================================================
    # OPTIONAL FIELDS — INTENTIONALLY EMPTY
    # ========================================================

    print("\n" + "=" * 70)
    print("OPTIONAL FIELDS")
    print("=" * 70)

    print("\nThreads handle      : SKIPPED")
    print("Affiliate program   : SKIPPED")
    print("Additional message  : SKIPPED")


    # ========================================================
    # STEP 10 — GDPR CHECKBOX
    # ========================================================

    print("\n" + "=" * 70)
    print("GDPR CHECKBOX")
    print("=" * 70)

    gdpr_checkbox = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//input[@type='checkbox' and "
                "starts-with(@id,'gdpr-1-')]"
            )
        )
    )

    print("\nGDPR checkbox detected.")

    print(
        "Current checked state:",
        gdpr_checkbox.is_selected()
    )

    if not gdpr_checkbox.is_selected():

        gdpr_checkbox.click()

        print("✓ GDPR checkbox checked.")

    else:

        print("✓ GDPR checkbox was already checked.")


    # ========================================================
    # ALLOW FORM STATE TO UPDATE
    # ========================================================

    time.sleep(2)


    # ========================================================
    # VERIFICATION
    # ========================================================

    print("\n" + "=" * 70)
    print("FORM VERIFICATION")
    print("=" * 70)


    actual_tool_name = tool_name_field.get_attribute(
        "value"
    )

    actual_tool_url = tool_url_field.get_attribute(
        "value"
    )

    actual_description = description_field.get_attribute(
        "value"
    )

    actual_name = name_field.get_attribute(
        "value"
    )

    actual_email = email_field.get_attribute(
        "value"
    )


    print("\nTool Name")
    print("  Expected :", TOOL_NAME)
    print("  Actual   :", actual_tool_name)

    if actual_tool_name == TOOL_NAME:
        print("  ✓ Verified.")
    else:
        print("  ✗ MISMATCH.")


    print("\nTool URL")
    print("  Expected :", TOOL_URL)
    print("  Actual   :", actual_tool_url)

    if actual_tool_url == TOOL_URL:
        print("  ✓ Verified.")
    else:
        print("  ✗ MISMATCH.")


    print("\nDescription")
    print("  Expected :", DESCRIPTION)
    print("  Actual   :", actual_description)

    if actual_description == DESCRIPTION:
        print("  ✓ Verified.")
    else:
        print("  ✗ MISMATCH.")


    print("\nYour Name")
    print("  Expected :", YOUR_NAME)
    print("  Actual   :", actual_name)

    if actual_name == YOUR_NAME:
        print("  ✓ Verified.")
    else:
        print("  ✗ MISMATCH.")


    print("\nEmail")
    print("  Expected :", EMAIL)
    print("  Actual   :", actual_email)

    if actual_email == EMAIL:
        print("  ✓ Verified.")
    else:
        print("  ✗ MISMATCH.")


    print("\nGDPR Checkbox")

    print(
        "  Checked :",
        gdpr_checkbox.is_selected()
    )

    if gdpr_checkbox.is_selected():
        print("  ✓ Verified.")
    else:
        print("  ✗ NOT CHECKED.")


    # ========================================================
    # SUBMIT BUTTON CHECK
    # ========================================================

    print("\n" + "=" * 70)
    print("SUBMISSION CONTROL CHECK")
    print("=" * 70)

    submit_button = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//button[normalize-space()='Submit']"
            )
        )
    )

    print("\n✓ Submit button detected.")

    print(
        "Button text :",
        repr(submit_button.text.strip())
    )

    print(
        "Button type :",
        submit_button.get_attribute("type")
    )

    print(
        "Displayed   :",
        submit_button.is_displayed()
    )

    print(
        "Enabled     :",
        submit_button.is_enabled()
    )

    print(
        "Class       :",
        submit_button.get_attribute("class")
    )


    # ========================================================
    # FINAL FIELD CHECK
    # ========================================================

    print("\n" + "=" * 70)
    print("FINAL FIELD CHECK")
    print("=" * 70)

    checks = [
        (
            "Tool Name",
            actual_tool_name == TOOL_NAME
        ),
        (
            "Tool URL",
            actual_tool_url == TOOL_URL
        ),
        (
            "Description",
            actual_description == DESCRIPTION
        ),
        (
            "Your Name",
            actual_name == YOUR_NAME
        ),
        (
            "Email",
            actual_email == EMAIL
        ),
        (
            "GDPR",
            gdpr_checkbox.is_selected()
        ),
    ]

    all_verified = True

    for field_name, result in checks:

        if result:
            print(f"✓ {field_name}")
        else:
            print(f"✗ {field_name}")
            all_verified = False


    # ========================================================
    # IMPORTANT SUBMISSION CONTROL
    # ========================================================

    print("\n" + "=" * 70)
    print("AUTOMATION STOP POINT")
    print("=" * 70)

    if all_verified:

        print(
            "\n✓ ALL MAPPED REQUIRED FIELDS VERIFIED."
        )

    else:

        print(
            "\n⚠ SOME FIELDS FAILED VERIFICATION."
        )


    print("\n✓ Homepage opened.")
    print("✓ Submission link found.")
    print("✓ Submission page opened.")
    print("✓ Dynamic custom form detected.")
    print("✓ Tool Name filled.")
    print("✓ Tool URL filled.")
    print("✓ Description filled.")
    print("✓ Your Name filled.")
    print("✓ Email filled.")
    print("✓ GDPR checkbox checked.")
    print("✓ Optional fields intentionally left empty.")
    print("✓ Submit button identified.")

    print("\n⚠ SUBMIT BUTTON WILL NOT BE CLICKED.")
    print("⚠ NO SUBMISSION WILL BE PERFORMED.")

    print("\nBrowser will remain open for inspection.")

    input("\nPress ENTER to close...")


finally:

    try:
        driver.quit()
    except Exception:
        pass