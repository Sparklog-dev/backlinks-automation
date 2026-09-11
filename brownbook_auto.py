import time

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


HOME_URL = "https://www.brownbook.net/"

PRODUCT_NAME = "Y2Map"
EMAIL = "sparklog.marketing@gmail.com"
WEBSITE = "https://y2map.com"
CATEGORY = "Educational Services"
COUNTRY = "India"


# Search terms only.
# NOTHING will be selected.
TAG_SEARCHES = [
    "AI",
    "art",
    "education",
    "technology",
    "computer",
    "training",
    "consulting",
    "internet",
    "software",
    "services",
]


def visible_elements(driver, xpath):
    elements = driver.find_elements(By.XPATH, xpath)
    return [element for element in elements if element.is_displayed()]


def first_visible(driver, xpath):
    elements = driver.find_elements(By.XPATH, xpath)

    for element in elements:
        if element.is_displayed():
            return element

    return None


def first_visible_enabled(driver, xpath):
    elements = driver.find_elements(By.XPATH, xpath)

    for element in elements:
        if element.is_displayed() and element.is_enabled():
            return element

    return None


options = uc.ChromeOptions()
options.add_argument("--start-maximized")

try:
    uc.Chrome.__del__ = lambda self: None
except Exception:
    pass

driver = uc.Chrome(
    version_main=152,
    options=options
)

wait = WebDriverWait(driver, 20)


try:

    # ============================================================
    # STEP 0
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 0 — HOME PAGE")
    print("=" * 70)

    driver.get(HOME_URL)

    wait.until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    print("Page title :", driver.title)
    print("Current URL:", driver.current_url)


    # ============================================================
    # STEP 1
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 1 — OPEN ADD A NEW BUSINESS")
    print("=" * 70)

    add_business_xpath = (
        "//a[contains("
        "translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'add a new business'"
        ")]"
    )

    add_business = WebDriverWait(driver, 20).until(
        lambda d: first_visible(d, add_business_xpath)
    )

    print("[PASS] Add a New Business link found.")
    print("Text :", add_business.text)
    print("Href :", add_business.get_attribute("href"))

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        add_business
    )

    time.sleep(0.5)

    driver.execute_script(
        "arguments[0].click();",
        add_business
    )

    wait.until(
        lambda d: "/add-business" in d.current_url
    )

    print("[OK] Add Business page opened.")
    print("Current URL:", driver.current_url)


    # ============================================================
    # STEP 2
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 2 — SELECT CATEGORY")
    print("=" * 70)

    category_trigger_xpath = "//input[@placeholder='Select category']"

    category_trigger = WebDriverWait(driver, 20).until(
        lambda d: first_visible(d, category_trigger_xpath)
    )

    print("[PASS] Category input detected.")
    print("Value before:", category_trigger.get_attribute("value"))


    # ============================================================
    # STEP 3
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 3 — SEARCH CATEGORY")
    print("=" * 70)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        category_trigger
    )

    time.sleep(0.5)

    driver.execute_script(
        "arguments[0].click();",
        category_trigger
    )

    time.sleep(1)

    category_search_xpath = (
        "//input["
        "contains("
        "translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'type to search categories'"
        ")"
        "]"
    )

    category_search = WebDriverWait(driver, 20).until(
        lambda d: first_visible_enabled(d, category_search_xpath)
    )

    category_search.send_keys("Education")

    print("[PASS] Category search entered: Education")


    # ============================================================
    # STEP 4
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 4 — FIND CATEGORY RESULTS")
    print("=" * 70)

    time.sleep(1.5)

    category_buttons_xpath = "//div[@role='button']"

    def find_educational_service_buttons(driver):
        buttons = driver.find_elements(
            By.XPATH,
            category_buttons_xpath
        )

        matches = []

        for button in buttons:

            if not button.is_displayed():
                continue

            text = button.text.strip()

            if not text:
                continue

            normalized = " ".join(text.lower().split())

            if "educational services" in normalized:
                matches.append(button)

        return matches

    educational_candidates = WebDriverWait(driver, 20).until(
        lambda d: find_educational_service_buttons(d) or False
    )

    print(
        "[PASS] Educational Services candidates visible:",
        len(educational_candidates)
    )


    # ============================================================
    # STEP 5
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 5 — SELECT EDUCATIONAL SERVICES")
    print("=" * 70)

    selected_category = None

    for candidate in educational_candidates:

        lines = [
            line.strip()
            for line in candidate.text.splitlines()
            if line.strip()
        ]

        if not lines:
            continue

        if lines[0].lower() == "educational services":
            selected_category = candidate
            break

    if selected_category is None:
        selected_category = educational_candidates[0]

    print("Selected text:")
    print(selected_category.text)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        selected_category
    )

    time.sleep(0.5)

    driver.execute_script(
        "arguments[0].click();",
        selected_category
    )

    print("[OK] Category clicked.")


    # ============================================================
    # STEP 6
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 6 — VERIFY CATEGORY")
    print("=" * 70)

    category_value = WebDriverWait(driver, 15).until(
        lambda d: first_visible(d, category_trigger_xpath)
    ).get_attribute("value")

    print("Category field value:", category_value)

    if category_value == CATEGORY:
        print("[PASS] Category verified.")
    else:
        print("[WARNING] Category value differs from expected.")


    # ============================================================
    # STEP 7
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 7 — SELECT COUNTRY")
    print("=" * 70)

    country_button_xpath = "//button[normalize-space()='Select country']"

    country_button = WebDriverWait(driver, 20).until(
        lambda d: first_visible_enabled(d, country_button_xpath)
    )

    print("[PASS] Select country button found.")
    print("Current text:", country_button.text)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        country_button
    )

    time.sleep(0.5)

    driver.execute_script(
        "arguments[0].click();",
        country_button
    )

    time.sleep(1)


    # ============================================================
    # STEP 8
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 8 — SEARCH COUNTRY")
    print("=" * 70)

    country_search_xpath = (
        "//input["
        "contains("
        "translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'search countries'"
        ")"
        "]"
    )

    country_search = WebDriverWait(driver, 20).until(
        lambda d: first_visible_enabled(d, country_search_xpath)
    )

    country_search.send_keys("India")

    print("[PASS] India search entered.")


    # ============================================================
    # STEP 9
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 9 — FIND INDIA")
    print("=" * 70)

    india_xpath = (
        "//*[@role='option']["
        "normalize-space(.)='India'"
        "]"
    )

    india_results = WebDriverWait(driver, 20).until(
        lambda d: visible_elements(d, india_xpath)
    )

    print("Visible India results:", len(india_results))

    if len(india_results) == 1:
        print("[PASS] Exactly one India result found.")
    else:
        print("[WARNING] India result count:", len(india_results))


    # ============================================================
    # STEP 10
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 10 — SELECT INDIA")
    print("=" * 70)

    india_option = india_results[0]

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        india_option
    )

    time.sleep(0.5)

    driver.execute_script(
        "arguments[0].click();",
        india_option
    )

    time.sleep(1)

    print("[OK] India selected.")


    # ============================================================
    # STEP 11
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 11 — VERIFY COUNTRY")
    print("=" * 70)

    selected_country_xpath = (
        "//button[@role='combobox']["
        "normalize-space(.)='India'"
        "]"
    )

    selected_country = WebDriverWait(driver, 15).until(
        lambda d: first_visible(d, selected_country_xpath)
    )

    print("Country control value:", selected_country.text)

    if selected_country.text.strip() == COUNTRY:
        print("[PASS] Country verified.")
    else:
        print("[WARNING] Country differs from expected.")


    # ============================================================
    # STEP 12
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 12 — VERIFY BUSINESS NAME")
    print("=" * 70)

    business_name_xpath = "//input[@name='name']"

    business_name = WebDriverWait(driver, 15).until(
        lambda d: first_visible_enabled(d, business_name_xpath)
    )

    business_name.clear()
    business_name.send_keys(PRODUCT_NAME)

    if business_name.get_attribute("value") == PRODUCT_NAME:
        print(
            "[PASS] Business Name verified:",
            business_name.get_attribute("value")
        )
    else:
        print("[WARNING] Business Name mismatch.")


    # ============================================================
    # STEP 13
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 13 — VERIFY EMAIL")
    print("=" * 70)

    email_xpath = "//input[@name='email']"

    email_field = WebDriverWait(driver, 15).until(
        lambda d: first_visible_enabled(d, email_xpath)
    )

    email_field.clear()
    email_field.send_keys(EMAIL)

    if email_field.get_attribute("value") == EMAIL:
        print(
            "[PASS] Email verified:",
            email_field.get_attribute("value")
        )
    else:
        print("[WARNING] Email mismatch.")


    # ============================================================
    # STEP 14
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 14 — VERIFY WEBSITE")
    print("=" * 70)

    website_xpath = "//input[@name='website']"

    website_field = WebDriverWait(driver, 15).until(
        lambda d: first_visible_enabled(d, website_xpath)
    )

    website_field.clear()
    website_field.send_keys(WEBSITE)

    if website_field.get_attribute("value") == WEBSITE:
        print(
            "[PASS] Website verified:",
            website_field.get_attribute("value")
        )
    else:
        print("[WARNING] Website mismatch.")


    # ============================================================
    # STEP 15
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 15 — DISPLAY WEBSITE")
    print("=" * 70)

    display_website_xpath = "//input[@name='display_website']"

    display_website = first_visible_enabled(
        driver,
        display_website_xpath
    )

    if display_website:

        display_website.clear()
        display_website.send_keys(WEBSITE)

        if display_website.get_attribute("value") == WEBSITE:
            print(
                "[PASS] Display Website verified:",
                display_website.get_attribute("value")
            )
        else:
            print("[WARNING] Display Website mismatch.")

    else:
        print("[INFO] Display Website field not available.")


    # ============================================================
    # STEP 16
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 16 — CHECK OPTIONAL FIELDS")
    print("=" * 70)

    optional_fields = [
        ("Address", "//textarea[@name='address']"),
        ("City", "//input[@name='city']"),
        ("Zip Code", "//input[@name='zip_code']"),
        ("Phone", "//input[@name='phone']"),
        ("Mobile", "//input[@name='mobile']"),
        ("Fax", "//input[@name='fax']"),
        ("Blog", "//input[@name='blog']"),
        ("Twitter", "//input[@name='twitter']"),
        ("Facebook", "//input[@name='facebook']"),
        ("Instagram", "//input[@name='instagram']"),
        ("LinkedIn", "//input[@name='linkedin']"),
        ("TikTok", "//input[@name='tiktok']"),
        ("Video", "//input[@name='skype']"),
        ("Instant Messenger", "//input[@name='im']")
    ]

    for label, xpath in optional_fields:

        element = first_visible(driver, xpath)

        if element:
            print(f"{label} available (left unchanged)")
        else:
            print(f"{label} not visible")


    # ============================================================
    # STEP 17 — OPEN BUSINESS TAGS
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 17 — OPEN BUSINESS TAGS")
    print("=" * 70)

    business_tags_xpath = (
        "//div[@role='combobox']["
        "normalize-space(.)='Select business tags'"
        "]"
    )

    business_tags = WebDriverWait(driver, 15).until(
        lambda d: first_visible(d, business_tags_xpath)
    )

    print("[PASS] Business Tags control detected.")
    print("Current text:", business_tags.text)

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        business_tags
    )

    time.sleep(0.5)

    driver.execute_script(
        "arguments[0].click();",
        business_tags
    )

    time.sleep(1)

    print("[OK] Business Tags control opened.")


    # ============================================================
    # STEP 18 — FIND TAG SEARCH
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 18 — FIND BUSINESS TAG SEARCH")
    print("=" * 70)

    tag_search_xpath = (
        "//input["
        "normalize-space(@placeholder)="
        "'Search or type to create...'"
        "]"
    )

    tag_search = WebDriverWait(driver, 15).until(
        lambda d: first_visible_enabled(d, tag_search_xpath)
    )

    print("[PASS] Business Tags search input detected.")
    print(
        "Placeholder:",
        tag_search.get_attribute("placeholder")
    )


    # ============================================================
    # STEP 19 — MAP AVAILABLE TAGS
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 19 — MAP BROWNBOOK BUSINESS TAGS")
    print("=" * 70)

    all_results = {}

    for search_term in TAG_SEARCHES:

        print("\n" + "-" * 60)
        print(f"SEARCH TERM: {search_term}")
        print("-" * 60)

        try:

            tag_search = WebDriverWait(driver, 10).until(
                lambda d: first_visible_enabled(
                    d,
                    tag_search_xpath
                )
            )

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                tag_search
            )

            tag_search.click()

            # Use CTRL+A through JavaScript-free keyboard actions.
            tag_search.clear()

            tag_search.send_keys(search_term)

            time.sleep(1.2)

            option_xpath = "//*[@role='option']"

            options_found = visible_elements(
                driver,
                option_xpath
            )

            # Remove blank values and duplicate text.
            unique_options = []

            for option in options_found:

                text = option.text.strip()

                if not text:
                    continue

                if text not in unique_options:
                    unique_options.append(text)

            all_results[search_term] = unique_options

            print(
                "Brownbook results:",
                len(unique_options)
            )

            if unique_options:

                for index, text in enumerate(
                    unique_options,
                    start=1
                ):
                    print(
                        f"{index}. {text}"
                    )

            else:

                print(
                    "[NONE] No visible Brownbook tag "
                    "suggestions for this search."
                )

        except Exception as e:

            all_results[search_term] = []

            print(
                "[ERROR] Search failed:",
                type(e).__name__
            )

        time.sleep(0.5)


    # ============================================================
    # STEP 20 — FINAL TAG MAP
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 20 — FINAL BROWNBOOK TAG MAP")
    print("=" * 70)

    found_any = False

    for search_term, results in all_results.items():

        print(f"\n[{search_term}]")

        if results:

            found_any = True

            for result in results:
                print(" -", result)

        else:

            print(" - No matching suggestions")


    if found_any:
        print("\n[PASS] Brownbook tag suggestions successfully mapped.")
    else:
        print("\n[INFO] No matching suggestions were returned.")


    # ============================================================
    # STEP 21 — DO NOT SELECT TAGS
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 21 — TAG SELECTION")
    print("=" * 70)

    print("[STOP] No Business Tag was selected.")
    print("[STOP] No custom tag was created.")
    print("[STOP] Tag mapping only.")


    # ============================================================
    # STEP 22 — LOCATION TAGS
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 22 — LOCATION TAGS")
    print("=" * 70)

    location_tags_xpath = (
        "//div[@role='combobox']["
        "normalize-space(.)='Select location tags'"
        "]"
    )

    location_tags = first_visible(
        driver,
        location_tags_xpath
    )

    if location_tags:

        print("[PASS] Location Tags control detected.")
        print("[STOP] Location Tags NOT filled.")
        print("[STOP] No location information invented.")

    else:

        print("[INFO] Location Tags control not visible.")


    # ============================================================
    # STEP 23 — VERIFY CORE VALUES
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 23 — VERIFY CORE VALUES")
    print("=" * 70)

    final_business_name = business_name.get_attribute("value")
    final_email = email_field.get_attribute("value")
    final_website = website_field.get_attribute("value")

    if display_website:
        final_display_website = display_website.get_attribute("value")
    else:
        final_display_website = ""

    print("Business Name :", final_business_name)
    print("Email         :", final_email)
    print("Website       :", final_website)
    print("Display Web   :", final_display_website)
    print("Category      :", category_value)
    print("Country       :", selected_country.text)


    # ============================================================
    # STEP 24 — STOP
    # ============================================================

    print("\n" + "=" * 70)
    print("STEP 24 — STOP BEFORE SUBMISSION")
    print("=" * 70)

    print("[STOP] Next button NOT clicked.")
    print("[STOP] No submission made.")
    print("[STOP] No final Submit action performed.")


    # ============================================================
    # FINAL STATUS
    # ============================================================

    print("\n" + "=" * 70)
    print("BROWNBOOK MAPPING STATUS")
    print("=" * 70)

    if final_business_name == PRODUCT_NAME:
        print("[PASS] Business Name verified")
    else:
        print("[FAIL] Business Name verification")

    if final_email == EMAIL:
        print("[PASS] Email verified")
    else:
        print("[FAIL] Email verification")

    if final_website == WEBSITE:
        print("[PASS] Website verified")
    else:
        print("[FAIL] Website verification")

    if category_value == CATEGORY:
        print("[PASS] Category verified")
    else:
        print("[FAIL] Category verification")

    if selected_country.text.strip() == COUNTRY:
        print("[PASS] Country verified")
    else:
        print("[FAIL] Country verification")

    print("[PASS] Business Tags mapped without selection")
    print("[PASS] Location Tags left untouched")
    print("[PASS] Next not clicked")
    print("[PASS] No submission made")

    print("\nBROWNBOOK TAG MAPPING COMPLETE")


    # ============================================================
    # KEEP BROWSER OPEN
    # ============================================================

    print("\n" + "=" * 70)
    print("BROWSER LEFT OPEN FOR INSPECTION")
    print("=" * 70)

    input("Press ENTER to close the browser...")


finally:

    try:
        driver.quit()
    except Exception:
        pass