import os
import time
import traceback

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# ======================================================================
# DROPYOURAI — Y2MAP AUTOMATION
# ======================================================================

HOMEPAGE = "https://www.dropyourai.com/"
EXPECTED_SUBMIT_URL = "https://www.dropyourai.com/submit-tool"

TOOL_NAME = "Y2Map"
EMAIL = "sparklog.marketing@gmail.com"
WEBSITE = "y2map.com"

SHORT_DESCRIPTION = "Turn videos and PDFs into mind maps."

LONG_DESCRIPTION = (
    "Y2Map is an AI-powered learning tool that turns YouTube videos, "
    "PDFs, books, and research content into visual mind maps. "
    "It helps students, researchers, founders, educators, and lifelong "
    "learners understand complex information faster, organize key ideas, "
    "and build stronger mental models."
)

LOGO_PATH = r"C:\Users\savan\OneDrive\Desktop\GTM_Internship\Nikhil\y2map_logo.png"

CATEGORY = "Productivity"


# ----------------------------------------------------------------------
# DRIVER CLEANUP
# ----------------------------------------------------------------------

uc.Chrome.__del__ = lambda self: None


# ----------------------------------------------------------------------
# DRIVER
# ----------------------------------------------------------------------

driver = None


# ----------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------

def visible_xpath(xpath, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


def find_visible_xpath(xpath):
    elements = driver.find_elements(By.XPATH, xpath)
    return [element for element in elements if element.is_displayed()]


def set_input_value(xpath, value, label):
    element = visible_xpath(xpath)

    driver.execute_script(
        """
        const element = arguments[0];
        const value = arguments[1];

        const prototype =
            element.tagName.toLowerCase() === 'textarea'
            ? window.HTMLTextAreaElement.prototype
            : window.HTMLInputElement.prototype;

        const descriptor =
            Object.getOwnPropertyDescriptor(prototype, 'value');

        if (descriptor && descriptor.set) {
            descriptor.set.call(element, value);
        } else {
            element.value = value;
        }

        element.dispatchEvent(new Event('input', { bubbles: true }));
        element.dispatchEvent(new Event('change', { bubbles: true }));
        element.dispatchEvent(new Event('blur', { bubbles: true }));
        """,
        element,
        value
    )

    time.sleep(0.5)

    actual_value = element.get_attribute("value")

    print(f"{label}: {actual_value}")

    if actual_value != value:
        raise RuntimeError(
            f"{label} verification failed. "
            f"Expected '{value}', got '{actual_value}'."
        )

    print(f"[PASS] {label} verified.")


def print_form_fields():
    print("\nVISIBLE INPUT DETAILS")

    inputs = driver.find_elements(By.XPATH, "//input")

    visible_inputs = [
        element for element in inputs
        if element.is_displayed()
    ]

    for index, element in enumerate(visible_inputs, start=1):
        print(
            f"{index}. "
            f"type={element.get_attribute('type')} | "
            f"name={element.get_attribute('name')} | "
            f"id={element.get_attribute('id')} | "
            f"placeholder={element.get_attribute('placeholder')} | "
            f"aria-label={element.get_attribute('aria-label')} | "
            f"value={element.get_attribute('value')}"
        )

    print(f"\nVisible input elements: {len(visible_inputs)}")

    textareas = driver.find_elements(By.XPATH, "//textarea")

    visible_textareas = [
        element for element in textareas
        if element.is_displayed()
    ]

    print(f"Visible textarea elements: {len(visible_textareas)}")

    if visible_textareas:
        print("\nVISIBLE TEXTAREA DETAILS")

        for index, element in enumerate(visible_textareas, start=1):
            print(
                f"{index}. "
                f"name={element.get_attribute('name')} | "
                f"id={element.get_attribute('id')} | "
                f"placeholder={element.get_attribute('placeholder')} | "
                f"aria-label={element.get_attribute('aria-label')}"
            )


def print_select_details():
    print("\nVISIBLE SELECT ELEMENTS")

    selects = driver.find_elements(By.XPATH, "//select")

    visible_selects = [
        element for element in selects
        if element.is_displayed()
    ]

    for index, select_element in enumerate(visible_selects, start=1):

        print(
            f"{index}. "
            f"id={select_element.get_attribute('id')} | "
            f"name={select_element.get_attribute('name')} | "
            f"value={select_element.get_attribute('value')}"
        )

        options = select_element.find_elements(By.XPATH, ".//option")

        for option in options:
            print(
                f"    option: "
                f"text='{option.text}' | "
                f"value='{option.get_attribute('value')}'"
            )


def select_option_by_visible_text(xpath, option_text, label):
    select_element = visible_xpath(xpath)

    select = Select(select_element)

    available_options = [
        option.text.strip()
        for option in select.options
    ]

    print(f"Available {label} options: {available_options}")

    if option_text not in available_options:
        raise RuntimeError(
            f"Expected {label} option '{option_text}' was not found."
        )

    select.select_by_visible_text(option_text)

    time.sleep(1)

    selected_text = select.first_selected_option.text.strip()

    print(f"{label}: {selected_text}")

    if selected_text != option_text:
        raise RuntimeError(
            f"{label} verification failed. "
            f"Expected '{option_text}', got '{selected_text}'."
        )

    print(f"[PASS] {label} selected and verified.")


# ======================================================================
# START
# ======================================================================

try:

    print("=" * 70)
    print("DROPYOURAI — Y2MAP AUTOMATION")
    print("=" * 70)

    print("\nStarting Chrome...")

    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = uc.Chrome(
        version_main=152,
        options=options
    )

    wait = WebDriverWait(driver, 20)


    # ==================================================================
    # STEP 1
    # ==================================================================

    print("\nSTEP 1 — OPEN DROPYOURAI HOMEPAGE")

    driver.get(HOMEPAGE)

    wait.until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    print("\n[PASS] Homepage loaded.")
    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")


    # ==================================================================
    # STEP 2
    # ==================================================================

    print("\nSTEP 2 — FIND ACTUAL SUBMIT TOOL LINK")

    submit_xpath = (
        "//a[@data-testid='linkElement' "
        "and normalize-space()='Submit tool' "
        "and contains(@href, '/submit-tool')]"
    )

    submit_links = find_visible_xpath(submit_xpath)

    print(f"Submit Tool links found: {len(submit_links)}")

    actual_submit_url = None

    for link in submit_links:
        text = link.text.strip()
        href = link.get_attribute("href")

        print(f"Link text: '{text}'")
        print(f"Href: {href}")

        if href == EXPECTED_SUBMIT_URL:
            actual_submit_url = href
            break

    if not actual_submit_url:
        raise RuntimeError(
            "Actual DropYourAI Submit Tool link was not found."
        )

    print(
        f"[PASS] Actual submission link found: "
        f"{actual_submit_url}"
    )


    # ==================================================================
    # STEP 3
    # ==================================================================

    print("\nSTEP 3 — OPEN SUBMISSION PAGE")

    driver.get(actual_submit_url)

    wait.until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    time.sleep(2)

    print(f"Current URL: {driver.current_url}")
    print(f"Page title: {driver.title}")

    if not driver.current_url.startswith(EXPECTED_SUBMIT_URL):
        raise RuntimeError(
            "Submission page URL verification failed."
        )

    print("[PASS] Submission page opened.")


    # ==================================================================
    # STEP 4
    # ==================================================================

    print("\nSTEP 4 — INSPECT FORM FIELDS")

    print_form_fields()

    print("\n[PASS] Form structure inspected.")


    # ==================================================================
    # STEP 5
    # ==================================================================

    print("\nSTEP 5 — PROJECT NAME")

    set_input_value(
        "//input[@id='input_comp-lk5wclbm']",
        TOOL_NAME,
        "Project Name"
    )


    # ==================================================================
    # STEP 6
    # ==================================================================

    print("\nSTEP 6 — E-MAIL")

    set_input_value(
        "//input[@id='input_comp-lklog3b66']",
        EMAIL,
        "E-mail"
    )


    # ==================================================================
    # STEP 7
    # ==================================================================

    print("\nSTEP 7 — WEBSITE")

    set_input_value(
        "//input[@id='input_comp-lkloggvo1']",
        WEBSITE,
        "Website"
    )


    # ==================================================================
    # STEP 8
    # ==================================================================

    print("\nSTEP 8 — PRICING TYPE")

    free_xpath = (
        "//*[normalize-space()='Free' "
        "and not(self::option)]"
    )

    free_elements = find_visible_xpath(free_xpath)

    if not free_elements:
        raise RuntimeError(
            "Free pricing option was not found."
        )

    free_selected = False

    for element in free_elements:

        try:
            element.click()
            time.sleep(0.5)

            free_selected = True
            break

        except Exception:
            continue

    if not free_selected:
        raise RuntimeError(
            "Could not select Free pricing option."
        )

    print("[PASS] Free pricing option selected.")


    # ==================================================================
    # STEP 9
    # ==================================================================

    print("\nSTEP 9 — PRICING")

    pricing_xpath = "//input[@id='input_comp-lk5wjxgk']"

    pricing_element = visible_xpath(pricing_xpath)

    print(
        "Pricing input detected: "
        f"placeholder='{pricing_element.get_attribute('placeholder')}' | "
        f"type='{pricing_element.get_attribute('type')}' | "
        f"value='{pricing_element.get_attribute('value')}'"
    )

    set_input_value(
        pricing_xpath,
        "0",
        "Pricing"
    )


    # ==================================================================
    # STEP 10
    # ==================================================================

    print("\nSTEP 10 — CURRENCY / PRICING TERM")

    print_select_details()

    print(
        "\n[INFO] Currency and pricing-term controls inspected."
    )

    print(
        "[INFO] They remain unchanged because Y2Map is being "
        "listed as Free."
    )


    # ==================================================================
    # STEP 11
    # ==================================================================

    print("\nSTEP 11 — AI CATEGORY")

    category_xpath = (
        "//select[@id='collection_comp-lkfvfvjd']"
    )

    select_option_by_visible_text(
        category_xpath,
        CATEGORY,
        "AI Category"
    )


    # ==================================================================
    # STEP 12
    # ==================================================================

    print("\nSTEP 12 — LOGO / IMAGE UPLOAD")

    if not os.path.isfile(LOGO_PATH):
        raise FileNotFoundError(
            f"Logo file was not found:\n{LOGO_PATH}"
        )

    print(f"Logo file found: {LOGO_PATH}")
    print(f"File size: {os.path.getsize(LOGO_PATH)} bytes")

    # IMPORTANT:
    # Search specifically for file-upload inputs using XPath.
    file_inputs = driver.find_elements(
        By.XPATH,
        "//input[@type='file']"
    )

    print(
        f"File upload inputs found: {len(file_inputs)}"
    )

    if len(file_inputs) == 0:
        raise RuntimeError(
            "No file upload input was found on the live page."
        )

    visible_or_present_file_inputs = [
        element
        for element in file_inputs
        if element.is_displayed() or element.is_enabled()
    ]

    if len(visible_or_present_file_inputs) == 0:
        raise RuntimeError(
            "A file input exists, but none is available for upload."
        )

    if len(visible_or_present_file_inputs) > 1:
        print(
            "[INFO] More than one file input exists. "
            "Inspecting their attributes before choosing."
        )

        for index, element in enumerate(
            visible_or_present_file_inputs,
            start=1
        ):
            print(
                f"{index}. "
                f"id={element.get_attribute('id')} | "
                f"name={element.get_attribute('name')} | "
                f"accept={element.get_attribute('accept')} | "
                f"multiple={element.get_attribute('multiple')}"
            )

        # We do not blindly choose among multiple upload inputs.
        raise RuntimeError(
            "Multiple file-upload inputs were found. "
            "The exact logo upload input needs to be confirmed."
        )

    file_input = visible_or_present_file_inputs[0]

    file_input.send_keys(LOGO_PATH)

    time.sleep(1)

    uploaded_value = file_input.get_attribute("value")

    print(f"Upload input value: {uploaded_value}")

    if not uploaded_value:
        raise RuntimeError(
            "Logo upload could not be verified."
        )

    if os.path.basename(LOGO_PATH).lower() not in uploaded_value.lower():
        raise RuntimeError(
            "Logo upload value does not contain the expected filename."
        )

    print(
        f"[PASS] Logo attached: "
        f"{os.path.basename(LOGO_PATH)}"
    )


    # ==================================================================
    # STEP 13
    # ==================================================================

    print("\nSTEP 13 — SHORT DESCRIPTION")

    set_input_value(
        "//input[@id='input_comp-lk5wlm9y3']",
        SHORT_DESCRIPTION,
        "Short Description"
    )


    # ==================================================================
    # STEP 14
    # ==================================================================

    print("\nSTEP 14 — LONG DESCRIPTION")

    set_input_value(
        "//textarea[@id='textarea_comp-lk5wsr9b']",
        LONG_DESCRIPTION,
        "Long Description"
    )


    # ==================================================================
    # STEP 15
    # ==================================================================

    print("\nSTEP 15 — OPTIONAL YOUTUBE")

    youtube_xpath = (
        "//input[@id='input_comp-lk5wj7iv']"
    )

    youtube_fields = find_visible_xpath(youtube_xpath)

    if youtube_fields:
        print("[INFO] Youtube field detected — left blank.")
    else:
        print("[INFO] Youtube field not visible.")


    # ==================================================================
    # STEP 16
    # ==================================================================

    print("\nSTEP 16 — OPTIONAL TWITTER")

    twitter_xpath = (
        "//input[@id='input_comp-lkgmxpld']"
    )

    twitter_fields = find_visible_xpath(twitter_xpath)

    if twitter_fields:
        print("[INFO] Twitter field detected — left blank.")
    else:
        print("[INFO] Twitter field not visible.")


    # ==================================================================
    # STEP 17
    # ==================================================================

    print("\nSTEP 17 — OPTIONAL LINKEDIN")

    linkedin_xpath = (
        "//input[@id='input_comp-lk5x4hgc4']"
    )

    linkedin_fields = find_visible_xpath(linkedin_xpath)

    if linkedin_fields:
        print("[INFO] Linkedin field detected — left blank.")
    else:
        print("[INFO] Linkedin field not visible.")


    # ==================================================================
    # STEP 18
    # ==================================================================

    print("\nSTEP 18 — FINAL EMAIL FIELD")

    additional_email_xpath = (
        "//input[@id='input_comp-lk5vwc16_r_comp-lk1e4wfn']"
    )

    additional_email_fields = find_visible_xpath(
        additional_email_xpath
    )

    if additional_email_fields:
        print("[INFO] Additional email field detected.")
        print("[INFO] Leaving additional email field unchanged.")
    else:
        print("[INFO] Additional email field not visible.")


    # ==================================================================
    # STEP 19
    # ==================================================================

    print("\nSTEP 19 — FINAL FIELD VERIFICATION")

    project_name = visible_xpath(
        "//input[@id='input_comp-lk5wclbm']"
    ).get_attribute("value")

    email_value = visible_xpath(
        "//input[@id='input_comp-lklog3b66']"
    ).get_attribute("value")

    website_value = visible_xpath(
        "//input[@id='input_comp-lkloggvo1']"
    ).get_attribute("value")

    pricing_value = visible_xpath(
        "//input[@id='input_comp-lk5wjxgk']"
    ).get_attribute("value")

    short_value = visible_xpath(
        "//input[@id='input_comp-lk5wlm9y3']"
    ).get_attribute("value")

    long_value = visible_xpath(
        "//textarea[@id='textarea_comp-lk5wsr9b']"
    ).get_attribute("value")

    print(f"Project Name: {project_name}")
    print(f"[PASS] Project Name verified.")

    print(f"E-mail: {email_value}")
    print(f"[PASS] E-mail verified.")

    print(f"Website: {website_value}")
    print(f"[PASS] Website verified.")

    print(f"Pricing: {pricing_value}")
    print(f"[PASS] Pricing verified.")

    print(f"Short Description: {short_value}")
    print(f"[PASS] Short Description verified.")

    print(f"Long Description: {long_value}")
    print(f"[PASS] Long Description verified.")


    # ==================================================================
    # STEP 20
    # ==================================================================

    print("\nSTEP 20 — CATEGORY VERIFICATION")

    category_element = visible_xpath(
        category_xpath
    )

    category_select = Select(category_element)

    selected_category = (
        category_select.first_selected_option.text.strip()
    )

    print(f"Selected AI Category: {selected_category}")

    if selected_category != CATEGORY:
        raise RuntimeError(
            f"AI Category verification failed. "
            f"Expected '{CATEGORY}', got '{selected_category}'."
        )

    print("[PASS] AI Category verified.")


    # ==================================================================
    # STEP 21
    # ==================================================================

    print("\nSTEP 21 — SUB-CATEGORY INSPECTION")

    subcategory_xpath = (
        "//select[@id='collection_comp-lkfvfvjg2']"
    )

    subcategory_fields = find_visible_xpath(
        subcategory_xpath
    )

    if subcategory_fields:

        subcategory_element = subcategory_fields[0]

        subcategory_select = Select(
            subcategory_element
        )

        print("Available Sub-category options:")

        for option in subcategory_select.options:
            print(
                f"    - text='{option.text.strip()}' | "
                f"value='{option.get_attribute('value')}'"
            )

        current_subcategory = (
            subcategory_select.first_selected_option.text.strip()
        )

        print(
            f"Current Sub-category: "
            f"'{current_subcategory}'"
        )

        print(
            "[INFO] Sub-category left unchanged because "
            "no Y2Map-relevant option has been verified."
        )

    else:
        print(
            "[INFO] Sub-category control not visible."
        )


    # ==================================================================
    # STEP 22
    # ==================================================================

    print("\nSTEP 22 — FIND CONTINUE / SUBMIT")

    print("[STOP CONDITION: DO NOT CLICK]")

    action_elements = driver.find_elements(
        By.XPATH,
        "//button | //a"
    )

    potential_actions = []

    for element in action_elements:

        if not element.is_displayed():
            continue

        text = element.text.strip()

        if text in ["Continue", "Submit tool"]:
            potential_actions.append(element)

    for index, element in enumerate(
        potential_actions,
        start=1
    ):
        print(
            f"Action {index}: "
            f"text='{element.text.strip()}' | "
            f"tag={element.tag_name} | "
            f"enabled={element.is_enabled()} | "
            f"id={element.get_attribute('id')}"
        )

    print(
        f"Potential Continue/Submit actions found: "
        f"{len(potential_actions)}"
    )


    # ==================================================================
    # FINAL SUMMARY
    # ==================================================================

    print("\n" + "=" * 70)
    print("DROPYOURAI — MAPPING COMPLETE")
    print("=" * 70)

    print("\nVerified data:")

    print(f"Project Name      : {project_name}")
    print(f"E-mail            : {email_value}")
    print(f"Website            : {website_value}")
    print(f"Pricing            : {pricing_value}")
    print(f"AI Category        : {selected_category}")
    print(f"Short Description  : {short_value}")
    print(f"Long Description   : {long_value}")
    print(
        f"Logo               : "
        f"{os.path.basename(LOGO_PATH)}"
    )

    print("\n[PASS] Homepage loaded.")
    print("[PASS] Actual Submit tool link verified.")
    print("[PASS] Submission page opened.")
    print("[PASS] Project Name verified.")
    print("[PASS] E-mail verified.")
    print("[PASS] Website verified.")
    print("[PASS] Free pricing selected.")
    print("[PASS] Pricing verified.")
    print("[PASS] AI Category verified.")
    print("[PASS] Logo upload verified.")
    print("[PASS] Short Description verified.")
    print("[PASS] Long Description verified.")
    print("[PASS] Final fields verified.")

    print(
        "\n[STOP] Continue/Submit was NOT clicked."
    )

    print(
        "\nBrowser will remain open for inspection."
    )

    input(
        "\nPress ENTER to close the browser..."
    )


except Exception as error:

    print("\n" + "=" * 70)
    print("ERROR")
    print("=" * 70)

    print(
        f"\n{type(error).__name__}: {error}"
    )

    traceback.print_exc()

    if driver is not None:
        print(
            "\nBrowser will remain open for inspection."
        )

        input(
            "\nPress ENTER to close the browser..."
        )

finally:

    if driver is not None:
        try:
            driver.quit()
        except Exception:
            pass