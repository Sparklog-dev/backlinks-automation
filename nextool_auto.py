import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Prevent WinError 6 cleanup noise
uc.Chrome.__del__ = lambda self: None


# =========================
# Y2MAP DATA
# =========================

TOOL_NAME = "Y2Map"

WEBSITE = "https://y2map.com"

CATEGORY = "Education"

EMAIL = "sparklog.marketing@gmail.com"

DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that transforms "
    "YouTube videos and PDFs into easy-to-understand visual mind maps. "
    "It helps students, researchers, educators, and lifelong learners "
    "understand, organize, review, and remember complex information faster."
)


# =========================
# BROWSER SETUP
# =========================

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

wait = WebDriverWait(driver, 20)


try:

    # =========================
    # 1. OPEN HOMEPAGE
    # =========================

    print("Opening Nextool.ai homepage...")

    driver.get("https://nextool.ai/")

    time.sleep(5)

    print(
        "Current URL:",
        driver.current_url
    )


    # =========================
    # 2. FIND VISIBLE SUBMIT LINK
    # =========================

    print("\n========== HOMEPAGE SUBMIT LINK ==========")

    # XPath ONLY
    links = driver.find_elements(
        By.XPATH,
        "//a"
    )

    submit_links = []

    for link in links:

        if not link.is_displayed():
            continue

        text = link.text.strip().lower()

        if "submit" in text:

            submit_links.append(link)

            print(
                "Link text:",
                link.text.strip()
            )

            print(
                "Link href:",
                link.get_attribute("href")
            )


    print(
        "Visible submit links:",
        len(submit_links)
    )


    if not submit_links:

        print(
            "ERROR: No visible Submit link found."
        )

        input(
            "Press Enter to close..."
        )

        raise SystemExit


    # =========================
    # 3. CLICK HOMEPAGE LINK
    # =========================

    submit_link = submit_links[0]

    print(
        "\nClicking visible Submit link..."
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        submit_link
    )

    time.sleep(1)

    submit_link.click()

    time.sleep(5)

    print(
        "Current URL:",
        driver.current_url
    )


    # =========================
    # 4. FIND TOOL NAME
    # =========================

    tool_name_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='e.g. ChatGPT']"
            )
        )
    )

    print(
        "\nTool Name field found."
    )


    # =========================
    # 5. FIND WEBSITE URL
    # =========================

    website_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='https://yourtool.com']"
            )
        )
    )

    print(
        "Website URL field found."
    )


    # =========================
    # 6. FIND CATEGORY
    # =========================

    category_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='e.g. Image Generation, Productivity']"
            )
        )
    )

    print(
        "Category field found."
    )


    # =========================
    # 7. FIND LOGO URL
    # =========================

    logo_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@placeholder='https://yourtool.com/logo.png']"
            )
        )
    )

    print(
        "Logo URL field found."
    )


    # =========================
    # 8. FIND CONTACT EMAIL
    # =========================

    email_fields = driver.find_elements(
        By.XPATH,
        "//input[@type='email']"
    )

    print(
        "\nEmail fields found:",
        len(email_fields)
    )

    for i, field in enumerate(
        email_fields,
        start=1
    ):

        print(
            f"Email {i}: "
            f"placeholder={field.get_attribute('placeholder')} | "
            f"displayed={field.is_displayed()}"
        )


    # Select the email with placeholder "you@example.com"

    email_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//input[@type='email' and "
                "@placeholder='you@example.com']"
            )
        )
    )

    print(
        "Contact email field found."
    )


    # =========================
    # 9. FIND DESCRIPTION
    # =========================

    description_field = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//textarea[@placeholder=\"Describe what this tool does, who it's for, and what makes it unique...\"]"
            )
        )
    )

    print(
        "Description field found."
    )


    # =========================
    # 10. FILL TOOL NAME
    # =========================

    tool_name_field.clear()

    tool_name_field.send_keys(
        TOOL_NAME
    )

    print(
        "Tool Name:",
        tool_name_field.get_attribute("value")
    )


    # =========================
    # 11. FILL WEBSITE
    # =========================

    website_field.clear()

    website_field.send_keys(
        WEBSITE
    )

    print(
        "Website:",
        website_field.get_attribute("value")
    )


    # =========================
    # 12. FILL CATEGORY
    # =========================

    category_field.clear()

    category_field.send_keys(
        CATEGORY
    )

    print(
        "Category:",
        category_field.get_attribute("value")
    )


    # =========================
    # 13. LEAVE LOGO EMPTY
    # =========================

    print(
        "Logo URL: left empty (optional)"
    )


    # =========================
    # 14. FILL EMAIL
    # =========================

    email_field.clear()

    email_field.send_keys(
        EMAIL
    )

    print(
        "Contact Email:",
        email_field.get_attribute("value")
    )


    # =========================
    # 15. FILL DESCRIPTION
    # =========================

    description_field.clear()

    description_field.send_keys(
        DESCRIPTION
    )

    print(
        "Description length:",
        len(
            description_field.get_attribute("value")
        )
    )


    # =========================
    # 16. VERIFY NEWSLETTER EMAIL
    # =========================

    newsletter_field = driver.find_element(
        By.XPATH,
        "//input[@type='email' and "
        "@placeholder='Enter your email']"
    )

    print(
        "Newsletter email field:",
        "EMPTY"
        if not newsletter_field.get_attribute("value")
        else "NOT EMPTY"
    )


    # =========================
    # 17. FINAL VERIFICATION
    # =========================

    print(
        "\n========== FINAL VERIFICATION =========="
    )

    actual_name = (
        tool_name_field.get_attribute("value")
    )

    actual_website = (
        website_field.get_attribute("value")
    )

    actual_category = (
        category_field.get_attribute("value")
    )

    actual_email = (
        email_field.get_attribute("value")
    )

    actual_description = (
        description_field.get_attribute("value")
    )


    print(
        "Tool Name:",
        "PASS"
        if actual_name == TOOL_NAME
        else "FAIL"
    )

    print(
        "Website:",
        "PASS"
        if actual_website == WEBSITE
        else "FAIL"
    )

    print(
        "Category:",
        "PASS"
        if actual_category == CATEGORY
        else "FAIL"
    )

    print(
        "Email:",
        "PASS"
        if actual_email == EMAIL
        else "FAIL"
    )

    print(
        "Description:",
        "PASS"
        if actual_description == DESCRIPTION
        else "FAIL"
    )

    print(
        "Description length:",
        len(actual_description)
    )

    print(
        "Logo:",
        "EMPTY"
        if not logo_field.get_attribute("value")
        else "FILLED"
    )

    print(
        "Newsletter:",
        "EMPTY"
        if not newsletter_field.get_attribute("value")
        else "FILLED"
    )


    # =========================
    # 18. FIND FREE SUBMIT BUTTON
    # =========================

    print(
        "\nFinding free submission button..."
    )

    submit_button = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//button[@type='submit' and "
                "contains(normalize-space(.), "
                "'Submit for Free Review')]"
            )
        )
    )

    print(
        "Button text:",
        submit_button.text.strip()
    )

    print(
        "Button enabled:",
        submit_button.is_enabled()
    )


    # =========================
    # SAFE STOP
    # =========================

    print(
        "\n========================================"
    )

    print(
        "MAPPING COMPLETE"
    )

    print(
        "FORM POPULATED"
    )

    print(
        "NO SUBMISSION MADE"
    )

    print(
        "========================================"
    )

    input(
        "\nPress Enter to close the browser..."
    )


finally:

    try:
        driver.quit()
    except Exception:
        pass