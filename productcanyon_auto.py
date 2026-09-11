import warnings
import logging
import traceback

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# =========================================================
# PRODUCT DETAILS
# =========================================================

NAME = "Nikhil"
EMAIL = "sparklog.marketing@gmail.com"
PRODUCT_NAME = "Y2Map"
WEBSITE = "https://y2map.com"

DESCRIPTION = (
    "Y2Map is an AI tool that helps you turn long videos and PDF "
    "documents into easy-to-read visual mind maps."
)

HOMEPAGE = "https://productcanyon.com/"


# =========================================================
# SUPPRESS ONLY WARNINGS / LOGGING
# DO NOT HIDE STDERR
# =========================================================

warnings.filterwarnings("ignore")
logging.disable(logging.CRITICAL)


# =========================================================
# START CHROME
# =========================================================

print("\n" + "=" * 70)
print("PRODUCT CANYON AUTOMATION")
print("=" * 70)

print("\n🚀 Starting Chrome...")

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

# Prevent undetected_chromedriver cleanup noise.
uc.Chrome.__del__ = lambda self: None

wait = WebDriverWait(driver, 20)


try:

    # =====================================================
    # STEP 0 — HOME PAGE
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 0 — HOME PAGE")
    print("=" * 70)

    driver.get(HOMEPAGE)

    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//body"
            )
        )
    )

    print("Page title :", driver.title)
    print("Current URL:", driver.current_url)


    # =====================================================
    # STEP 1 — FIND LIST YOUR PRODUCT
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 1 — FIND LIST YOUR PRODUCT")
    print("=" * 70)

    list_product_xpath = (
        "//a["
        "contains("
        "translate(@href,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'/sell-your-products/'"
        ")"
        "]"
    )

    list_product_link = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                list_product_xpath
            )
        )
    )

    link_text = list_product_link.text.strip()
    submission_url = list_product_link.get_attribute("href")
    target = list_product_link.get_attribute("target")

    print("[PASS] List Your Product link found.")
    print("Text  :", link_text)
    print("Href  :", submission_url)
    print("Target:", target)

    if not submission_url:
        raise Exception(
            "List Your Product link has no href."
        )

    if "/sell-your-products/" not in submission_url:
        raise Exception(
            "The verified List Your Product href is not the expected submission page."
        )

    print("[PASS] Submission href verified.")


    # =====================================================
    # STEP 2 — OPEN VERIFIED SUBMISSION URL IN NEW TAB
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 2 — OPEN LIST YOUR PRODUCT")
    print("=" * 70)

    driver.switch_to.new_window("tab")

    driver.get(submission_url)

    print("[OK] Verified List Your Product URL opened in new tab.")


    # =====================================================
    # STEP 3 — VERIFY SUBMISSION PAGE
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 3 — VERIFY SUBMISSION PAGE")
    print("=" * 70)

    wait.until(
        lambda d: "/sell-your-products/" in d.current_url
    )

    print("[PASS] Submission page opened.")
    print("URL  :", driver.current_url)
    print("Title:", driver.title)


    # =====================================================
    # STEP 4 — WAIT FOR FORM
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 4 — DETECT FORM")
    print("=" * 70)

    name_xpath = (
        "//input[@id='ff_4_names_first_name_']"
    )

    email_xpath = (
        "//input[@id='ff_4_email']"
    )

    product_xpath = (
        "//input[@id='ff_4_subject']"
    )

    website_xpath = (
        "//input[@id='ff_4_subject_1']"
    )

    description_xpath = (
        "//textarea[@id='ff_4_message']"
    )

    paid_radio_xpath = (
        "//input[@id='input_radio_c20bb6b170d978147aa2c524c0c23e7d']"
    )

    free_radio_xpath = (
        "//input[@id='input_radio_01b8e5cdbe821c396c63543b36e2ee8d']"
    )

    subscription_xpath = (
        "//select[@id='ff_4_dropdown']"
    )

    hear_xpath = (
        "//select[@id='ff_4_dropdown_1']"
    )

    wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                name_xpath
            )
        )
    )

    print("[PASS] Product Canyon form detected.")


    # =====================================================
    # STEP 5 — NAME
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 5 — NAME")
    print("=" * 70)

    name_field = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                name_xpath
            )
        )
    )

    name_field.clear()
    name_field.send_keys(NAME)

    print("[PASS] Name entered:", NAME)


    # =====================================================
    # STEP 6 — EMAIL
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 6 — EMAIL")
    print("=" * 70)

    email_field = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                email_xpath
            )
        )
    )

    email_field.clear()
    email_field.send_keys(EMAIL)

    print("[PASS] Email entered:", EMAIL)


    # =====================================================
    # STEP 7 — PRODUCT NAME
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 7 — PRODUCT NAME")
    print("=" * 70)

    product_field = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                product_xpath
            )
        )
    )

    product_field.clear()
    product_field.send_keys(PRODUCT_NAME)

    print("[PASS] Product Name entered:", PRODUCT_NAME)


    # =====================================================
    # STEP 8 — WEBSITE
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 8 — WEBSITE")
    print("=" * 70)

    website_field = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                website_xpath
            )
        )
    )

    website_field.clear()
    website_field.send_keys(WEBSITE)

    print("[PASS] Website entered:", WEBSITE)

    # =====================================================
    # STEP 9 — PRODUCT TYPE
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 9 — PRODUCT TYPE")
    print("=" * 70)

    print("[INFO] Checking Product Type options...")

    product_type_radios = wait.until(
        EC.presence_of_all_elements_located(
            (
                By.XPATH,
                "//input[@type='radio']"
            )
        )
    )

    if len(product_type_radios) < 2:
        raise Exception(
            "Product Type radio buttons were not detected correctly."
        )

    print(
        "[INFO] Radio buttons detected:",
        len(product_type_radios)
    )

    selected_radio = None

    for radio in product_type_radios:

        if radio.is_selected():
            selected_radio = radio
            break

    if selected_radio is None:
        raise Exception(
            "No Product Type option is currently selected."
        )

    # Get the visible text associated with the selected radio.
    selected_label = driver.execute_script(
        """
        var input = arguments[0];

        var label = input.closest('label');

        if (label) {
            return label.innerText.trim();
        }

        var parent = input.parentElement;

        if (parent) {
            return parent.innerText.trim();
        }

        return '';
        """,
        selected_radio
    )

    print(
        "[INFO] Selected Product Type:",
        selected_label
    )

    if "Paid" not in selected_label:
        raise Exception(
            "Product Type is not Paid."
        )

    print("[PASS] Product Type: Paid")

    # =====================================================
    # STEP 10 — SUBSCRIPTION TYPE
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 10 — SUBSCRIPTION TYPE")
    print("=" * 70)

    subscription_element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                subscription_xpath
            )
        )
    )

    subscription_dropdown = Select(
        subscription_element
    )

    current_subscription = (
        subscription_dropdown
        .first_selected_option
        .text
        .strip()
    )

    print(
        "Current selection:",
        current_subscription
    )

    subscription_dropdown.select_by_visible_text(
        "Lifetime Deal"
    )

    selected_subscription = (
        subscription_dropdown
        .first_selected_option
        .text
        .strip()
    )

    print(
        "[PASS] Subscription Type:",
        selected_subscription
    )


    # =====================================================
    # STEP 11 — HOW DID YOU HEAR ABOUT US?
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 11 — HOW DID YOU HEAR ABOUT US")
    print("=" * 70)

    hear_element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                hear_xpath
            )
        )
    )

    hear_dropdown = Select(
        hear_element
    )

    current_source = (
        hear_dropdown
        .first_selected_option
        .text
        .strip()
    )

    print(
        "Current selection:",
        current_source
    )

    hear_dropdown.select_by_visible_text(
        "Other"
    )

    selected_source = (
        hear_dropdown
        .first_selected_option
        .text
        .strip()
    )

    print(
        "[PASS] How did you hear:",
        selected_source
    )


    # =====================================================
    # STEP 12 — DESCRIPTION
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 12 — PRODUCT DESCRIPTION")
    print("=" * 70)

    description_field = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                description_xpath
            )
        )
    )

    description_field.clear()
    description_field.send_keys(DESCRIPTION)

    print("[PASS] Product Description entered.")


    # =====================================================
    # STEP 13 — FINAL VALUE VERIFICATION
    # =====================================================

    print("\n" + "=" * 70)
    print("STEP 13 — VERIFY ACTUAL FORM VALUES")
    print("=" * 70)

    actual_name = (
        driver.find_element(
            By.XPATH,
            name_xpath
        )
        .get_attribute("value")
        .strip()
    )

    actual_email = (
        driver.find_element(
            By.XPATH,
            email_xpath
        )
        .get_attribute("value")
        .strip()
    )

    actual_product = (
        driver.find_element(
            By.XPATH,
            product_xpath
        )
        .get_attribute("value")
        .strip()
    )

    actual_website = (
        driver.find_element(
            By.XPATH,
            website_xpath
        )
        .get_attribute("value")
        .strip()
    )

    actual_description = (
        driver.find_element(
            By.XPATH,
            description_xpath
        )
        .get_attribute("value")
        .strip()
    )
    # -----------------------------------------------------
    # GET ACTUAL PRODUCT TYPE
    # -----------------------------------------------------

    actual_product_type = None

    actual_radios = driver.find_elements(
        By.XPATH,
        "//input[@type='radio']"
    )

    for radio in actual_radios:

        if radio.is_selected():

            actual_product_type = driver.execute_script(
                """
                var input = arguments[0];

                var label = input.closest('label');

                if (label) {
                    return label.innerText.trim();
                }

                var parent = input.parentElement;

                if (parent) {
                    return parent.innerText.trim();
                }

                return '';
                """,
                radio
            )

            break

    if not actual_product_type:
        raise Exception(
            "Product Type verification failed. "
            "No selected radio option was found."
        )

    print(
        "[INFO] Actual Product Type:",
        actual_product_type
    )

    if "Paid" not in actual_product_type:
        raise Exception(
            "Product Type verification failed. "
            f"Expected Paid | Actual: {actual_product_type}"
        )

    print("[PASS] Product Type verified: Paid")

    actual_subscription = (
        Select(
            driver.find_element(
                By.XPATH,
                subscription_xpath
            )
        )
        .first_selected_option
        .text
        .strip()
    )

    actual_source = (
        Select(
            driver.find_element(
                By.XPATH,
                hear_xpath
            )
        )
        .first_selected_option
        .text
        .strip()
    )


    # -----------------------------------------------------
    # VERIFY NAME
    # -----------------------------------------------------

    if actual_name != NAME:
        raise Exception(
            f"Name verification failed. "
            f"Expected: {NAME} | Actual: {actual_name}"
        )

    print("[PASS] Name verified:", actual_name)


    # -----------------------------------------------------
    # VERIFY EMAIL
    # -----------------------------------------------------

    if actual_email != EMAIL:
        raise Exception(
            f"Email verification failed. "
            f"Expected: {EMAIL} | Actual: {actual_email}"
        )

    print("[PASS] Email verified:", actual_email)


    # -----------------------------------------------------
    # VERIFY PRODUCT NAME
    # -----------------------------------------------------

    if actual_product != PRODUCT_NAME:
        raise Exception(
            f"Product Name verification failed. "
            f"Expected: {PRODUCT_NAME} | Actual: {actual_product}"
        )

    print("[PASS] Product Name verified:", actual_product)


    # -----------------------------------------------------
    # VERIFY WEBSITE
    # -----------------------------------------------------

    if actual_website != WEBSITE:
        raise Exception(
            f"Website verification failed. "
            f"Expected: {WEBSITE} | Actual: {actual_website}"
        )

    print("[PASS] Website verified:", actual_website)


    # -----------------------------------------------------
    # VERIFY SUBSCRIPTION
    # -----------------------------------------------------

    if actual_subscription != "Lifetime Deal":
        raise Exception(
            f"Subscription verification failed. "
            f"Expected: Lifetime Deal | Actual: {actual_subscription}"
        )

    print(
        "[PASS] Subscription verified:",
        actual_subscription
    )


    # -----------------------------------------------------
    # VERIFY SOURCE
    # -----------------------------------------------------

    if actual_source != "Other":
        raise Exception(
            f"Source verification failed. "
            f"Expected: Other | Actual: {actual_source}"
        )

    print(
        "[PASS] How did you hear verified:",
        actual_source
    )


    # -----------------------------------------------------
    # VERIFY DESCRIPTION
    # -----------------------------------------------------

    if actual_description != DESCRIPTION:
        raise Exception(
            "Product Description verification failed."
        )

    print("[PASS] Product Description verified.")


    # =====================================================
    # STEP 14 — FINAL STATUS
    # =====================================================

    print("\n" + "=" * 70)
    print("PRODUCT CANYON MAPPING COMPLETE")
    print("=" * 70)

    print("\nName             :", actual_name)
    print("Email            :", actual_email)
    print("Product Name     :", actual_product)
    print("Website          :", actual_website)
    print("Product Type     : Paid")
    print("Subscription     :", actual_subscription)
    print("How did you hear :", actual_source)
    print("Description      :", actual_description)

    print("\n" + "=" * 70)
    print("STOP — NO SUBMISSION")
    print("=" * 70)

    print("[STOP] No Submit button clicked.")
    print("[STOP] No form submission performed.")
    print("[STOP] Browser remains open for inspection.")


    # =====================================================
    # KEEP BROWSER OPEN
    # =====================================================

    input(
        "\nPress ENTER when ready to close Chrome..."
    )


except Exception as error:

    print("\n" + "=" * 70)
    print("AUTOMATION STOPPED WITH ERROR")
    print("=" * 70)

    print("\nError type :", type(error).__name__)
    print("Error      :", str(error))

    print("\nFull traceback:")
    traceback.print_exc()

    print("\nCurrent URL :", driver.current_url)

    print("\n" + "=" * 70)
    print("STOP — BROWSER KEPT OPEN FOR INSPECTION")
    print("=" * 70)

    input(
        "\nPress ENTER to close Chrome..."
    )


finally:

    try:
        driver.quit()
    except Exception:
        pass