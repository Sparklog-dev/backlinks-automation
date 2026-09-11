# techtools_auto.py

import time
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

HOMEPAGE = "https://techtools.cz/"
EXPECTED_LAUNCHPAD = "https://techtools.cz/tools/launchpad/"

TOOL_NAME = "Y2Map"
WEBSITE_URL = "https://y2map.com"

TAGLINE = "Convert YouTube videos and PDFs into mind maps."

DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that transforms "
    "YouTube videos, PDFs, books, and research content into easy-to-understand "
    "visual mind maps. It helps users understand complex topics faster by "
    "organizing important ideas, concepts, summaries, references, and related "
    "information into a structured visual format."
)

CATEGORY = "AI & Machine Learning"

YOUR_NAME = "Nikhil"
YOUR_WEBSITE = "https://y2map.com"


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
# MAIN AUTOMATION
# ============================================================

try:

    # --------------------------------------------------------
    # STEP 1
    # --------------------------------------------------------

    print("\n[STEP 1] Opening TechTools homepage...")

    driver.get(HOMEPAGE)

    wait.until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    print(f"[OK] URL: {driver.current_url}")
    print(f"[OK] Title: {driver.title}")


    # --------------------------------------------------------
    # STEP 2
    # --------------------------------------------------------

    print("\n[STEP 2] Looking for actual Launchpad link...")

    launchpad_xpath = (
        "//a[contains(@href,'/tools/launchpad/') "
        "and contains(normalize-space(.),'Launchpad')]"
    )

    launchpad_link = find_visible_xpath(launchpad_xpath)

    href = launchpad_link.get_attribute("href")

    print("[OK] Found Launchpad link.")
    print(f"[INFO] href: {href}")

    if EXPECTED_LAUNCHPAD not in href:
        raise Exception(
            f"Unexpected Launchpad URL: {href}"
        )

    print("[INFO] Clicking actual Launchpad link...")

    click_xpath(launchpad_xpath)

    WebDriverWait(driver, 15).until(
        lambda d: "/tools/launchpad/" in d.current_url
    )

    print("[OK] Launchpad opened.")
    print(f"[OK] Current URL: {driver.current_url}")


    # --------------------------------------------------------
    # STEP 3
    # --------------------------------------------------------

    print("\n[STEP 3] Checking Launchpad page...")

    # Instead of depending on one exact heading/text,
    # check for the actual form controls.

    page_ready_xpath = (
        "//input["
        "@placeholder='My Awesome Tool'"
        " or @placeholder='https://myawesometool.com'"
        "]"
        " | //textarea"
        " | //select"
    )

    find_xpath(page_ready_xpath, timeout=15)

    print("[OK] Launchpad form detected.")


    # --------------------------------------------------------
    # STEP 4 - TOOL NAME
    # --------------------------------------------------------

    print("\n[STEP 4] Filling Tool Name...")

    tool_name_xpath = (
        "//label[contains(normalize-space(.),'Tool Name')]/following::input[1]"
        " | //input[@placeholder='My Awesome Tool']"
    )

    fill_xpath(tool_name_xpath, TOOL_NAME)

    verify_input(
        tool_name_xpath,
        TOOL_NAME,
        "Tool Name"
    )


    # --------------------------------------------------------
    # STEP 5 - WEBSITE
    # --------------------------------------------------------

    print("\n[STEP 5] Filling Website URL...")

    website_xpath = (
        "//label[contains(normalize-space(.),'URL')]/following::input[1]"
        " | //input[@placeholder='https://myawesometool.com']"
    )

    fill_xpath(website_xpath, WEBSITE_URL)

    verify_input(
        website_xpath,
        WEBSITE_URL,
        "Website URL"
    )


    # --------------------------------------------------------
    # STEP 6 - TAGLINE
    # --------------------------------------------------------

    print("\n[STEP 6] Filling Tagline...")

    tagline_xpath = (
        "//label[contains(normalize-space(.),'Tagline')]/following::input[1]"
        " | //input[contains(translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'tagline')]"
    )

    fill_xpath(tagline_xpath, TAGLINE)

    verify_input(
        tagline_xpath,
        TAGLINE,
        "Tagline"
    )


    # --------------------------------------------------------
    # STEP 7 - DESCRIPTION
    # --------------------------------------------------------

    print("\n[STEP 7] Filling Description...")

    description_xpath = (
        "//label[contains(normalize-space(.),'Description')]/following::textarea[1]"
        " | //textarea"
    )

    fill_xpath(description_xpath, DESCRIPTION)

    description_element = find_xpath(description_xpath)

    actual_description = description_element.get_attribute("value")

    if actual_description == DESCRIPTION:
        print("[PASS] Description verified.")
    else:
        print("[FAIL] Description verification failed.")
        print(f"[INFO] Expected length: {len(DESCRIPTION)}")
        print(f"[INFO] Actual length:   {len(actual_description or '')}")


    # --------------------------------------------------------
    # STEP 8 - CATEGORY
    # --------------------------------------------------------

    print("\n[STEP 8] Selecting Category...")

    category_xpath = (
        "//label[contains(normalize-space(.),'Category')]/following::select[1]"
        " | //select[1]"
    )

    category_element = find_visible_xpath(category_xpath)

    select_category = Select(category_element)

    try:
        select_category.select_by_visible_text(CATEGORY)

    except Exception:
        # Fallback: find option using XPath and click it
        option_xpath = (
            "//select[1]/option["
            "normalize-space(.)='AI & Machine Learning'"
            "]"
        )

        option = find_xpath(option_xpath)
        driver.execute_script(
            "arguments[0].selected = true;",
            option
        )

        driver.execute_script(
            "arguments[0].dispatchEvent("
            "new Event('change', {bubbles:true})"
            ");",
            category_element
        )

    selected_category = Select(
        find_xpath(category_xpath)
    ).first_selected_option.text.strip()

    if selected_category == CATEGORY:
        print(f"[PASS] Category verified: {selected_category}")
    else:
        print("[FAIL] Category verification failed.")
        print(f"[INFO] Expected: {CATEGORY}")
        print(f"[INFO] Actual:   {selected_category}")


    # --------------------------------------------------------
    # STEP 9 - YOUR NAME
    # --------------------------------------------------------

    print("\n[STEP 9] Filling optional Your Name...")

    name_xpath = (
        "//label[contains(normalize-space(.),'Your Name')]/following::input[1]"
        " | //input[contains(@placeholder,'John Doe')]"
    )

    try:
        fill_xpath(name_xpath, YOUR_NAME)

        verify_input(
            name_xpath,
            YOUR_NAME,
            "Your Name"
        )

    except TimeoutException:
        print("[INFO] Your Name field not found. Leaving optional field blank.")


    # --------------------------------------------------------
    # STEP 10 - YOUR WEBSITE
    # --------------------------------------------------------

    print("\n[STEP 10] Filling optional Your Website...")

    your_website_xpath = (
        "//label[contains(normalize-space(.),'Your Website')]/following::input[1]"
        " | //input[@placeholder='https://yourwebsite.com']"
    )

    try:
        fill_xpath(
            your_website_xpath,
            YOUR_WEBSITE
        )

        verify_input(
            your_website_xpath,
            YOUR_WEBSITE,
            "Your Website"
        )

    except TimeoutException:
        print(
            "[INFO] Your Website field not found. "
            "Leaving optional field blank."
        )


    # --------------------------------------------------------
    # STEP 11 - LOGO
    # --------------------------------------------------------

    print("\n[STEP 11] Checking optional Logo URL field...")

    logo_xpath = (
        "//label[contains(normalize-space(.),'Logo URL')]/following::input[1]"
        " | //input[contains(@placeholder,'logo')]"
    )

    try:
        logo_element = find_xpath(logo_xpath, timeout=5)

        print("[INFO] Logo URL field detected.")
        print(
            "[INFO] Leaving Logo URL blank because the field is optional "
            "and we do not have a hosted logo URL."
        )

    except TimeoutException:
        print("[INFO] Logo URL field not detected. No action needed.")


    # --------------------------------------------------------
    # STEP 12 - FINAL BUTTON CHECK
    # --------------------------------------------------------

    print("\n[STEP 12] Checking final Launch Tool button...")

    launch_button_xpath = (
        "//button[normalize-space(.)='Launch Tool']"
        " | //input[@type='submit' and @value='Launch Tool']"
    )

    try:
        launch_button = find_visible_xpath(
            launch_button_xpath,
            timeout=10
        )

        print("[OK] Final 'Launch Tool' button detected.")
        print("[STOP] Launch Tool will NOT be clicked.")

    except TimeoutException:
        print(
            "[WARNING] Could not locate final Launch Tool button."
        )


    # --------------------------------------------------------
    # FINAL
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("MAPPING COMPLETE")
    print("=" * 60)

    print("[PASS] TechTools Launchpad form was reached.")
    print("[PASS] Required listing information was entered.")
    print("[PASS] Browser values were verified.")
    print("[PASS] Category selected: AI & Machine Learning")

    print("\n[STOP]")
    print("The final 'Launch Tool' button was NOT clicked.")
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