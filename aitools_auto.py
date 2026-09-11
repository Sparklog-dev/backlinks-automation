from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import undetected_chromedriver as uc


# Prevent harmless WinError 6 cleanup noise
uc.Chrome.__del__ = lambda self: None


# ==========================================
# DATA
# ==========================================

TOOL_NAME = "Y2Map"
WEBSITE_URL = "https://y2map.com"

FIRST_NAME = "Nikhil"
LAST_NAME = "Savant"
EMAIL = "sparklog.marketing@gmail.com"


# ==========================================
# BROWSER SETUP
# ==========================================

options = Options()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

wait = WebDriverWait(driver, 20)


try:

    print("\n==========================================")
    print("AI TOOLS - FULL 3 PAGE AUTOMATION")
    print("==========================================\n")

    # ==========================================
    # 1. OPEN AI TOOLS HOMEPAGE
    # ==========================================

    print("Opening AI Tools homepage...")

    driver.get("https://aitools.inc/")
    time.sleep(3)

    print("Current URL:", driver.current_url)

    # ==========================================
    # 2. FIND VISIBLE SUBMIT TOOL
    # ==========================================

    print("\n========== HOMEPAGE ==========")

    submit_links = driver.find_elements(
        By.XPATH,
        "//a[contains(normalize-space(.), 'Submit Tool')]"
    )

    visible_submit_links = [
        link for link in submit_links
        if link.is_displayed()
    ]

    print(
        "Visible Submit Tool links:",
        len(visible_submit_links)
    )

    if not visible_submit_links:
        raise Exception(
            "No visible Submit Tool link found."
        )

    submit_link = visible_submit_links[0]

    print(
        "Clicking visible Submit Tool:",
        repr(submit_link.text)
    )

    print(
        "Href:",
        submit_link.get_attribute("href")
    )

    submit_link.click()

    time.sleep(3)

    print("Current URL:", driver.current_url)

    # ==========================================
    # 3. FIND FREE SUBMIT NOW
    # ==========================================

    print("\n========== FREE LISTING ==========")

    submit_now_links = driver.find_elements(
        By.XPATH,
        "//a[contains(normalize-space(.), 'Submit Now')]"
    )

    visible_submit_now = [
        link for link in submit_now_links
        if link.is_displayed()
    ]

    print(
        "Visible Submit Now links:",
        len(visible_submit_now)
    )

    for i, link in enumerate(
        visible_submit_now,
        start=1
    ):
        print(
            i,
            "| Text:",
            repr(link.text),
            "| Href:",
            link.get_attribute("href")
        )

    if not visible_submit_now:
        raise Exception(
            "No visible Submit Now link found."
        )

    # First Submit Now is the FREE listing
    free_submit = visible_submit_now[0]

    free_href = free_submit.get_attribute("href")

    print("\nUsing FREE Typeform:")
    print(free_href)

    driver.get(free_href)

    time.sleep(4)

    # ==========================================
    # 4. TYPEFORM
    # ==========================================

    print("\n========== TYPEFORM ==========")

    print("Current URL:", driver.current_url)
    print("Title:", driver.title)

    # ==========================================
    # PAGE 1
    # ==========================================

    print("\n==========================================")
    print("PAGE 1")
    print("==========================================")

    page1_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//div[@data-qa-focused='true']//input[@placeholder='Type your answer here...']"
            )
        )
    )

    print("Page 1 input FOUND.")

    page1_input.click()
    page1_input.clear()
    page1_input.send_keys(TOOL_NAME)

    page1_value = page1_input.get_attribute(
        "value"
    )

    print(
        "Page 1 value:",
        repr(page1_value)
    )

    if page1_value == TOOL_NAME:
        print("Tool Name: PASS")
    else:
        print("Tool Name: FAIL")

    # ==========================================
    # PAGE 1 OK
    # ==========================================

    print("\n========== PAGE 1 OK ==========")

    page1_ok = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[@data-qa='ok-button-visible deep-purple-ok-button-visible' and @aria-label='OK Next question']"
            )
        )
    )

    print("Page 1 OK button FOUND.")

    page1_ok.click()

    time.sleep(2)

    print("Page 1 OK clicked.")

    # ==========================================
    # PAGE 2
    # ==========================================

    print("\n==========================================")
    print("PAGE 2")
    print("==========================================")

    page2_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//div[@data-qa-focused='true']//input[@type='url' and @placeholder='https://']"
            )
        )
    )

    print("Page 2 website field FOUND.")

    page2_input.click()
    page2_input.clear()
    page2_input.send_keys(WEBSITE_URL)

    page2_value = page2_input.get_attribute(
        "value"
    )

    print(
        "Page 2 value:",
        repr(page2_value)
    )

    if page2_value == WEBSITE_URL:
        print("Website URL: PASS")
    else:
        print("Website URL: FAIL")

    # ==========================================
    # PAGE 2 OK
    # ==========================================

    print("\n========== PAGE 2 OK ==========")

    page2_ok = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//div[@data-qa-focused='true']//button[@data-qa='ok-button-visible deep-purple-ok-button-visible' and @aria-label='OK Next question']"
            )
        )
    )

    print("Page 2 OK button FOUND.")

    page2_ok.click()

    time.sleep(5)

    print("Page 2 OK clicked.")

    # ==========================================
    # PAGE 3
    # ==========================================

    print("\n==========================================")
    print("PAGE 3")
    print("==========================================")

    # ------------------------------------------
    # FIRST NAME
    # ------------------------------------------

    first_name_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@name='given-name']"
            )
        )
    )

    print("First name field FOUND.")

    first_name_input.click()
    first_name_input.clear()
    first_name_input.send_keys(FIRST_NAME)

    first_name_value = first_name_input.get_attribute(
        "value"
    )

    print(
        "First name:",
        repr(first_name_value)
    )

    # ------------------------------------------
    # LAST NAME
    # ------------------------------------------

    last_name_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@name='family-name']"
            )
        )
    )

    print("Last name field FOUND.")

    last_name_input.click()
    last_name_input.clear()
    last_name_input.send_keys(LAST_NAME)

    last_name_value = last_name_input.get_attribute(
        "value"
    )

    print(
        "Last name:",
        repr(last_name_value)
    )

    # ------------------------------------------
    # EMAIL
    # ------------------------------------------

    email_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@name='email']"
            )
        )
    )

    print("Email field FOUND.")

    email_input.click()
    email_input.clear()
    email_input.send_keys(EMAIL)

    email_value = email_input.get_attribute(
        "value"
    )

    print(
        "Email:",
        repr(email_value)
    )

    # ==========================================
    # PAGE 3 VERIFICATION
    # ==========================================

    print("\n========== PAGE 3 VERIFICATION ==========")

    if first_name_value == FIRST_NAME:
        print("First Name: PASS")
    else:
        print("First Name: FAIL")

    if last_name_value == LAST_NAME:
        print("Last Name: PASS")
    else:
        print("Last Name: FAIL")

    if email_value == EMAIL:
        print("Email: PASS")
    else:
        print("Email: FAIL")

    # ==========================================
    # FINAL SUBMIT BUTTON CHECK
    # ==========================================

    print("\n========== FINAL SUBMIT CHECK ==========")

    submit_button = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//button[@data-qa='submit-button deep-purple-submit-button' and @aria-label='Submit answers']"
            )
        )
    )

    print("Final Submit button FOUND.")
    print(
        "Button text:",
        repr(submit_button.text)
    )
    print(
        "Button enabled:",
        submit_button.is_enabled()
    )

    # ==========================================
    # FINAL VERIFICATION
    # ==========================================

    print("\n==========================================")
    print("AUTOMATION COMPLETE")
    print("==========================================")

    print("Page 1: Y2Map entered.")
    print("Page 1: OK clicked.")
    print("Page 2: https://y2map.com entered.")
    print("Page 2: OK clicked.")
    print("Page 3: Nikhil entered.")
    print("Page 3: Savant entered.")
    print("Page 3: Email entered.")

    print("\n========== RESULTS ==========")

    print(
        "Tool Name:",
        "PASS" if page1_value == TOOL_NAME else "FAIL"
    )

    print(
        "Website:",
        "PASS" if page2_value == WEBSITE_URL else "FAIL"
    )

    print(
        "First Name:",
        "PASS" if first_name_value == FIRST_NAME else "FAIL"
    )

    print(
        "Last Name:",
        "PASS" if last_name_value == LAST_NAME else "FAIL"
    )

    print(
        "Email:",
        "PASS" if email_value == EMAIL else "FAIL"
    )

    print(
        "Final Submit Button:",
        "FOUND"
    )

    print(
        "Final Submit Button Enabled:",
        submit_button.is_enabled()
    )

    print("\n==========================================")
    print("SAFE STOP")
    print("==========================================")

    print("FORM FULLY POPULATED.")
    print("NO FINAL SUBMISSION MADE.")

    print("\nBrowser will remain open.")

    input("\nPress ENTER to close the browser...")


finally:

    try:
        driver.quit()
    except Exception:
        pass