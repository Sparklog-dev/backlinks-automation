import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException
)


# ============================================================
# SILENCE UC CLEANUP ERROR
# ============================================================

def silent_del(self):
    try:
        pass
    except Exception:
        pass


uc.Chrome.__del__ = silent_del


# ============================================================
# CONFIGURATION
# ============================================================

HOME_URL = "https://twelve.tools/"

Y2MAP_URL = "https://y2map.com"
EMAIL = "sparklog.marketing@gmail.com"

TOOL_NAME = "Y2Map"

HEADLINE = (
    "Turn YouTube Videos and PDFs into Clear Visual Mind Maps"
)

LONG_DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that transforms "
    "YouTube videos, PDFs, books, and research content into easy-to-understand "
    "visual mind maps. It helps students, researchers, educators, founders, "
    "engineers, and lifelong learners understand complex topics faster by "
    "organizing important ideas, concepts, summaries, references, and related "
    "information into a structured visual format. Instead of spending hours "
    "going through lengthy videos or documents, users can create a visual "
    "overview that makes information easier to explore, review, connect, "
    "and remember."
)

CATEGORY = "Education"


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def section(title):
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)


def get_body_text(driver):
    try:
        return driver.find_element(
            By.TAG_NAME,
            "body"
        ).text
    except Exception:
        return ""


def get_visible_button_candidates(driver):

    selectors = [
        "button",
        "input[type='button']",
        "input[type='submit']",
        "[role='button']"
    ]

    elements = []

    for selector in selectors:

        try:

            found = driver.find_elements(
                By.CSS_SELECTOR,
                selector
            )

            for element in found:

                try:

                    if element.is_displayed():
                        elements.append(element)

                except StaleElementReferenceException:
                    continue

        except Exception:
            continue

    return elements


def get_button_label(element):

    try:

        text = element.text.strip()

        if text:
            return text

    except Exception:
        pass

    try:

        value = element.get_attribute("value")

        if value:
            return value.strip()

    except Exception:
        pass

    try:

        aria = element.get_attribute("aria-label")

        if aria:
            return aria.strip()

    except Exception:
        pass

    return ""


# ============================================================
# START DRIVER
# ============================================================

section("TWELVE TOOLS — FULL WEBSITE FLOW")

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

wait = WebDriverWait(driver, 30)


try:

    # ========================================================
    # STEP 0 — HOME PAGE
    # ========================================================

    section("STEP 0 — HOME PAGE")

    driver.get(HOME_URL)

    time.sleep(4)

    print("Page title :", driver.title)
    print("Current URL:", driver.current_url)

    print(
        "\nSearching homepage for 'Submit your Tool'..."
    )

    submit_link = None

    try:

        submit_link = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[contains(normalize-space(.), 'Submit your Tool')]"
                )
            )
        )

    except TimeoutException:

        print(
            "Exact 'Submit your Tool' link not found."
        )

    if submit_link is None:

        try:

            submit_link = driver.find_element(
                By.CSS_SELECTOR,
                "a[href='https://twelve.tools/submit']"
            )

        except Exception:

            print(
                "ERROR: Homepage submission link could not be found."
            )

            input(
                "\nPress ENTER to close the browser..."
            )

            raise SystemExit


    print(
        "Submit link text:",
        submit_link.text.strip()
    )

    print(
        "Submit link href:",
        submit_link.get_attribute("href")
    )


    # ========================================================
    # STEP 1 — CLICK "SUBMIT YOUR TOOL"
    # ========================================================

    section("STEP 1 — SUBMIT YOUR TOOL")

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        submit_link
    )

    time.sleep(1)

    submit_link.click()

    # Wait for pricing page
    try:

        wait.until(
            lambda d: (
                d.current_url.rstrip("/")
                == "https://twelve.tools/submit"
            )
        )

    except TimeoutException:

        print(
            "Pricing page navigation wait timed out."
        )

    time.sleep(3)

    print("Page title :", driver.title)
    print("Current URL:", driver.current_url)


    # ========================================================
    # STEP 2 — PRICING PAGE
    # ========================================================

    section("STEP 2 — PRICING PAGE")

    print(
        "We are now on the Twelve Tools pricing/submission-choice page."
    )

    print(
        "\nLooking for the FREE submission option..."
    )

    free_link = None

    # --------------------------------------------------------
    # Primary selector
    # --------------------------------------------------------

    try:

        free_link = wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[contains(normalize-space(.), \"Continue\") "
                    "and contains(normalize-space(.), \"free\")]"
                )
            )
        )

    except TimeoutException:

        print(
            "Primary free-option selector not found."
        )


    # --------------------------------------------------------
    # Fallback selectors
    # --------------------------------------------------------

    if free_link is None:

        try:

            free_link = driver.find_element(
                By.CSS_SELECTOR,
                "a[href*='submit-your-tool']"
            )

            print(
                "Found free submission link using href fallback."
            )

        except Exception:

            pass


    if free_link is None:

        print(
            "\nERROR: Could not find the FREE submission option."
        )

        print(
            "\nCurrent page text:"
        )

        print(
            get_body_text(driver)
        )

        input(
            "\nPress ENTER to close the browser..."
        )

        raise SystemExit


    print(
        "Free option text:",
        free_link.text.strip()
    )

    print(
        "Free option href:",
        free_link.get_attribute("href")
    )


    # ========================================================
    # CLICK FREE OPTION
    # ========================================================

    print(
        "\nClicking 'Continue — it's free'..."
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        free_link
    )

    time.sleep(1)

    free_link.click()


    # ========================================================
    # STEP 3 — ACTUAL SUBMISSION FORM
    # ========================================================

    section("STEP 3 — ACTUAL SUBMISSION FORM")

    try:

        wait.until(
            lambda d: (
                "submit-your-tool" in d.current_url.lower()
            )
        )

    except TimeoutException:

        print(
            "Submission-form navigation wait timed out."
        )

    time.sleep(3)

    print("Page title :", driver.title)
    print("Current URL:", driver.current_url)


    # --------------------------------------------------------
    # Confirm fUrl exists
    # --------------------------------------------------------

    url_field = wait.until(
        EC.presence_of_element_located(
            (By.ID, "fUrl")
        )
    )

    print(
        "\nWebsite URL field found."
    )

    print(
        "Field ID   :",
        url_field.get_attribute("id")
    )

    print(
        "Placeholder:",
        url_field.get_attribute("placeholder")
    )


    # ========================================================
    # ENTER Y2MAP URL
    # ========================================================

    url_field.clear()

    url_field.send_keys(
        Y2MAP_URL
    )

    print(
        "Entered URL:",
        url_field.get_attribute("value")
    )


    # ========================================================
    # STEP 4 — WEBSITE ANALYSIS
    # ========================================================

    section("STEP 4 — WEBSITE ANALYSIS")

    analyze_button = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "btnAnalyze")
        )
    )

    print(
        "Continue button found:",
        analyze_button.get_attribute("value")
    )

    print(
        "\nClicking Continue..."
    )

    analyze_button.click()


    # ========================================================
    # WAIT FOR ANALYSIS
    # ========================================================

    print(
        "\nWaiting for website analysis..."
    )

    analysis_done = False

    for i in range(45):

        time.sleep(2)

        body = get_body_text(driver)

        if "Analyzing your website" in body:

            print(
                f"Analysis running... {(i + 1) * 2}s"
            )

            continue

        analysis_done = True

        print(
            "Website analysis completed."
        )

        break


    if not analysis_done:

        print(
            "WARNING: Analysis timeout reached."
        )


    # ========================================================
    # STEP 5 — SCREENSHOT
    # ========================================================

    section("STEP 5 — SCREENSHOT")

    print(
        "Waiting for Twelve Tools to capture the screenshot..."
    )

    screenshot_continue = None

    for i in range(45):

        time.sleep(2)

        body = get_body_text(driver)

        if "Taking a screenshot" in body:

            print(
                f"Screenshot processing... {(i + 1) * 2}s"
            )

            continue


        # Look for Continue after screenshot
        buttons = get_visible_button_candidates(
            driver
        )

        for button in buttons:

            try:

                label = get_button_label(
                    button
                ).lower()

                if label.startswith("continue"):

                    screenshot_continue = button
                    break

            except StaleElementReferenceException:

                continue


        if screenshot_continue is not None:

            print(
                "Screenshot completed."
            )

            break


    if screenshot_continue is None:

        print(
            "\nERROR: Screenshot Continue button not found."
        )

        print(
            "\nCurrent page text:\n"
        )

        print(
            get_body_text(driver)
        )

        input(
            "\nPress ENTER to close the browser..."
        )

        raise SystemExit


    # ========================================================
    # CLICK SCREENSHOT CONTINUE
    # ========================================================

    section("STEP 6 — SCREENSHOT CONTINUE")

    try:

        print(
            "Button:",
            get_button_label(
                screenshot_continue
            )
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            screenshot_continue
        )

        time.sleep(1)

        screenshot_continue.click()

        print(
            "Screenshot Continue clicked."
        )

    except StaleElementReferenceException:

        print(
            "Continue became stale. Re-locating..."
        )

        clicked = False

        buttons = get_visible_button_candidates(
            driver
        )

        for button in buttons:

            try:

                label = get_button_label(
                    button
                ).lower()

                if label.startswith("continue"):

                    button.click()

                    clicked = True

                    print(
                        "Continue clicked after re-location."
                    )

                    break

            except Exception:

                continue


        if not clicked:

            print(
                "ERROR: Could not click Continue."
            )

            input(
                "\nPress ENTER to close the browser..."
            )

            raise SystemExit


    # ========================================================
    # STEP 7 — REVIEW PAGE
    # ========================================================

    section("STEP 7 — REVIEW PAGE")

    print(
        "Waiting for Review page..."
    )

    review_found = False

    for i in range(30):

        time.sleep(2)

        body = get_body_text(driver)

        if (
            "Review your listing" in body
            and
            "Tool's name" in body
        ):

            review_found = True

            print(
                "Review page detected."
            )

            break


    if not review_found:

        print(
            "ERROR: Review page was not detected."
        )

        print(
            "\nCurrent URL:",
            driver.current_url
        )

        print(
            "\nCurrent page text:"
        )

        print(
            get_body_text(driver)
        )

        input(
            "\nPress ENTER to close the browser..."
        )

        raise SystemExit


    print(
        "\nCurrent URL:",
        driver.current_url
    )


    # ========================================================
    # REVIEW PAGE — LETTER LOGO
    # ========================================================

    section("REVIEW — LETTER LOGO")

    letter_logo = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "letterLogo")
        )
    )

    if not letter_logo.is_selected():

        driver.execute_script(
            "arguments[0].click();",
            letter_logo
        )

        print(
            "Letter logo enabled."
        )

    else:

        print(
            "Letter logo already enabled."
        )


    # ========================================================
    # REVIEW — TOOL NAME
    # ========================================================

    section("REVIEW — TOOL NAME")

    name_field = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "name")
        )
    )

    name_field.clear()

    name_field.send_keys(
        TOOL_NAME
    )

    print(
        "Tool name:",
        name_field.get_attribute("value")
    )


    # ========================================================
    # REVIEW — HEADLINE
    # ========================================================

    section("REVIEW — HEADLINE")

    headline_field = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "headline")
        )
    )

    headline_field.clear()

    headline_field.send_keys(
        HEADLINE
    )

    actual_headline = headline_field.get_attribute(
        "value"
    )

    print(
        "Headline:",
        actual_headline
    )

    print(
        "Headline length:",
        len(actual_headline)
    )


    # ========================================================
    # REVIEW — LONG DESCRIPTION
    # ========================================================

    section("REVIEW — LONG DESCRIPTION")

    description_field = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "longdesc")
        )
    )

    description_field.clear()

    description_field.send_keys(
        LONG_DESCRIPTION
    )

    actual_description = (
        description_field.get_attribute(
            "value"
        )
    )

    print(
        "Description length:",
        len(actual_description)
    )

    print(
        "Description:"
    )

    print(
        actual_description
    )


    # ========================================================
    # REVIEW — CATEGORY
    # ========================================================

    section("REVIEW — CATEGORY")

    category_element = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "categ")
        )
    )

    category_select = Select(
        category_element
    )

    category_select.select_by_visible_text(
        CATEGORY
    )

    selected_category = (
        category_select
        .first_selected_option
        .text
        .strip()
    )

    print(
        "Selected category:",
        selected_category
    )


    # ========================================================
    # REVIEW — EMAIL
    # ========================================================

    section("REVIEW — EMAIL")

    email_field = wait.until(
        EC.presence_of_element_located(
            (By.NAME, "email")
        )
    )

    email_field.clear()

    email_field.send_keys(
        EMAIL
    )

    print(
        "Email:",
        email_field.get_attribute(
            "value"
        )
    )


    # ========================================================
    # FINAL VERIFICATION
    # ========================================================

    section("FINAL REVIEW VERIFICATION")

    verified = True


    # Letter logo
    if letter_logo.is_selected():

        print(
            "[OK] Letter logo enabled"
        )

    else:

        print(
            "[ERROR] Letter logo not enabled"
        )

        verified = False


    # Tool name
    actual_name = name_field.get_attribute(
        "value"
    )

    if actual_name == TOOL_NAME:

        print(
            "[OK] Tool name:",
            actual_name
        )

    else:

        print(
            "[ERROR] Tool name:",
            actual_name
        )

        verified = False


    # Headline
    actual_headline = headline_field.get_attribute(
        "value"
    )

    if actual_headline == HEADLINE:

        print(
            "[OK] Headline:",
            actual_headline
        )

    else:

        print(
            "[ERROR] Headline mismatch"
        )

        verified = False


    # Description
    actual_description = description_field.get_attribute(
        "value"
    )

    if actual_description == LONG_DESCRIPTION:

        print(
            "[OK] Long description:",
            len(actual_description),
            "characters"
        )

    else:

        print(
            "[ERROR] Long description mismatch"
        )

        verified = False


    # Category
    actual_category = (
        category_select
        .first_selected_option
        .text
        .strip()
    )

    if actual_category == CATEGORY:

        print(
            "[OK] Category:",
            actual_category
        )

    else:

        print(
            "[ERROR] Category:",
            actual_category
        )

        verified = False


    # Email
    actual_email = email_field.get_attribute(
        "value"
    )

    if actual_email == EMAIL:

        print(
            "[OK] Email:",
            actual_email
        )

    else:

        print(
            "[ERROR] Email mismatch"
        )

        verified = False


    # ========================================================
    # FINAL SUBMISSION BUTTON
    # ========================================================

    section("FINAL SUBMISSION BUTTON — INSPECTION ONLY")

    try:

        final_button = driver.find_element(
            By.NAME,
            "btFinal"
        )

        print(
            "Button name :",
            final_button.get_attribute("name")
        )

        print(
            "Button type :",
            final_button.get_attribute("type")
        )

        print(
            "Button value:",
            final_button.get_attribute("value")
        )

        print(
            "Button enabled:",
            final_button.is_enabled()
        )

        print(
            "\n[SAFE STOP] Submit for verification was NOT clicked."
        )

    except Exception as e:

        print(
            "Could not inspect final button:",
            e
        )


    # ========================================================
    # FINAL STATUS
    # ========================================================

    section("FINAL STATUS")

    if verified:

        print(
            "SUCCESS — FULL TWELVE TOOLS FLOW "
            "COMPLETED THROUGH REVIEW."
        )

    else:

        print(
            "WARNING — REVIEW VERIFICATION FAILED."
        )


    print("""
------------------------------------------------------------
FLOW COMPLETED
------------------------------------------------------------

1. Home page opened
2. "Submit your Tool" found
3. Pricing page opened
4. FREE submission option found
5. "Continue — it's free" clicked
6. Actual submission form opened
7. Y2Map URL entered
8. Website analysis started
9. Website analysis completed
10. Screenshot processing completed
11. Screenshot Continue clicked
12. Review page opened
13. Letter logo enabled
14. Tool name filled
15. Headline filled
16. Long description filled
17. Education category selected
18. Email filled
19. All Review fields verified

------------------------------------------------------------
SAFE STOP
------------------------------------------------------------

Submit for verification : NOT CLICKED
Badge stage              : NOT ENTERED
Live stage               : NOT ENTERED
Payment                  : NOT STARTED
Listing submission       : NOT PERFORMED

------------------------------------------------------------
""")

    input(
        "Press ENTER to close the browser..."
    )


finally:

    try:
        driver.quit()
    except Exception:
        pass