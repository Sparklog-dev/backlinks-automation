# faceless_auto.py

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)


# Prevent harmless uc cleanup error on Windows
uc.Chrome.__del__ = lambda self: None


# ============================================================
# CONFIG
# ============================================================

HOMEPAGE = "https://faceless.directory/"
EXPECTED_SUBMIT_URL = "https://faceless.directory/submit"

TOOL_NAME = "Y2Map"
WEBSITE_URL = "https://y2map.com"
EMAIL = "sparklog.marketing@gmail.com"

CATEGORY = "Other"

SHORT_DESCRIPTION = (
    "Turn YouTube videos and PDFs into clear visual mind maps."
)


# ============================================================
# BROWSER
# ============================================================

options = uc.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = uc.Chrome(
    version_main=152,
    options=options
)

wait = WebDriverWait(driver, 15)


# ============================================================
# HELPERS
# ============================================================

def find_xpath(xpath, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )


def find_visible_xpath(xpath, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


def click_xpath(xpath, timeout=15):
    element = find_visible_xpath(xpath, timeout)

    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script(
            "arguments[0].click();",
            element
        )

    return element


def fill_xpath(xpath, value, timeout=15):
    element = find_visible_xpath(xpath, timeout)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )

    element.clear()
    element.send_keys(value)

    return element


def get_value_xpath(xpath, timeout=15):
    element = find_xpath(xpath, timeout)
    return element.get_attribute("value")


def verify_input(xpath, expected, label):
    actual = get_value_xpath(xpath)

    if actual == expected:
        print(f"[PASS] {label} verified: {actual}")
        return True

    print(f"[FAIL] {label}")
    print(f"       Expected: {expected}")
    print(f"       Actual:   {actual}")
    return False


# ============================================================
# MAIN
# ============================================================

try:

    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    print("\n[STEP 1] Opening Faceless Directory homepage...")

    driver.get(HOMEPAGE)

    wait.until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    print(f"[OK] URL: {driver.current_url}")
    print(f"[OK] Title: {driver.title}")


    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    print("\n[STEP 2] Looking for actual Submit link...")

    submit_link_xpath = (
        "//a[contains(@href,'/submit') "
        "and contains(normalize-space(.),'Submit')]"
    )

    submit_link = find_visible_xpath(submit_link_xpath)

    href = submit_link.get_attribute("href")

    print("[OK] Found Submit link.")
    print(f"[INFO] href: {href}")

    if EXPECTED_SUBMIT_URL not in href:
        raise Exception(
            f"Unexpected Submit URL: {href}"
        )

    print("[INFO] Clicking actual homepage Submit link...")

    click_xpath(submit_link_xpath)

    WebDriverWait(driver, 15).until(
        lambda d: "/submit" in d.current_url
    )

    print("[OK] Submit page opened.")
    print(f"[OK] Current URL: {driver.current_url}")


    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    print("\n[STEP 3] Checking Submit Tool page...")

    form_control_xpath = (
        "//input"
        " | //select"
        " | //textarea"
        " | //button[contains("
        "translate(normalize-space(.),"
        "'abcdefghijklmnopqrstuvwxyz',"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),"
        "'SUBMIT TOOL')]"
    )

    find_xpath(form_control_xpath, timeout=15)

    print("[OK] Submission form detected.")


    # --------------------------------------------------------
    # STEP 4 - TOOL NAME
    # --------------------------------------------------------

    print("\n[STEP 4] Filling Tool Name...")

    tool_name_xpath = (
        "//input["
        "contains(translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'tool name')"
        "]"
        " | //label[contains(normalize-space(.),'Tool name')]/following::input[1]"
    )

    fill_xpath(
        tool_name_xpath,
        TOOL_NAME
    )

    verify_input(
        tool_name_xpath,
        TOOL_NAME,
        "Tool Name"
    )


    # --------------------------------------------------------
    # STEP 5 - WEBSITE URL
    # --------------------------------------------------------

    print("\n[STEP 5] Filling Tool URL...")

    website_xpath = (
        "//input["
        "contains(translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'https://')"
        "]"
        " | //label[contains(normalize-space(.),'Tool URL')]/following::input[1]"
    )

    fill_xpath(
        website_xpath,
        WEBSITE_URL
    )

    verify_input(
        website_xpath,
        WEBSITE_URL,
        "Tool URL"
    )


    # --------------------------------------------------------
    # STEP 6 - SHORT DESCRIPTION
    # --------------------------------------------------------

    print("\n[STEP 6] Checking for Short Description field...")

    short_description_xpath = (
        "//label[contains(translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'short description')]/following::input[1]"
        " | //label[contains(translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'short description')]/following::textarea[1]"
        " | //input[contains(translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'short description')]"
        " | //textarea[contains(translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'short description')]"
    )

    try:

        short_description_element = find_visible_xpath(
            short_description_xpath,
            timeout=5
        )

        print("[OK] Short Description field detected.")

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            short_description_element
        )

        short_description_element.clear()
        short_description_element.send_keys(
            SHORT_DESCRIPTION
        )

        actual_short_description = (
            short_description_element.get_attribute("value")
        )

        if actual_short_description == SHORT_DESCRIPTION:

            print(
                "[PASS] Short Description verified: "
                f"{actual_short_description}"
            )

        else:

            print("[FAIL] Short Description verification failed.")
            print(
                f"[INFO] Expected: {SHORT_DESCRIPTION}"
            )
            print(
                f"[INFO] Actual:   {actual_short_description}"
            )

    except TimeoutException:

        print(
            "[INFO] Short Description field was not found."
        )

        print(
            "[INFO] No short description was entered."
        )


    # --------------------------------------------------------
    # STEP 7 - CATEGORY
    # --------------------------------------------------------

    print("\n[STEP 7] Selecting Category...")

    category_xpath = (
        "//label[contains(normalize-space(.),'Category')]/following::select[1]"
        " | //select[1]"
    )

    category_element = find_visible_xpath(
        category_xpath,
        timeout=15
    )

    category_select = Select(category_element)

    available_categories = [
        option.text.strip()
        for option in category_select.options
        if option.text.strip()
    ]

    print("[INFO] Available categories:")

    for category in available_categories:
        print(f"       - {category}")

    if CATEGORY in available_categories:

        category_select.select_by_visible_text(
            CATEGORY
        )

    else:

        print(
            f"[WARNING] '{CATEGORY}' was not found."
        )

        print(
            "[INFO] Category will not be changed."
        )

    selected_category = Select(
        find_xpath(category_xpath)
    ).first_selected_option.text.strip()

    print(
        f"[INFO] Browser selected category: "
        f"{selected_category}"
    )

    if selected_category == CATEGORY:

        print(
            f"[PASS] Category verified: "
            f"{selected_category}"
        )

    else:

        print(
            "[INFO] Category differs from requested value."
        )


    # --------------------------------------------------------
    # STEP 8 - EMAIL
    # --------------------------------------------------------

    print("\n[STEP 8] Filling Email...")

    email_xpath = (
        "//input[@type='email']"
        " | //input["
        "contains(translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'email')"
        "]"
        " | //label[contains(normalize-space(.),'email')]/following::input[1]"
    )

    fill_xpath(
        email_xpath,
        EMAIL
    )

    verify_input(
        email_xpath,
        EMAIL,
        "Email"
    )


    # --------------------------------------------------------
    # STEP 9 - FINAL BUTTON
    # --------------------------------------------------------

    print("\n[STEP 9] Checking final Submit Tool button...")

    final_button_xpath = (
        "//button["
        "contains(translate(normalize-space(.),"
        "'abcdefghijklmnopqrstuvwxyz',"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),"
        "'SUBMIT TOOL')"
        "]"
        " | //input["
        "@type='submit' "
        "and contains(translate(@value,"
        "'abcdefghijklmnopqrstuvwxyz',"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ'),"
        "'SUBMIT TOOL')"
        "]"
    )

    try:

        find_visible_xpath(
            final_button_xpath,
            timeout=10
        )

        print(
            "[OK] Final 'SUBMIT TOOL' button detected."
        )

        print(
            "[STOP] Submit Tool will NOT be clicked."
        )

    except TimeoutException:

        print(
            "[WARNING] Final Submit Tool button "
            "could not be located."
        )


    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("MAPPING COMPLETE")
    print("=" * 60)

    print("[PASS] Homepage opened.")
    print("[PASS] Actual Submit link followed.")
    print("[PASS] Submission form detected.")
    print("[PASS] Tool Name verified.")
    print("[PASS] Tool URL verified.")
    print("[PASS] Email verified.")

    if selected_category == CATEGORY:
        print(
            f"[PASS] Category verified: {selected_category}"
        )

    print("\n[STOP]")
    print("The final 'SUBMIT TOOL' button was NOT clicked.")
    print("No submission was made.")

    print("\nBrowser will remain open for inspection.")

    input("\nPress Enter to close the browser...")


except TimeoutException as e:

    print("\n" + "=" * 60)
    print("[ERROR] Automation stopped.")
    print("=" * 60)

    print("TimeoutException:", e)

    print("\nCurrent URL:")
    print(driver.current_url)

    print("\nCurrent title:")
    print(driver.title)

    input("\nPress Enter to close the browser...")


except Exception as e:

    print("\n" + "=" * 60)
    print("[ERROR] Automation stopped.")
    print("=" * 60)

    print(type(e).__name__, ":", e)

    print("\nCurrent URL:")
    print(driver.current_url)

    print("\nCurrent title:")
    print(driver.title)

    input("\nPress Enter to close the browser...")


finally:

    try:
        driver.quit()
    except Exception:
        pass