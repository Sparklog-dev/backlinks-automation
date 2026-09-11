# ============================================================
# aisotools_auto.py
# AISO Tools — Y2Map submission form automation
# XPath-only Selenium selectors
# ============================================================

import time
import traceback

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# CONFIGURATION
# ============================================================

HOMEPAGE_URL = "https://aisotools.com/"
EXPECTED_SUBMIT_URL = "https://aisotools.com/submit"

TOOL_NAME = "Y2Map"

WEBSITE_URL = "https://y2map.com"

SHORT_DESCRIPTION = "Turn videos and PDFs into mind maps."

FULL_DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that "
    "transforms YouTube videos, PDFs, books, and research content "
    "into easy-to-understand visual mind maps. It helps students, "
    "researchers, educators, and lifelong learners understand "
    "complex topics faster by organizing important ideas, concepts, "
    "summaries, and related information into a structured visual format."
)

CATEGORY_VALUE = "education"
CATEGORY_TEXT = "Education & Research"

PRICING_VALUE = "free"
PRICING_TEXT = "Free"

PRICING_DETAILS = "Free to use"

FEATURES = (
    "YouTube to mind maps, "
    "PDF to mind maps, "
    "Visual learning, "
    "Knowledge organization"
)

CONTACT_EMAIL = "sparklog.marketing@gmail.com"


# ============================================================
# CHROME SETUP
# ============================================================

uc.Chrome.__del__ = lambda self: None

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def wait_for_xpath(xpath, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )


def wait_for_visible_xpath(xpath, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(
            (By.XPATH, xpath)
        )
    )


def scroll_to_element(element):
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        element
    )
    time.sleep(0.5)


def set_text_xpath(xpath, value, field_name):
    """
    Locate the field using XPath and set its value through
    the native HTML element value setter.

    This avoids characters being dropped by send_keys()
    on the AISO Tools form.
    """

    element = wait_for_visible_xpath(xpath)

    scroll_to_element(element)

    driver.execute_script(
        """
        const element = arguments[0];
        const value = arguments[1];

        if (element.tagName.toLowerCase() === 'textarea') {

            const setter = Object.getOwnPropertyDescriptor(
                HTMLTextAreaElement.prototype,
                'value'
            ).set;

            setter.call(element, value);

        } else {

            const setter = Object.getOwnPropertyDescriptor(
                HTMLInputElement.prototype,
                'value'
            ).set;

            setter.call(element, value);
        }

        element.dispatchEvent(
            new Event('input', {bubbles: true})
        );

        element.dispatchEvent(
            new Event('change', {bubbles: true})
        );
        """,
        element,
        value
    )

    time.sleep(0.7)

    actual_value = driver.execute_script(
        """
        return arguments[0].value || "";
        """,
        element
    )

    print("Value:", actual_value)

    if actual_value != value:

        print()
        print("EXPECTED:")
        print(value)

        print()
        print("ACTUAL:")
        print(actual_value)

        raise Exception(
            f"{field_name} verification failed. "
            f"Expected '{value}', got '{actual_value}'."
        )

    print(f"[PASS] {field_name} verified.")

    return element


# ============================================================
# START
# ============================================================

try:

    print()
    print("Starting Chrome...")

    driver = uc.Chrome(
        version_main=152,
        options=options
    )

    wait = WebDriverWait(driver, 20)


    # ========================================================
    # STEP 1 — OPEN HOMEPAGE
    # ========================================================

    print()
    print("STEP 1 — OPEN AISO TOOLS HOMEPAGE")

    driver.get(HOMEPAGE_URL)

    wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    time.sleep(2)

    print()
    print("[PASS] Homepage loaded.")
    print("Current URL:", driver.current_url)
    print("Page title:", driver.title)


    # ========================================================
    # STEP 2 — FIND ACTUAL SUBMIT TOOL LINK
    # ========================================================

    print()
    print("STEP 2 — FIND ACTUAL SUBMIT TOOL LINK")

    submit_links = driver.find_elements(
        By.XPATH,
        "//a[contains(normalize-space(.), 'Submit Tool')]"
    )

    print(
        "Submit Tool links found:",
        len(submit_links)
    )

    actual_submit_href = None

    for link in submit_links:

        try:

            if not link.is_displayed():
                continue

            link_text = (
                link.text or ""
            ).strip()

            href = (
                link.get_attribute("href")
                or ""
            ).strip()

            print(
                f"Link text: {link_text!r} | "
                f"Href: {href}"
            )

            if href:
                actual_submit_href = href
                break

        except Exception:
            continue


    if actual_submit_href is None:

        raise Exception(
            "Actual Submit Tool link was not found."
        )


    print()
    print(
        "[PASS] Actual submission link found:",
        actual_submit_href
    )


    # ========================================================
    # STEP 3 — OPEN SUBMISSION PAGE
    # ========================================================

    print()
    print("STEP 3 — OPEN SUBMISSION PAGE")

    driver.get(actual_submit_href)

    wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    time.sleep(2)

    print()
    print("Current URL:", driver.current_url)
    print("Page title:", driver.title)

    if (
        driver.current_url.rstrip("/")
        != EXPECTED_SUBMIT_URL.rstrip("/")
    ):

        raise Exception(
            "Unexpected submission URL. "
            f"Expected '{EXPECTED_SUBMIT_URL}', "
            f"got '{driver.current_url}'."
        )

    print("[PASS] Submission page opened.")


    # ========================================================
    # STEP 4 — TOOL NAME
    # ========================================================

    print()
    print("STEP 4 — TOOL NAME")

    tool_name_xpath = (
        "//input["
        "@placeholder='e.g., ChatGPT, Midjourney, Cursor'"
        "]"
    )

    set_text_xpath(
        tool_name_xpath,
        TOOL_NAME,
        "Tool Name"
    )


    # ========================================================
    # STEP 5 — WEBSITE URL
    # ========================================================

    print()
    print("STEP 5 — WEBSITE URL")

    website_xpath = (
        "//input["
        "@placeholder='https://yourtool.com'"
        "]"
    )

    set_text_xpath(
        website_xpath,
        WEBSITE_URL,
        "Website URL"
    )


    # ========================================================
    # STEP 6 — CATEGORY
    # ========================================================

    print()
    print("STEP 6 — CATEGORY")

    category_xpath = (
        "//select["
        ".//option[@value='education']"
        "]"
    )

    category_select = wait_for_visible_xpath(
        category_xpath
    )

    scroll_to_element(category_select)

    category_options = category_select.find_elements(
        By.XPATH,
        ".//option"
    )

    print()
    print("Available categories:")

    for option in category_options:

        try:

            print(
                f" - {option.text.strip()} "
                f"| value: "
                f"{option.get_attribute('value')}"
            )

        except Exception:
            continue


    # --------------------------------------------------------
    # Select Education & Research
    # --------------------------------------------------------

    driver.execute_script(
        """
        const select = arguments[0];
        const value = arguments[1];

        select.value = value;

        select.dispatchEvent(
            new Event('change', {bubbles: true})
        );
        """,
        category_select,
        CATEGORY_VALUE
    )

    time.sleep(1)


    selected_category_value = driver.execute_script(
        """
        const select = arguments[0];
        return select.value;
        """,
        category_select
    )


    selected_category_text = driver.execute_script(
        """
        const select = arguments[0];

        if (
            !select.selectedOptions ||
            select.selectedOptions.length === 0
        ) {
            return "";
        }

        return select.selectedOptions[0]
            .textContent
            .trim();
        """,
        category_select
    )


    print()
    print(
        "Selected category:",
        selected_category_text
    )

    print(
        "Selected category value:",
        selected_category_value
    )


    if selected_category_value != CATEGORY_VALUE:

        raise Exception(
            "Category verification failed. "
            f"Expected value '{CATEGORY_VALUE}', "
            f"got '{selected_category_value}'."
        )


    if CATEGORY_TEXT not in selected_category_text:

        raise Exception(
            "Category text verification failed. "
            f"Expected text containing '{CATEGORY_TEXT}', "
            f"got '{selected_category_text}'."
        )


    print(
        "[PASS] Category verified."
    )


    # ========================================================
    # STEP 7 — EXPAND OPTIONAL DESCRIPTION SECTION
    # ========================================================

    print()
    print(
        "STEP 7 — EXPAND DESCRIPTION / PRICING / FEATURES"
    )

    expand_xpath = (
        "//summary[contains("
        "normalize-space(.), "
        "'Write your own description'"
        ")]"
        " | "
        "//button[contains("
        "normalize-space(.), "
        "'Write your own description'"
        ")]"
    )

    expand_element = WebDriverWait(
        driver,
        10
    ).until(
        EC.element_to_be_clickable(
            (By.XPATH, expand_xpath)
        )
    )

    scroll_to_element(
        expand_element
    )

    expand_element.click()

    time.sleep(1)

    print(
        "[PASS] Description / pricing / features section expanded."
    )


    # ========================================================
    # STEP 8 — SHORT DESCRIPTION
    # ========================================================

    print()
    print("STEP 8 — SHORT DESCRIPTION")

    short_description_xpath = (
        "//input["
        "contains("
        "@placeholder,"
        "'One sentence about what your tool does'"
        ") "
        "or "
        "contains("
        "@aria-label,"
        "'Short Description'"
        ") "
        "or "
        "contains(@name,'short') "
        "or "
        "contains(@id,'short')"
        "]"
    )

    set_text_xpath(
        short_description_xpath,
        SHORT_DESCRIPTION,
        "Short Description"
    )


    # ========================================================
    # STEP 9 — FULL DESCRIPTION
    # ========================================================

    print()
    print("STEP 9 — FULL DESCRIPTION")

    full_description_xpath = (
        "//textarea["
        "preceding::*["
        "normalize-space(.)="
        "'Full Description (optional)'"
        "]"
        "]"
    )

    description_fields = driver.find_elements(
        By.XPATH,
        full_description_xpath
    )

    full_description_field = None

    for field in description_fields:

        try:

            if (
                field.is_displayed()
                and field.is_enabled()
            ):

                full_description_field = field
                break

        except Exception:
            continue


    # --------------------------------------------------------
    # Fallback: visible enabled textarea
    # --------------------------------------------------------

    if full_description_field is None:

        textareas = driver.find_elements(
            By.XPATH,
            "//textarea"
        )

        for textarea in textareas:

            try:

                if (
                    textarea.is_displayed()
                    and textarea.is_enabled()
                ):

                    full_description_field = textarea
                    break

            except Exception:
                continue


    if full_description_field is None:

        raise Exception(
            "Full Description textarea was not found."
        )


    scroll_to_element(
        full_description_field
    )


    # --------------------------------------------------------
    # Set textarea value using native JavaScript setter.
    # This prevents characters from being dropped.
    # --------------------------------------------------------

    driver.execute_script(
        """
        const element = arguments[0];
        const value = arguments[1];

        const setter = Object.getOwnPropertyDescriptor(
            HTMLTextAreaElement.prototype,
            'value'
        ).set;

        setter.call(element, value);

        element.dispatchEvent(
            new Event('input', {bubbles: true})
        );

        element.dispatchEvent(
            new Event('change', {bubbles: true})
        );
        """,
        full_description_field,
        FULL_DESCRIPTION
    )

    time.sleep(1)


    actual_description = driver.execute_script(
        """
        return arguments[0].value || "";
        """,
        full_description_field
    )


    print(
        "Value:",
        actual_description
    )


    if actual_description != FULL_DESCRIPTION:

        print()
        print("EXPECTED:")
        print(FULL_DESCRIPTION)

        print()
        print("ACTUAL:")
        print(actual_description)

        raise Exception(
            "Full Description verification failed."
        )


    print(
        "[PASS] Full Description verified."
    )


    # ========================================================
    # STEP 10 — PRICING MODEL
    # ========================================================

    print()
    print("STEP 10 — PRICING MODEL")

    pricing_xpath = (
        "//select["
        ".//option[@value='free']"
        "]"
    )

    pricing_select = wait_for_visible_xpath(
        pricing_xpath
    )

    scroll_to_element(
        pricing_select
    )

    pricing_options = pricing_select.find_elements(
        By.XPATH,
        ".//option"
    )

    print()
    print("Available pricing options:")

    for option in pricing_options:

        try:

            print(
                f" - {option.text.strip()} "
                f"| value: "
                f"{option.get_attribute('value')}"
            )

        except Exception:
            continue


    driver.execute_script(
        """
        const select = arguments[0];
        const value = arguments[1];

        select.value = value;

        select.dispatchEvent(
            new Event('change', {bubbles: true})
        );
        """,
        pricing_select,
        PRICING_VALUE
    )

    time.sleep(1)


    selected_pricing_value = driver.execute_script(
        """
        const select = arguments[0];
        return select.value;
        """,
        pricing_select
    )


    selected_pricing_text = driver.execute_script(
        """
        const select = arguments[0];

        if (
            !select.selectedOptions ||
            select.selectedOptions.length === 0
        ) {
            return "";
        }

        return select.selectedOptions[0]
            .textContent
            .trim();
        """,
        pricing_select
    )


    print()
    print(
        "Selected pricing:",
        selected_pricing_text
    )

    print(
        "Selected pricing value:",
        selected_pricing_value
    )


    if selected_pricing_value != PRICING_VALUE:

        raise Exception(
            "Pricing verification failed. "
            f"Expected value '{PRICING_VALUE}', "
            f"got '{selected_pricing_value}'."
        )


    if PRICING_TEXT not in selected_pricing_text:

        raise Exception(
            "Pricing text verification failed. "
            f"Expected text containing '{PRICING_TEXT}', "
            f"got '{selected_pricing_text}'."
        )


    print(
        "[PASS] Pricing verified."
    )


    # ========================================================
    # STEP 11 — PRICING DETAILS
    # ========================================================

    print()
    print("STEP 11 — PRICING DETAILS")

    pricing_details_xpath = (
        "//input["
        "@placeholder='e.g., Free tier available. "
        "Pro $20/mo, Team $25/user/mo'"
        "]"
    )

    set_text_xpath(
        pricing_details_xpath,
        PRICING_DETAILS,
        "Pricing Details"
    )


    # ========================================================
    # STEP 12 — KEY FEATURES
    # ========================================================

    print()
    print("STEP 12 — KEY FEATURES")

    features_xpath = (
        "//input["
        "@placeholder='e.g., AI code generation, "
        "Multi-file editing, Codebase chat'"
        "]"
    )

    set_text_xpath(
        features_xpath,
        FEATURES,
        "Key Features"
    )


    # ========================================================
    # STEP 13 — CONTACT EMAIL
    # ========================================================

    print()
    print("STEP 13 — CONTACT EMAIL")

    contact_email_xpath = (
        "//input["
        "@placeholder='you@company.com'"
        "]"
    )

    set_text_xpath(
        contact_email_xpath,
        CONTACT_EMAIL,
        "Contact Email"
    )


    # ========================================================
    # STEP 14 — FINAL FORM INSPECTION
    # ========================================================

    print()
    print("STEP 14 — FINAL FORM INSPECTION")

    print()
    print("=" * 70)
    print("FINAL VALUES")
    print("=" * 70)


    print()
    print("Tool Name:")
    print(TOOL_NAME)


    print()
    print("Website URL:")
    print(WEBSITE_URL)


    print()
    print("Category:")
    print(selected_category_text)


    print()
    print("Pricing:")
    print(selected_pricing_text)


    print()
    print("Short Description:")
    print(SHORT_DESCRIPTION)


    print()
    print("Full Description:")
    print(FULL_DESCRIPTION)


    print()
    print("Pricing Details:")
    print(PRICING_DETAILS)


    print()
    print("Key Features:")
    print(FEATURES)


    print()
    print("Contact Email:")
    print(CONTACT_EMAIL)


    print()
    print("=" * 70)


    # ========================================================
    # STEP 15 — FIND SUBMIT BUTTON
    # DO NOT CLICK
    # ========================================================

    print()
    print(
        "STEP 15 — FIND SUBMIT BUTTON "
        "(DO NOT CLICK)"
    )

    submit_buttons = driver.find_elements(
        By.XPATH,
        "//button[contains("
        "translate("
        "normalize-space(.), "
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
        "'abcdefghijklmnopqrstuvwxyz'"
        "), "
        "'submit'"
        ")]"
    )

    submit_inputs = driver.find_elements(
        By.XPATH,
        "//input[@type='submit']"
    )


    print(
        "Submit buttons found:",
        len(submit_buttons)
    )

    print(
        "Submit inputs found:",
        len(submit_inputs)
    )


    for button in submit_buttons:

        try:

            print(
                "Button text:",
                repr(button.text.strip()),
                "| enabled:",
                button.is_enabled()
            )

        except Exception:
            continue


    for submit_input in submit_inputs:

        try:

            print(
                "Submit input value:",
                repr(
                    submit_input.get_attribute(
                        "value"
                    )
                ),
                "| enabled:",
                submit_input.is_enabled()
            )

        except Exception:
            continue


    # ========================================================
    # COMPLETE
    # ========================================================

    print()
    print("=" * 70)
    print("AISO TOOLS — MAPPING COMPLETE")
    print("=" * 70)

    print()
    print("[PASS] Homepage loaded")
    print("[PASS] Actual Submit Tool link found")
    print("[PASS] Submission page opened")
    print("[PASS] Tool Name filled")
    print("[PASS] Website URL filled")
    print("[PASS] Category selected")
    print("[PASS] Category verified")
    print("[PASS] Description section expanded")
    print("[PASS] Short Description filled")
    print("[PASS] Full Description filled")
    print("[PASS] Pricing Model selected")
    print("[PASS] Pricing Details filled")
    print("[PASS] Key Features filled")
    print("[PASS] Contact Email filled")
    print("[PASS] Contact Email verified")
    print("[PASS] Submit button inspected")

    print()
    print("[STOP] Final submission was NOT clicked.")
    print()
    print("Browser will remain open for inspection.")
    print("Press ENTER to close the browser...")

    input()


except Exception as e:

    print()
    print("=" * 70)
    print("AISO TOOLS — AUTOMATION ERROR")
    print("=" * 70)

    print()
    print("Exception:", str(e))

    print()
    print("[TRACEBACK]")
    traceback.print_exc()

    print()
    print("[STOP] Browser will remain open for inspection.")

    if driver is not None:

        try:

            print(
                "Current URL:",
                driver.current_url
            )

        except Exception:
            pass

    print()
    print("Press ENTER to close the browser...")

    try:
        input()
    except Exception:
        pass