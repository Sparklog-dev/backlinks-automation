import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# AI KENDRA AUTOMATION
# Workflow:
# Homepage -> Submit Tool -> Fill form -> Verify
# STOP before final submission
#
# IMPORTANT:
# - XPath only for Selenium selectors
# - Security verification is NOT bypassed
# - Final "Submit Free listing" is NOT clicked
# ============================================================


# -----------------------------
# Y2Map information
# -----------------------------

PRODUCT_NAME = "Y2Map"

WEBSITE_URL = "https://y2map.com"

TAGLINE = "Convert YouTube videos and PDFs into mind maps."

DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that transforms "
    "YouTube videos, PDFs, books, and research content into easy-to-understand "
    "visual mind maps. It helps users understand complex topics faster by "
    "organizing important ideas, concepts, summaries, references, and related "
    "information into a structured visual format."
)

TAGS = "AI, Mind Maps, YouTube, PDF, Productivity"

EMAIL = "sparklog.marketing@gmail.com"

CATEGORY = "Productivity"

PRICING = "Free"


# -----------------------------
# Chrome setup
# -----------------------------

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

# Prevent harmless uc cleanup error
uc.Chrome.__del__ = lambda self: None

wait = WebDriverWait(driver, 20)


def find_xpath(xpath, timeout=20):
    """Wait for an element using XPath only."""
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def click_xpath(xpath, timeout=20):
    """Click an element using XPath only."""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )

    try:
        element.click()
    except Exception:
        # JS click fallback, while the element is still located by XPath
        driver.execute_script("arguments[0].click();", element)

    return element


def fill_xpath(xpath, value, timeout=20):
    """Clear and type into an element located using XPath only."""
    element = find_xpath(xpath, timeout)

    driver.execute_script(
        """
        arguments[0].scrollIntoView({
            behavior: 'instant',
            block: 'center'
        });
        """,
        element
    )

    try:
        element.click()
    except Exception:
        pass

    element.clear()
    element.send_keys(value)

    return element


def get_value_xpath(xpath, timeout=20):
    """Read actual browser value from an input/textarea."""
    element = find_xpath(xpath, timeout)

    return driver.execute_script(
        "return arguments[0].value;",
        element
    )


try:

    # ========================================================
    # STEP 1 — OPEN HOMEPAGE
    # ========================================================

    print("\n[STEP 1] Opening AI Kendra homepage...")

    driver.get("https://aikendra.com/")

    time.sleep(3)

    print("[OK] URL:", driver.current_url)
    print("[OK] Title:", driver.title)


    # ========================================================
    # STEP 2 — FIND ACTUAL SUBMIT LINK ON HOMEPAGE
    # ========================================================

    print("\n[STEP 2] Looking for actual Submit link...")

    submit_xpath = (
        "//a["
        "contains(normalize-space(.), 'Submit') "
        "and "
        "contains(@href, '/submit')"
        "]"
    )

    submit_link = find_xpath(submit_xpath)

    print("[OK] Found Submit link:")
    print("[INFO] href:", submit_link.get_attribute("href"))

    print("[INFO] Clicking actual homepage Submit link...")

    click_xpath(submit_xpath)

    time.sleep(3)

    print("[OK] Submit page opened.")
    print("[OK] Current URL:", driver.current_url)


    # ========================================================
    # STEP 3 — VERIFY SUBMIT PAGE
    # ========================================================

    print("\n[STEP 3] Checking Submit Tool page...")

    heading_xpath = (
        "//h1[contains(normalize-space(.), 'List your AI tool')]"
    )

    find_xpath(heading_xpath)

    print("[OK] Submit Tool page detected.")


    # ========================================================
    # STEP 4 — TOOL NAME
    # ========================================================

    print("\n[STEP 4] Filling Tool Name...")

    # Uses the visible label relationship rather than IDs.
    tool_name_xpath = (
        "//label["
        "contains(normalize-space(.), 'Tool name')"
        "]"
        "/following::input[1]"
    )

    fill_xpath(tool_name_xpath, PRODUCT_NAME)

    actual_tool_name = get_value_xpath(tool_name_xpath)

    if actual_tool_name == PRODUCT_NAME:
        print("[PASS] Tool Name verified:", actual_tool_name)
    else:
        print("[FAIL] Tool Name mismatch.")
        print("[INFO] Browser value:", actual_tool_name)


    # ========================================================
    # STEP 5 — WEBSITE
    # ========================================================

    print("\n[STEP 5] Filling Website...")

    website_xpath = (
        "//label["
        "contains(normalize-space(.), 'Website')"
        "]"
        "/following::input[1]"
    )

    fill_xpath(website_xpath, WEBSITE_URL)

    actual_website = get_value_xpath(website_xpath)

    if actual_website == WEBSITE_URL:
        print("[PASS] Website verified:", actual_website)
    else:
        print("[FAIL] Website mismatch.")
        print("[INFO] Browser value:", actual_website)


    # ========================================================
    # STEP 6 — CATEGORY
    # ========================================================

    print("\n[STEP 6] Selecting Category...")

    # AI Kendra does not provide Education.
    # Productivity is the selected category for Y2Map.

    category_xpath = (
        "//button["
        "normalize-space(.)='Productivity'"
        "]"
    )

    category_button = find_xpath(category_xpath)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        category_button
    )

    click_xpath(category_xpath)

    time.sleep(1)

    print("[OK] Productivity category selected.")


    # ========================================================
    # STEP 7 — PRICING MODEL
    # ========================================================

    print("\n[STEP 7] Selecting Pricing Model: Free...")

    pricing_xpath = (
        "//button["
        "normalize-space(.)='Free'"
        "]"
    )

    click_xpath(pricing_xpath)

    time.sleep(1)

    print("[OK] Free pricing selected.")


    # ========================================================
    # STEP 8 — TAGLINE
    # ========================================================

    print("\n[STEP 8] Filling One-line Tagline...")

    tagline_xpath = (
        "//label["
        "contains(normalize-space(.), 'One-line tagline')"
        "]"
        "/following::input[1]"
    )

    fill_xpath(tagline_xpath, TAGLINE)

    actual_tagline = get_value_xpath(tagline_xpath)

    if actual_tagline == TAGLINE:
        print("[PASS] Tagline verified.")
    else:
        print("[FAIL] Tagline mismatch.")
        print("[INFO] Browser value:", actual_tagline)


    # ========================================================
    # STEP 9 — DESCRIPTION
    # ========================================================

    print("\n[STEP 9] Filling Description...")

    description_xpath = (
        "//label["
        "contains(normalize-space(.), 'Description')"
        "]"
        "/following::textarea[1]"
    )

    fill_xpath(description_xpath, DESCRIPTION)

    actual_description = get_value_xpath(description_xpath)

    if actual_description == DESCRIPTION:
        print("[PASS] Description verified.")
    else:
        print("[FAIL] Description mismatch.")
        print("[INFO] Browser value:", actual_description)


    # ========================================================
    # STEP 10 — TAGS
    # ========================================================

    print("\n[STEP 10] Filling Tags...")

    tags_xpath = (
        "//label["
        "contains(normalize-space(.), 'Tags')"
        "]"
        "/following::input[1]"
    )

    fill_xpath(tags_xpath, TAGS)

    actual_tags = get_value_xpath(tags_xpath)

    if actual_tags == TAGS:
        print("[PASS] Tags verified:", actual_tags)
    else:
        print("[FAIL] Tags mismatch.")
        print("[INFO] Browser value:", actual_tags)


    # ========================================================
    # STEP 11 — EMAIL
    # ========================================================

    print("\n[STEP 11] Filling Email...")

    email_xpath = (
        "//label["
        "contains(normalize-space(.), 'Your email')"
        "]"
        "/following::input[1]"
    )

    fill_xpath(email_xpath, EMAIL)

    actual_email = get_value_xpath(email_xpath)

    if actual_email == EMAIL:
        print("[PASS] Email verified:", actual_email)
    else:
        print("[FAIL] Email mismatch.")
        print("[INFO] Browser value:", actual_email)


    # ========================================================
    # STEP 12 — SECURITY VERIFICATION
    # ========================================================

    print("\n[STEP 12] Checking security verification...")

    security_text_xpath = (
        "//*["
        "contains(normalize-space(.), 'security verification')"
        "]"
    )

    try:
        find_xpath(security_text_xpath, timeout=5)

        print("[OK] Security verification detected.")
        print("[INFO] Security verification will NOT be bypassed.")
        print("[INFO] Manual browser interaction may be required.")

    except Exception:
        print("[INFO] Security verification text was not detected.")


    # ========================================================
    # STEP 13 — TERMS CHECKBOX
    # ========================================================

    print("\n[STEP 13] Checking Terms checkbox...")

    terms_label_xpath = (
        "//label["
        "contains(normalize-space(.), 'Terms of Service')"
        "]"
    )

    try:

        terms_label = find_xpath(terms_label_xpath, timeout=8)

        # Find checkbox inside/near the Terms label using XPath.
        terms_checkbox_xpath = (
            "//label["
            "contains(normalize-space(.), 'Terms of Service')"
            "]"
            "//input[@type='checkbox']"
        )

        try:
            checkbox = find_xpath(terms_checkbox_xpath, timeout=5)

            is_checked = checkbox.is_selected()

            if not is_checked:
                click_xpath(terms_checkbox_xpath)
                print("[OK] Terms checkbox checked.")
            else:
                print("[OK] Terms checkbox was already checked.")

        except Exception:
            # Some custom checkbox implementations place the input elsewhere.
            print("[INFO] Terms checkbox is custom-rendered.")
            print("[INFO] Inspecting label for manual confirmation.")

    except Exception:
        print("[WARNING] Terms label could not be located.")


    # ========================================================
    # STEP 14 — NEWSLETTER
    # ========================================================

    print("\n[STEP 14] Checking newsletter option...")

    newsletter_xpath = (
        "//label["
        "contains(normalize-space(.), 'Kendra Brief')"
        "]"
        "//input[@type='checkbox']"
    )

    try:

        newsletter_checkbox = find_xpath(newsletter_xpath, timeout=5)

        if newsletter_checkbox.is_selected():
            click_xpath(newsletter_xpath)
            print("[OK] Newsletter checkbox unchecked.")

        else:
            print("[OK] Newsletter checkbox already unchecked.")

    except Exception:
        print("[INFO] Newsletter checkbox not directly located.")
        print("[INFO] Leaving newsletter option untouched.")


    # ========================================================
    # STEP 15 — FINAL VERIFICATION
    # ========================================================

    print("\n[STEP 15] Final browser-value verification...")

    checks = {
        "Tool Name": (tool_name_xpath, PRODUCT_NAME),
        "Website": (website_xpath, WEBSITE_URL),
        "Tagline": (tagline_xpath, TAGLINE),
        "Description": (description_xpath, DESCRIPTION),
        "Tags": (tags_xpath, TAGS),
        "Email": (email_xpath, EMAIL),
    }

    all_passed = True

    for field_name, (xpath, expected) in checks.items():

        try:
            actual = get_value_xpath(xpath)

            if actual == expected:
                print(f"[PASS] {field_name}")
            else:
                print(f"[FAIL] {field_name}")
                print(f"       Expected: {expected}")
                print(f"       Actual:   {actual}")
                all_passed = False

        except Exception as e:
            print(f"[FAIL] {field_name} could not be verified.")
            print("       Error:", e)
            all_passed = False


    # ========================================================
    # FINAL STATUS
    # ========================================================

    print("\n" + "=" * 60)

    if all_passed:
        print("MAPPING COMPLETE")
        print("ALL TEXT FIELDS VERIFIED SUCCESSFULLY.")
    else:
        print("MAPPING COMPLETED WITH VERIFICATION WARNINGS.")

    print("=" * 60)

    print("\n[STOP]")
    print("The final 'Submit Free listing' button was NOT clicked.")
    print("No submission was made.")
    print("Security verification was NOT bypassed.")
    print("\nBrowser will remain open for inspection.")

    input("\nPress Enter to close the browser...")


except Exception as e:

    print("\n" + "=" * 60)
    print("[ERROR] Automation stopped.")
    print("=" * 60)
    print(type(e).__name__, ":", e)

    input("\nPress Enter to close the browser...")


finally:

    try:
        driver.quit()
    except Exception:
        pass