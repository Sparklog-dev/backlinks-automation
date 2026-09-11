import time
import traceback

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# THE NEXT AI — FORM MAPPING + FILLING
# XPath-only Selenium version
# NO SUBMISSION
# ============================================================


# ============================================================
# Y2MAP DATA
# ============================================================

TOOL_NAME = "Y2Map"

WEBSITE_URL = "https://y2map.com"

SHORT_DESCRIPTION = (
    "Turn YouTube videos and PDFs into clear visual mind maps."
)

FULL_DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that transforms "
    "YouTube videos, PDFs, books, and research content into easy-to-understand "
    "visual mind maps. It helps students, researchers, educators, founders, "
    "engineers, and lifelong learners understand complex topics faster by "
    "organizing important ideas, concepts, summaries, references, and related "
    "information into a structured visual format. Instead of spending hours "
    "going through lengthy videos or documents, users can create a visual "
    "overview that makes information easier to explore, review, connect, and "
    "remember."
)

EMAIL = "sparklog.marketing@gmail.com"

TAGS = (
    "AI, Mind Maps, YouTube, PDF, Education, Learning, "
    "Knowledge Management, Productivity"
)


# ============================================================
# SILENCE undetected_chromedriver CLEANUP MESSAGE
# ============================================================

def silent_del(self):
    pass


uc.Chrome.__del__ = silent_del


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def wait_for_element(driver, xpath, timeout=20):
    """
    Wait for an element using XPath only.
    """
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )


def wait_for_visible(driver, xpath, timeout=20):
    """
    Wait for a visible element using XPath only.
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(
            (By.XPATH, xpath)
        )
    )


def wait_for_clickable(driver, xpath, timeout=20):
    """
    Wait for a clickable element using XPath only.
    """
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath)
        )
    )


def fill_input(driver, xpath, text):
    """
    Fill a normal input/textarea using XPath only.
    """
    element = wait_for_visible(driver, xpath)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )

    time.sleep(0.3)

    element.click()
    element.clear()
    element.send_keys(text)

    return element


def select_dropdown(driver, xpath, visible_text):
    """
    Select an HTML <select> using an XPath-located element.
    """
    element = wait_for_visible(driver, xpath)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )

    time.sleep(0.3)

    select = Select(element)

    try:
        select.select_by_visible_text(visible_text)

    except Exception:

        matched = False

        for option in select.options:

            option_text = (
                option.text or ""
            ).strip()

            if visible_text.lower() in option_text.lower():

                select.select_by_value(
                    option.get_attribute("value")
                )

                matched = True
                break

        if not matched:
            raise Exception(
                f"Could not select dropdown option: "
                f"{visible_text}"
            )

    return element


def actual_value(element):
    """
    Read the actual value from an input/select/textarea.
    """
    return element.get_attribute("value") or ""


def verify_value(label, element, expected):
    """
    Verify actual browser value.
    """
    actual = actual_value(element)

    if actual != expected:
        raise Exception(
            f"{label} verification failed.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )

    print(f"[PASS] {label}: {actual}")


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n" + "=" * 90)
    print("THE NEXT AI — Y2MAP SUBMISSION MAPPING")
    print("XPath-only version")
    print("=" * 90)


    options = uc.ChromeOptions()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    driver = uc.Chrome(
        version_main=152,
        options=options
    )

    try:

        # ====================================================
        # STEP 1 — OPEN HOMEPAGE
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 1 — OPEN THE NEXT AI HOMEPAGE")
        print("-" * 90)

        driver.get(
            "https://www.thenextai.com/"
        )

        time.sleep(4)

        print("Page title :", driver.title)
        print("Current URL:", driver.current_url)

        if "thenextai.com" not in driver.current_url:

            raise Exception(
                "Unexpected homepage URL."
            )

        print("[PASS] Homepage opened.")


        # ====================================================
        # STEP 2 — FIND ACTUAL SUBMIT TOOL LINK
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 2 — FIND ACTUAL SUBMIT TOOL LINK")
        print("-" * 90)

        submit_link_xpath = (
            "//a[contains("
            "translate(normalize-space(.),"
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
            "'abcdefghijklmnopqrstuvwxyz'),"
            "'submit tool'"
            ")]"
        )

        submit_links = driver.find_elements(
            By.XPATH,
            submit_link_xpath
        )

        visible_submit_links = [
            link
            for link in submit_links
            if link.is_displayed()
        ]

        print(
            "Visible Submit Tool links found:",
            len(visible_submit_links)
        )

        if not visible_submit_links:

            raise Exception(
                "Could not find the actual "
                "'Submit Tool' link on the homepage."
            )

        submit_link = visible_submit_links[0]

        print(
            "Link text:",
            repr(submit_link.text)
        )

        print(
            "Href:",
            submit_link.get_attribute("href")
        )

        print("[PASS] Submission link found.")


        # ====================================================
        # STEP 3 — CLICK ACTUAL SUBMIT LINK
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 3 — OPEN SUBMISSION FORM")
        print("-" * 90)

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            submit_link
        )

        time.sleep(0.5)

        submit_link.click()

        time.sleep(4)

        print("Current URL:", driver.current_url)
        print("Page title :", driver.title)

        if "/submit-ai-tool/" not in driver.current_url:

            print(
                "[WARN] Submission URL does not contain "
                "'/submit-ai-tool/'."
            )

        else:

            print(
                "[PASS] Actual submission page opened."
            )


        # ====================================================
        # STEP 4 — CHECK FORM
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 4 — CHECK SUBMISSION FORM")
        print("-" * 90)

        name_xpath = (
            "//input[@id='f-name']"
        )

        name_field = wait_for_visible(
            driver,
            name_xpath
        )

        print(
            "Tool Name field found."
        )

        print("[PASS] Submission form detected.")


        # ====================================================
        # STEP 5 — TOOL NAME
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 5 — TOOL NAME")
        print("-" * 90)

        fill_input(
            driver,
            name_xpath,
            TOOL_NAME
        )

        print(
            "Value:",
            actual_value(name_field)
        )


        # ====================================================
        # STEP 6 — WEBSITE
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 6 — WEBSITE URL")
        print("-" * 90)

        website_xpath = (
            "//input[@id='f-url']"
        )

        website_field = fill_input(
            driver,
            website_xpath,
            WEBSITE_URL
        )

        print(
            "Value:",
            actual_value(website_field)
        )


        # ====================================================
        # STEP 7 — CATEGORY
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 7 — CATEGORY")
        print("-" * 90)

        category_xpath = (
            "//select[@id='f-cat']"
        )

        category_field = select_dropdown(
            driver,
            category_xpath,
            "🎓 Education"
        )

        selected_category = Select(
            category_field
        ).first_selected_option.text.strip()

        print(
            "Selected category:",
            selected_category
        )

        if "education" not in selected_category.lower():

            raise Exception(
                "Category verification failed.\n"
                f"Expected: Education\n"
                f"Actual: {selected_category}"
            )

        print(
            "[PASS] Category: Education"
        )


        # ====================================================
        # STEP 8 — PRICING
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 8 — PRICING MODEL")
        print("-" * 90)

        pricing_xpath = (
            "//select[@id='f-pricing']"
        )

        pricing_field = select_dropdown(
            driver,
            pricing_xpath,
            "Free"
        )

        selected_pricing = Select(
            pricing_field
        ).first_selected_option.text.strip()

        print(
            "Selected pricing:",
            selected_pricing
        )

        if selected_pricing.lower() != "free":

            raise Exception(
                "Pricing verification failed.\n"
                f"Expected: Free\n"
                f"Actual: {selected_pricing}"
            )

        print(
            "[PASS] Pricing: Free"
        )


        # ====================================================
        # STEP 9 — SHORT DESCRIPTION
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 9 — SHORT DESCRIPTION")
        print("-" * 90)

        short_xpath = (
            "//input[@id='f-short']"
        )

        short_field = fill_input(
            driver,
            short_xpath,
            SHORT_DESCRIPTION
        )

        print(
            "Character count:",
            len(actual_value(short_field))
        )

        print(
            "Value:",
            actual_value(short_field)
        )

        if len(SHORT_DESCRIPTION) > 120:

            raise Exception(
                "Short description exceeds the "
                "current 120-character limit."
            )

        print(
            "[PASS] Short Description"
        )


        # ====================================================
        # STEP 10 — FULL DESCRIPTION
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 10 — FULL DESCRIPTION")
        print("-" * 90)

        description_xpath = (
            "//textarea[@id='f-desc']"
        )

        description_field = fill_input(
            driver,
            description_xpath,
            FULL_DESCRIPTION
        )

        print(
            "Character count:",
            len(actual_value(description_field))
        )

        print(
            "[PASS] Full Description"
        )


        # ====================================================
        # STEP 11 — LOGO URL
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 11 — LOGO URL")
        print("-" * 90)

        logo_xpath = (
            "//input[@id='f-logo']"
        )

        logo_field = wait_for_visible(
            driver,
            logo_xpath
        )

        print(
            "Logo URL field found."
        )

        print(
            "Current value:",
            repr(actual_value(logo_field))
        )

        print(
            "[PASS] Logo URL field found — left blank."
        )


        # ====================================================
        # STEP 12 — EMAIL
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 12 — EMAIL")
        print("-" * 90)

        email_xpath = (
            "//input[@id='f-email']"
        )

        email_field = fill_input(
            driver,
            email_xpath,
            EMAIL
        )

        print(
            "Value:",
            actual_value(email_field)
        )


        # ====================================================
        # STEP 13 — TAGS
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 13 — TAGS")
        print("-" * 90)

        tags_xpath = (
            "//input[@id='f-tags']"
        )

        tags_field = fill_input(
            driver,
            tags_xpath,
            TAGS
        )

        print(
            "Value:",
            actual_value(tags_field)
        )


        # ====================================================
        # STEP 14 — QUICK CHECK
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 14 — QUICK CHECK")
        print("-" * 90)

        quick_check_input_xpath = (
            "//input[@id='captchaInput']"
        )

        quick_check_input = wait_for_visible(
            driver,
            quick_check_input_xpath
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            quick_check_input
        )

        print(
            "Quick Check field found."
        )

        print(
            "Current value:",
            repr(actual_value(quick_check_input))
        )

        print(
            "[MANUAL ACTION REQUIRED]"
        )

        print(
            "The Quick Check is a bot-prevention "
            "arithmetic check."
        )

        print(
            "It will NOT be solved automatically."
        )

        print(
            "Enter the answer manually in the browser."
        )


        # ====================================================
        # STEP 15 — INSPECT FINAL SUBMIT BUTTON
        # ====================================================

        print("\n" + "-" * 90)
        print("STEP 15 — INSPECT FINAL SUBMISSION BUTTON")
        print("-" * 90)

        final_button_xpath = (
            "//button[contains("
            "normalize-space(.),"
            "'Submit Free Listing'"
            ")]"
        )

        final_buttons = driver.find_elements(
            By.XPATH,
            final_button_xpath
        )

        visible_final_buttons = [
            button
            for button in final_buttons
            if button.is_displayed()
        ]

        if visible_final_buttons:

            final_button = visible_final_buttons[0]

            print(
                "Final button text:",
                repr(final_button.text)
            )

            print(
                "Enabled:",
                final_button.is_enabled()
            )

            print(
                "[PASS] Final submission button identified."
            )

        else:

            # Current site can also expose a slightly
            # different submit-review label.
            alternate_button_xpath = (
                "//button[contains("
                "normalize-space(.),"
                "'Submit for Review'"
                ")]"
            )

            alternate_buttons = driver.find_elements(
                By.XPATH,
                alternate_button_xpath
            )

            visible_alternate_buttons = [
                button
                for button in alternate_buttons
                if button.is_displayed()
            ]

            if visible_alternate_buttons:

                final_button = (
                    visible_alternate_buttons[0]
                )

                print(
                    "Final button text:",
                    repr(final_button.text)
                )

                print(
                    "Enabled:",
                    final_button.is_enabled()
                )

                print(
                    "[PASS] Final submission button identified."
                )

            else:

                raise Exception(
                    "Could not identify the final "
                    "submission button."
                )


        # ====================================================
        # STEP 16 — FINAL VERIFICATION
        # ====================================================

        print("\n" + "=" * 90)
        print("STEP 16 — FINAL FORM VERIFICATION")
        print("=" * 90)

        final_name = wait_for_visible(
            driver,
            "//input[@id='f-name']"
        )

        final_website = wait_for_visible(
            driver,
            "//input[@id='f-url']"
        )

        final_short = wait_for_visible(
            driver,
            "//input[@id='f-short']"
        )

        final_description = wait_for_visible(
            driver,
            "//textarea[@id='f-desc']"
        )

        final_email = wait_for_visible(
            driver,
            "//input[@id='f-email']"
        )

        final_tags = wait_for_visible(
            driver,
            "//input[@id='f-tags']"
        )

        verify_value(
            "Tool Name",
            final_name,
            TOOL_NAME
        )

        verify_value(
            "Website URL",
            final_website,
            WEBSITE_URL
        )

        verify_value(
            "Short Description",
            final_short,
            SHORT_DESCRIPTION
        )

        verify_value(
            "Full Description",
            final_description,
            FULL_DESCRIPTION
        )

        verify_value(
            "Email",
            final_email,
            EMAIL
        )

        verify_value(
            "Tags",
            final_tags,
            TAGS
        )


        # ----------------------------------------------------
        # VERIFY DROPDOWNS
        # ----------------------------------------------------

        final_category = Select(
            wait_for_visible(
                driver,
                "//select[@id='f-cat']"
            )
        ).first_selected_option.text.strip()

        final_pricing = Select(
            wait_for_visible(
                driver,
                "//select[@id='f-pricing']"
            )
        ).first_selected_option.text.strip()

        print(
            "[PASS] Category:",
            final_category
        )

        print(
            "[PASS] Pricing:",
            final_pricing
        )


        # ====================================================
        # SAFE STOP
        # ====================================================

        print("\n" + "=" * 90)
        print("THE NEXT AI — MAPPING COMPLETE")
        print("=" * 90)

        print(
            "\n[PASS] Y2Map information filled."
        )

        print(
            "[PASS] All mapped fields verified."
        )

        print(
            "[MANUAL] Quick Check left for manual entry."
        )

        print(
            "[STOP] No Submit button clicked."
        )

        print(
            "[STOP] No form submission performed."
        )

        print(
            "[STOP] Browser remains open for inspection."
        )

        print("\n" + "=" * 90)

        input(
            "\nPress ENTER to close the browser..."
        )


    except Exception as error:

        print("\n" + "=" * 90)
        print("ERROR — SCRIPT STOPPED")
        print("=" * 90)

        print(
            "\nError type:",
            type(error).__name__
        )

        print(
            "\nError message:",
            str(error)
        )

        print(
            "\nFull traceback:"
        )

        traceback.print_exc()

        print("\n" + "=" * 90)
        print("SAFE STOP")
        print("=" * 90)

        print(
            "No submission was attempted."
        )

        print(
            "Browser remains open for inspection."
        )

        input(
            "\nPress ENTER to close the browser..."
        )


    finally:

        try:
            driver.quit()
        except Exception:
            pass


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()