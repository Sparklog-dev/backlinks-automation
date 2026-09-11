import time
import warnings
import logging

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
# Y2MAP DATA
# ============================================================

TOOL_NAME = "Y2Map"

TOOL_URL = "https://y2map.com"

DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that transforms "
    "YouTube videos, PDFs, books, and research content into easy-to-understand "
    "visual mind maps. It helps students, researchers, educators, founders, "
    "engineers, and lifelong learners understand complex topics faster, "
    "organize important ideas, and improve recall."
)

CATEGORY = "Productivity"

HOMEPAGE_URL = "https://aitoolsguide.com/"


# ============================================================
# HELPER — FILL FIELD
# ============================================================

def fill_field(driver, field, value):

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        field
    )

    time.sleep(0.5)

    field.click()
    field.clear()
    field.send_keys(value)

    time.sleep(0.5)


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

wait = WebDriverWait(driver, 25)


try:

    # ========================================================
    # STEP 1 — OPEN HOMEPAGE
    # ========================================================

    print()
    print("STEP 1 — OPEN AI TOOLS GUIDE HOMEPAGE")
    print()

    driver.get(HOMEPAGE_URL)

    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//body"
            )
        )
    )

    time.sleep(3)

    print("[PASS] Homepage loaded.")
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")


    # ========================================================
    # STEP 2 — FIND ACTUAL SUBMIT TOOL LINK
    # ========================================================

    print()
    print("STEP 2 — FIND ACTUAL SUBMIT TOOL LINK")
    print()

    submit_links = driver.find_elements(
        By.XPATH,
        "//a[contains(normalize-space(.), 'Submit Tool')]"
    )

    print(
        f"Submit Tool links found: {len(submit_links)}"
    )

    submit_link = None

    for link in submit_links:

        try:

            text = (link.text or "").strip()
            href = (link.get_attribute("href") or "").strip()

            print(
                f"Link text: {text!r} | Href: {href}"
            )

            if (
                link.is_displayed()
                and "submit" in text.lower()
                and href
            ):
                submit_link = link
                break

        except Exception:
            continue


    if submit_link is None:

        raise Exception(
            "Could not find a visible Submit Tool link on the homepage."
        )


    actual_submit_href = (
        submit_link.get_attribute("href") or ""
    ).strip()

    print()
    print(
        f"[PASS] Actual submission link found: {actual_submit_href}"
    )


    # ========================================================
    # STEP 3 — OPEN ACTUAL SUBMISSION PAGE
    # ========================================================

    print()
    print("STEP 3 — OPEN ACTUAL SUBMISSION PAGE")
    print()

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        submit_link
    )

    time.sleep(0.5)

    driver.execute_script(
        "arguments[0].click();",
        submit_link
    )

    time.sleep(3)

    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")

    print("[PASS] Submission page opened.")


    # ========================================================
    # STEP 4 — WAIT FOR TOOL NAME FIELD
    # ========================================================

    print()
    print("STEP 4 — CHECK SUBMISSION FORM")
    print()

    name_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='Tool name']"
            )
        )
    )

    print("[PASS] Tool Name field detected.")
    print("[PASS] Submission form loaded.")


    # ========================================================
    # STEP 5 — TOOL NAME
    # ========================================================

    print()
    print("STEP 5 — TOOL NAME")

    fill_field(
        driver,
        name_field,
        TOOL_NAME
    )

    print(f"[PASS] Tool Name: {TOOL_NAME}")


    # ========================================================
    # STEP 6 — WEBSITE URL
    # ========================================================

    print()
    print("STEP 6 — WEBSITE URL")

    website_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='https://']"
            )
        )
    )

    fill_field(
        driver,
        website_field,
        TOOL_URL
    )

    print(f"[PASS] Website URL: {TOOL_URL}")


    # ========================================================
    # STEP 7 — DESCRIPTION
    # ========================================================

    print()
    print("STEP 7 — DESCRIPTION")

    description_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//textarea[@placeholder='Tell us what makes this tool valuable...']"
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        description_field
    )

    time.sleep(0.5)

    print(
        "Displayed :",
        description_field.is_displayed()
    )

    print(
        "Enabled   :",
        description_field.is_enabled()
    )

    description_field.click()
    description_field.clear()
    description_field.send_keys(DESCRIPTION)

    time.sleep(1)

    actual_description = (
        description_field.get_attribute("value") or ""
    )

    print()
    print("DESCRIPTION VERIFICATION")
    print(
        "Expected characters :",
        len(DESCRIPTION)
    )
    print(
        "Actual characters   :",
        len(actual_description)
    )

    if actual_description == DESCRIPTION:

        print("[PASS] Description verified.")

    else:

        raise Exception(
            "Description entered does not match expected value."
        )


    # ========================================================
    # STEP 8 — CATEGORY
    # ========================================================

    print()
    print("STEP 8 — CATEGORY")

    category_select_element = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//select"
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        category_select_element
    )

    time.sleep(0.5)

    category_dropdown = Select(
        category_select_element
    )

    print()
    print("Available categories:")

    for option in category_dropdown.options:

        print(
            " -",
            option.text.strip()
        )


    category_dropdown.select_by_visible_text(
        CATEGORY
    )

    selected_category = (
        category_dropdown
        .first_selected_option
        .text
        .strip()
    )

    print()
    print(
        "Selected category:",
        selected_category
    )

    if selected_category == CATEGORY:

        print("[PASS] Category verified.")

    else:

        raise Exception(
            "Category selection does not match expected value."
        )


    # ========================================================
    # STEP 9 — FINAL FORM VERIFICATION
    # ========================================================

    print()
    print("STEP 9 — FINAL FORM VERIFICATION")

    final_name = (
        name_field.get_attribute("value") or ""
    )

    final_website = (
        website_field.get_attribute("value") or ""
    )

    final_description = (
        description_field.get_attribute("value") or ""
    )

    final_category = (
        category_dropdown
        .first_selected_option
        .text
        .strip()
    )


    print()
    print("=" * 70)
    print("FINAL FORM VERIFICATION")
    print("=" * 70)

    print("Tool Name    :", final_name)
    print("Website URL  :", final_website)
    print(
        "Description  :",
        len(final_description),
        "characters"
    )
    print("Description  :", final_description)
    print("Category     :", final_category)

    print("=" * 70)


    # ========================================================
    # STEP 10 — VERIFY REQUIRED VALUES
    # ========================================================

    print()
    print("STEP 10 — CHECK REQUIRED FIELD VALUES")
    print()

    if final_name == TOOL_NAME:

        print("[PASS] Tool Name verified.")

    else:

        raise Exception(
            "Tool Name verification failed."
        )


    if final_website == TOOL_URL:

        print("[PASS] Website URL verified.")

    else:

        raise Exception(
            "Website URL verification failed."
        )


    if final_description == DESCRIPTION:

        print("[PASS] Description verified.")

    else:

        raise Exception(
            "Description verification failed."
        )


    if final_category == CATEGORY:

        print("[PASS] Category verified.")

    else:

        raise Exception(
            "Category verification failed."
        )


    print()
    print(
        "[PASS] ALL REQUIRED FIELDS VERIFIED SUCCESSFULLY."
    )


    # ========================================================
    # STEP 11 — INSPECT SUBMISSION CONTROLS
    # ========================================================

    print()
    print("=" * 70)
    print("STEP 11 — SUBMISSION CONTROL CHECK")
    print("=" * 70)
    print()

    print("Scanning page for submission controls...")


    # --------------------------------------------------------
    # BUTTONS
    # --------------------------------------------------------

    buttons = driver.find_elements(
        By.XPATH,
        "//button"
    )

    print()
    print(
        "BUTTONS FOUND:",
        len(buttons)
    )

    submit_candidates = []


    for index, button in enumerate(
        buttons,
        start=1
    ):

        try:

            text = (
                button.text or ""
            ).strip()

            button_type = (
                button.get_attribute("type") or ""
            ).strip()

            aria = (
                button.get_attribute("aria-label") or ""
            ).strip()

            name = (
                button.get_attribute("name") or ""
            ).strip()

            value = (
                button.get_attribute("value") or ""
            ).strip()

            displayed = button.is_displayed()
            enabled = button.is_enabled()


            print()
            print(
                f"BUTTON #{index}"
            )

            print(
                "  Text       :",
                repr(text)
            )

            print(
                "  Type       :",
                repr(button_type)
            )

            print(
                "  Name       :",
                repr(name)
            )

            print(
                "  Value      :",
                repr(value)
            )

            print(
                "  Aria-label :",
                repr(aria)
            )

            print(
                "  Displayed  :",
                displayed
            )

            print(
                "  Enabled    :",
                enabled
            )


            combined = (
                text + " " +
                aria + " " +
                name + " " +
                value
            ).lower()


            if (
                "submit" in combined
                or "send" in combined
                or "add tool" in combined
            ):

                submit_candidates.append(
                    button
                )


        except Exception as button_error:

            print(
                "  Could not inspect button:",
                button_error
            )


    # --------------------------------------------------------
    # INPUT TYPE SUBMIT
    # --------------------------------------------------------

    submit_inputs = driver.find_elements(
        By.XPATH,
        "//input[@type='submit']"
    )

    print()
    print(
        "INPUT SUBMIT CONTROLS FOUND:",
        len(submit_inputs)
    )


    for index, element in enumerate(
        submit_inputs,
        start=1
    ):

        try:

            value = (
                element.get_attribute("value") or ""
            ).strip()

            name = (
                element.get_attribute("name") or ""
            ).strip()


            print()
            print(
                f"SUBMIT INPUT #{index}"
            )

            print(
                "  Value      :",
                repr(value)
            )

            print(
                "  Name       :",
                repr(name)
            )

            print(
                "  Displayed  :",
                element.is_displayed()
            )

            print(
                "  Enabled    :",
                element.is_enabled()
            )


            submit_candidates.append(
                element
            )


        except Exception as input_error:

            print(
                "Could not inspect submit input:",
                input_error
            )


    # ========================================================
    # STEP 12 — RESULT
    # ========================================================

    print()
    print("-" * 70)

    if submit_candidates:

        print(
            "[PASS] Submission control detected."
        )

        print(
            "Number of candidate controls:",
            len(submit_candidates)
        )

        print()
        print(
            "[STOP] Submit button will NOT be clicked."
        )

    else:

        print(
            "[INFO] No submission control detected."
        )

        print()
        print(
            "The mapped fields are verified."
        )

        print(
            "Submission control requires further inspection."
        )


    # ========================================================
    # FINAL STOP POINT
    # ========================================================

    print()
    print("=" * 70)
    print("AI TOOLS GUIDE — MAPPING COMPLETE")
    print("=" * 70)

    print("[PASS] Homepage opened.")
    print("[PASS] Actual submission link found.")
    print("[PASS] Submission page opened.")
    print("[PASS] Tool Name filled and verified.")
    print("[PASS] Website URL filled and verified.")
    print("[PASS] Description filled and verified.")
    print("[PASS] Category selected and verified.")

    if submit_candidates:

        print(
            "[PASS] Submission control identified."
        )

    else:

        print(
            "[INFO] Submission control not identified."
        )

    print()
    print("[STOP] No submission performed.")
    print("[STOP] No Submit control clicked.")
    print()
    print("Browser will remain open for inspection.")
    print("Press ENTER to close...")


    input()


except Exception as e:

    print()
    print("=" * 70)
    print("AUTOMATION ERROR")
    print("=" * 70)

    print(
        type(e).__name__ + ":",
        str(e)
    )

    print()
    print(
        "[STOP] Browser will remain open for inspection."
    )

    print(
        "Press ENTER to close..."
    )

    input()


finally:

    try:
        driver.quit()
    except Exception:
        pass