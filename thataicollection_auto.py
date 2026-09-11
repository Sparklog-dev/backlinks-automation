import time
import traceback
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# THAT AI COLLECTION — FORM MAPPING + FILLING
# XPath-only Selenium version
# ============================================================

URL = "https://thataicollection.com/submit/details/"

PROJECT_NAME = "Y2Map"
WEBSITE = "https://y2map.com"

CATEGORY = "Note Taking & Second Brain"

SHORT_TITLE = "Y2Map - AI Mind Maps for YouTube Videos and PDFs"

LONG_DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that transforms "
    "YouTube videos, PDFs, books, and research content into easy-to-understand "
    "visual mind maps. It helps students, researchers, educators, and lifelong "
    "learners organize complex information, understand key ideas faster, and "
    "create structured visual overviews that make learning and reviewing easier."
)


# ============================================================
# SILENCE undetected_chromedriver CLEANUP ERROR
# ============================================================

def silent_del(self):
    pass


uc.Chrome.__del__ = silent_del


# ============================================================
# BROWSER SETUP
# ============================================================

options = uc.ChromeOptions()

driver = uc.Chrome(
    version_main=152,
    options=options
)

wait = WebDriverWait(driver, 20)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def visible_xpath(xpath, timeout=20):
    """
    Wait for a visible element using XPath only.
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(
            (By.XPATH, xpath)
        )
    )


def clickable_xpath(xpath, timeout=20):
    """
    Wait for a clickable element using XPath only.
    """
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath)
        )
    )


def get_value(element):
    """
    Read actual browser value.
    """
    return element.get_attribute("value") or ""


def get_text(element):
    """
    Read visible text safely.
    """
    return (element.text or "").strip()


def verify_value(label, element, expected):
    """
    Verify actual browser field value.
    """
    actual = get_value(element)

    if actual != expected:
        raise Exception(
            f"{label} verification failed.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )

    print(f"[PASS] {label}: {actual}")


# ============================================================
# MAIN WORKFLOW
# ============================================================

try:

    print("\n" + "=" * 90)
    print("THAT AI COLLECTION — FORM MAPPING + FILLING")
    print("XPath-only version")
    print("=" * 90)


    # --------------------------------------------------------
    # STEP 1 — OPEN PAGE
    # --------------------------------------------------------

    print("\n" + "-" * 90)
    print("STEP 1 — OPEN SUBMISSION PAGE")
    print("-" * 90)

    driver.get(URL)

    time.sleep(4)

    print("Page title :", driver.title)
    print("Current URL:", driver.current_url)

    if "thataicollection.com" not in driver.current_url:
        raise Exception(
            "Unexpected URL detected. "
            "The browser did not open the expected That AI Collection page."
        )

    print("[PASS] Submission page opened.")


    # --------------------------------------------------------
    # STEP 2 — TOOL NAME
    # --------------------------------------------------------

    print("\n" + "-" * 90)
    print("STEP 2 — TOOL NAME")
    print("-" * 90)

    name_xpath = (
        "//input[@id='application-name']"
    )

    name_field = visible_xpath(name_xpath)

    name_field.click()
    name_field.clear()
    name_field.send_keys(PROJECT_NAME)

    print("XPath:", name_xpath)
    print("Value:", get_value(name_field))


    # --------------------------------------------------------
    # STEP 3 — WEBSITE URL
    # --------------------------------------------------------

    print("\n" + "-" * 90)
    print("STEP 3 — WEBSITE URL")
    print("-" * 90)

    website_xpath = (
        "//input[@id='application-url']"
    )

    website_field = visible_xpath(website_xpath)

    website_field.click()
    website_field.clear()
    website_field.send_keys(WEBSITE)

    print("XPath:", website_xpath)
    print("Value:", get_value(website_field))


    # --------------------------------------------------------
    # STEP 4 — FIND VISIBLE TEXTAREAS
    # --------------------------------------------------------

    print("\n" + "-" * 90)
    print("STEP 4 — TEXTAREAS")
    print("-" * 90)

    textarea_xpath = (
        "//textarea[not(ancestor-or-self::*["
        "contains(@style,'display:none')"
        "])]"
    )

    all_textareas = driver.find_elements(
        By.XPATH,
        textarea_xpath
    )

    visible_textareas = [
        textarea
        for textarea in all_textareas
        if textarea.is_displayed()
    ]

    print("Visible textareas found:", len(visible_textareas))

    if len(visible_textareas) < 2:
        raise Exception(
            "Expected at least 2 visible textareas, "
            f"but found {len(visible_textareas)}."
        )

    print("[PASS] At least 2 visible textareas detected.")


    # --------------------------------------------------------
    # STEP 5 — SHORT TITLE
    # --------------------------------------------------------

    print("\n" + "-" * 90)
    print("STEP 5 — SHORT TITLE")
    print("-" * 90)

    short_title_field = visible_textareas[0]

    short_title_field.click()
    short_title_field.clear()
    short_title_field.send_keys(SHORT_TITLE)

    print("Textarea XPath:", textarea_xpath)
    print("Position:", 1)
    print("Placeholder:",
          short_title_field.get_attribute("placeholder"))
    print("Value:",
          get_value(short_title_field))


    # --------------------------------------------------------
    # STEP 6 — LONG DESCRIPTION
    # --------------------------------------------------------

    print("\n" + "-" * 90)
    print("STEP 6 — LONG DESCRIPTION")
    print("-" * 90)

    long_description_field = visible_textareas[1]

    long_description_field.click()
    long_description_field.clear()
    long_description_field.send_keys(LONG_DESCRIPTION)

    long_value = get_value(long_description_field)

    print("Textarea XPath:", textarea_xpath)
    print("Position:", 2)
    print("Placeholder:",
          long_description_field.get_attribute("placeholder"))
    print("Character count:",
          len(long_value))


    # --------------------------------------------------------
    # STEP 7 — CATEGORY DROPDOWN
    # --------------------------------------------------------

    print("\n" + "-" * 90)
    print("STEP 7 — CATEGORY")
    print("-" * 90)

    category_button_xpath = (
        "//button[@id='dropdownDefaultButton']"
    )

    category_button = clickable_xpath(
        category_button_xpath
    )

    print("Category button found.")
    print("Before selection:",
          get_text(category_button))

    category_button.click()

    time.sleep(1)

    print("[PASS] Category dropdown opened.")


    # --------------------------------------------------------
    # STEP 8 — INSPECT CATEGORY OPTIONS
    # --------------------------------------------------------

    print("\n" + "-" * 90)
    print("STEP 8 — CATEGORY OPTIONS")
    print("-" * 90)

    category_option_xpath = (
        "//*[self::button or self::a or self::li or "
        "self::div][normalize-space(.)="
        f"'{CATEGORY}']"
    )

    category_options = driver.find_elements(
        By.XPATH,
        category_option_xpath
    )

    visible_category_options = [
        option
        for option in category_options
        if option.is_displayed()
    ]

    print(
        "Visible exact category matches:",
        len(visible_category_options)
    )

    category_selected = False

    if visible_category_options:

        for option in visible_category_options:

            print(
                "Candidate:",
                repr(get_text(option)),
                "| TAG:",
                option.tag_name
            )

            try:

                driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    option
                )

                time.sleep(0.5)

                option.click()

                category_selected = True

                print(
                    "[PASS] Category selected:",
                    get_text(option)
                )

                break

            except Exception as click_error:

                print(
                    "[WARN] Category candidate click failed:",
                    click_error
                )


    # --------------------------------------------------------
    # CATEGORY FALLBACK
    # --------------------------------------------------------

    if not category_selected:

        print("\nExact option click did not succeed.")
        print("Inspecting visible dropdown elements...")

        broad_category_xpath = (
            "//*[contains("
            "translate(normalize-space(.),"
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            "'abcdefghijklmnopqrstuvwxyz'),"
            "'note taking'"
            ")]"
        )

        possible_elements = driver.find_elements(
            By.XPATH,
            broad_category_xpath
        )

        visible_possible_elements = [
            element
            for element in possible_elements
            if element.is_displayed()
        ]

        print(
            "Visible elements containing 'Note Taking':",
            len(visible_possible_elements)
        )

        for index, element in enumerate(
            visible_possible_elements,
            start=1
        ):

            print(
                f"[{index}]",
                "TAG=",
                element.tag_name,
                "TEXT=",
                repr(get_text(element))
            )

        for element in visible_possible_elements:

            element_text = get_text(element)

            if CATEGORY.lower() in element_text.lower():

                try:

                    driver.execute_script(
                        "arguments[0].scrollIntoView({block:'center'});",
                        element
                    )

                    time.sleep(0.5)

                    element.click()

                    category_selected = True

                    print(
                        "[PASS] Category selected using fallback:"
                    )
                    print(
                        "      ",
                        element_text
                    )

                    break

                except Exception as click_error:

                    print(
                        "[WARN] Fallback click failed:",
                        click_error
                    )


    if not category_selected:

        raise Exception(
            "CATEGORY SELECTION FAILED.\n"
            f"Could not select: {CATEGORY}\n"
            "No submission was attempted."
        )


    time.sleep(1)


    # --------------------------------------------------------
    # STEP 9 — CATEGORY VERIFICATION
    # --------------------------------------------------------

    print("\n" + "-" * 90)
    print("STEP 9 — CATEGORY VERIFICATION")
    print("-" * 90)

    category_after_xpath = (
        "//button[@id='dropdownDefaultButton']"
    )

    category_button_after = visible_xpath(
        category_after_xpath
    )

    actual_category = get_text(
        category_button_after
    )

    print("Actual category button text:",
          repr(actual_category))

    if CATEGORY.lower() not in actual_category.lower():

        # Some dropdowns may not update the button text.
        # In that case inspect selected/active elements.
        selected_xpath = (
            "//*[@aria-selected='true' and "
            "normalize-space(.)="
            f"'{CATEGORY}']"
        )

        selected_elements = driver.find_elements(
            By.XPATH,
            selected_xpath
        )

        visible_selected = [
            element
            for element in selected_elements
            if element.is_displayed()
        ]

        if not visible_selected:

            raise Exception(
                "Category was clicked but could not be verified.\n"
                f"Expected category: {CATEGORY}\n"
                f"Button text: {actual_category}"
            )

        print(
            "[PASS] Category verified through aria-selected."
        )

    else:

        print(
            "[PASS] Category verified:",
            actual_category
        )


    # --------------------------------------------------------
    # STEP 10 — FINAL FORM VALUE VERIFICATION
    # --------------------------------------------------------

    print("\n" + "=" * 90)
    print("STEP 10 — FINAL FORM VALUE VERIFICATION")
    print("=" * 90)

    print("\nChecking actual browser values...\n")

    # Re-locate fields using XPath rather than relying only
    # on previous WebElement references.

    final_name_field = visible_xpath(
        "//input[@id='application-name']"
    )

    final_website_field = visible_xpath(
        "//input[@id='application-url']"
    )

    verify_value(
        "Tool Name",
        final_name_field,
        PROJECT_NAME
    )

    verify_value(
        "Website",
        final_website_field,
        WEBSITE
    )


    # Re-read visible textareas.
    final_textareas = driver.find_elements(
        By.XPATH,
        textarea_xpath
    )

    final_visible_textareas = [
        textarea
        for textarea in final_textareas
        if textarea.is_displayed()
    ]

    if len(final_visible_textareas) < 2:
        raise Exception(
            "Final verification could not find "
            "the expected 2 visible textareas."
        )

    final_short_title = final_visible_textareas[0]
    final_long_description = final_visible_textareas[1]

    verify_value(
        "Short Title",
        final_short_title,
        SHORT_TITLE
    )

    actual_long_description = get_value(
        final_long_description
    )

    if actual_long_description != LONG_DESCRIPTION:

        raise Exception(
            "Long Description verification failed.\n"
            f"Expected length: {len(LONG_DESCRIPTION)}\n"
            f"Actual length:   {len(actual_long_description)}"
        )

    print(
        "[PASS] Long Description:",
        len(actual_long_description),
        "characters"
    )

    print(
        "[PASS] Long Description content verified."
    )


    # --------------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------------

    print("\n" + "=" * 90)
    print("THAT AI COLLECTION — MAPPING COMPLETE")
    print("=" * 90)

    print("\nTool Name:")
    print(" ", get_value(final_name_field))

    print("\nWebsite:")
    print(" ", get_value(final_website_field))

    print("\nShort Title:")
    print(" ", get_value(final_short_title))

    print("\nLong Description:")
    print(" ", actual_long_description)

    print("\nCategory:")
    print(" ", actual_category)

    print("\n" + "=" * 90)
    print("STOP — NO SUBMISSION")
    print("=" * 90)

    print("\n[STOP] No Next button clicked.")
    print("[STOP] No Submit button clicked.")
    print("[STOP] No form submission performed.")
    print("[STOP] Browser remains open for manual inspection.")

    input("\nPress ENTER to close the browser...")


except Exception as error:

    print("\n" + "=" * 90)
    print("ERROR — SCRIPT STOPPED")
    print("=" * 90)

    print("\nError type:")
    print(type(error).__name__)

    print("\nError message:")
    print(str(error))

    print("\nFull traceback:")
    traceback.print_exc()

    print("\n" + "=" * 90)
    print("IMPORTANT")
    print("=" * 90)

    print("The browser will remain open.")
    print("No submission will be attempted.")
    print("Inspect the page before making any changes.")

    input("\nPress ENTER to close the browser...")


finally:

    try:
        driver.quit()
    except Exception:
        pass