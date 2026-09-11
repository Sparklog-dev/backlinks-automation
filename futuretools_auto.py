import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# ==================================================
# Y2MAP DATA
# ==================================================

TOOL_NAME = "Y2Map"

WEBSITE_URL = "https://y2map.com/"

SHORT_DESCRIPTION = (
    "Turn YouTube videos and PDFs into clear visual mind maps."
)

CATEGORY = "Education"

PRICING = "Free"

SUBMITTER_NAME = "Nikhil"

EMAIL = "sparklog.marketing@gmail.com"


# ==================================================
# START BROWSER
# ==================================================

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

uc.Chrome.__del__ = lambda self: None

wait = WebDriverWait(driver, 20)


# ==================================================
# 1. OPEN HOMEPAGE
# ==================================================

driver.get("https://futuretools.io/")

print("Opened Future Tools homepage")

time.sleep(3)


# ==================================================
# 2. FIND VISIBLE SUBMIT A TOOL LINK
# ==================================================

submit_links = driver.find_elements(
    By.XPATH,
    "//a[contains(translate(normalize-space(), "
    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
    "'abcdefghijklmnopqrstuvwxyz'), 'submit a tool')]"
)

visible_submit_links = [
    link
    for link in submit_links
    if link.is_displayed()
]

print(
    f"Found {len(visible_submit_links)} visible Submit a Tool link(s)"
)

if not visible_submit_links:

    print("ERROR: Submit a Tool link not found.")

    input(
        "Press Enter to close the browser..."
    )

    driver.quit()

    raise SystemExit


# ==================================================
# 3. CLICK VISIBLE SUBMIT LINK
# ==================================================

submit_link = visible_submit_links[0]

print()
print("Clicking visible Submit a Tool link")

print(
    "Link text:",
    repr(submit_link.text)
)

print(
    "Link href:",
    submit_link.get_attribute("href")
)

driver.execute_script(
    "arguments[0].click();",
    submit_link
)

time.sleep(4)

print()
print("Current URL:", driver.current_url)


# ==================================================
# 4. FIND FORM FIELDS
# ==================================================

print()
print("=" * 50)
print("FINDING FORM FIELDS")
print("=" * 50)

name_field = wait.until(
    EC.visibility_of_element_located(
        (
            By.XPATH,
            "//input[@name='submitter_name']"
        )
    )
)

tool_name_field = wait.until(
    EC.visibility_of_element_located(
        (
            By.XPATH,
            "//input[@name='tool_name']"
        )
    )
)

url_field = wait.until(
    EC.visibility_of_element_located(
        (
            By.XPATH,
            "//input[@name='tool_url']"
        )
    )
)

description_field = wait.until(
    EC.visibility_of_element_located(
        (
            By.XPATH,
            "//textarea[@id='description']"
        )
    )
)

category_field = wait.until(
    EC.visibility_of_element_located(
        (
            By.XPATH,
            "//select[@name='category']"
        )
    )
)

email_field = wait.until(
    EC.visibility_of_element_located(
        (
            By.XPATH,
            "//input[@name='submitter_email']"
        )
    )
)

print("Your Name field: found")
print("Tool Name field: found")
print("Tool URL field: found")
print("Short Description field: found")
print("Category field: found")
print("Email field: found")


# ==================================================
# 5. FILL YOUR NAME
# ==================================================

print()
print("Filling Your Name...")

name_field.clear()
name_field.send_keys(SUBMITTER_NAME)

print(
    "Your Name:",
    name_field.get_attribute("value")
)


# ==================================================
# 6. FILL TOOL NAME
# ==================================================

print()
print("Filling Tool Name...")

tool_name_field.clear()
tool_name_field.send_keys(TOOL_NAME)

print(
    "Tool Name:",
    tool_name_field.get_attribute("value")
)


# ==================================================
# 7. FILL WEBSITE URL
# ==================================================

print()
print("Filling Tool URL...")

url_field.clear()
url_field.send_keys(WEBSITE_URL)

print(
    "Tool URL:",
    url_field.get_attribute("value")
)


# ==================================================
# 8. FILL SHORT DESCRIPTION
# ==================================================

print()
print("=" * 50)
print("FILLING SHORT DESCRIPTION")
print("=" * 50)

description_field.click()
description_field.clear()
description_field.send_keys(SHORT_DESCRIPTION)

time.sleep(0.5)

print(
    "Short Description:",
    description_field.get_attribute("value")
)

print(
    "Description Length:",
    len(
        description_field.get_attribute("value") or ""
    )
)


# ==================================================
# 9. SELECT CATEGORY
# ==================================================

print()
print("Selecting Category...")

category_select = Select(category_field)

print("Available categories:")

for option in category_select.options:

    text = option.text.strip()

    if text:
        print(" -", text)

category_select.select_by_visible_text(
    CATEGORY
)

print(
    "Selected Category:",
    category_select.first_selected_option.text
)


# ==================================================
# 10. SELECT PRICING
# ==================================================

print()
print("Selecting Pricing...")

pricing_radios = driver.find_elements(
    By.XPATH,
    "//input[@type='radio'][@name='pricing_tier']"
)

print(
    "Pricing radio buttons found:",
    len(pricing_radios)
)

for radio in pricing_radios:

    value = (
        radio.get_attribute("value")
        or ""
    ).strip()

    print(
        "Radio value:",
        repr(value)
    )


# Find the radio associated with Free.

free_radio = None

for radio in pricing_radios:

    value = (
        radio.get_attribute("value")
        or ""
    ).strip().lower()

    if value == "free":

        free_radio = radio
        break


if free_radio is None:

    print()
    print(
        "WARNING: Could not identify the Free pricing radio."
    )

else:

    driver.execute_script(
        "arguments[0].click();",
        free_radio
    )

    time.sleep(0.5)

    print(
        "Selected Pricing:",
        free_radio.get_attribute("value")
    )


# ==================================================
# 11. FILL EMAIL
# ==================================================

print()
print("Filling Email...")

email_field.click()
email_field.clear()
email_field.send_keys(EMAIL)

print(
    "Email:",
    email_field.get_attribute("value")
)


# ==================================================
# 12. NEWSLETTER
# ==================================================

print()
print("Checking Newsletter option...")

newsletter_boxes = driver.find_elements(
    By.XPATH,
    "//input[@type='checkbox' and @name='newsletter_opt_in']"
)

if newsletter_boxes:

    newsletter = newsletter_boxes[0]

    print(
        "Newsletter checkbox selected:",
        newsletter.is_selected()
    )

    # Intentionally leave unchecked.

    if newsletter.is_selected():

        newsletter.click()

    print(
        "Newsletter checkbox after check:",
        newsletter.is_selected()
    )

else:

    print(
        "Newsletter checkbox not found."
    )


# ==================================================
# 13. CAPTCHA CHECK
# ==================================================

print()
print("=" * 50)
print("CAPTCHA CHECK")
print("=" * 50)

page_text = driver.find_element(
    By.XPATH,
    "//body"
).text.lower()

if "captcha" in page_text:

    print(
        "CAPTCHA detected on the page."
    )

    print(
        "We will NOT attempt to bypass or solve it automatically."
    )

else:

    print(
        "No visible CAPTCHA text detected."
    )


# ==================================================
# 14. FINAL FORM VERIFICATION
# ==================================================

print()
print("=" * 50)
print("FINAL FORM VERIFICATION")
print("=" * 50)

print()
print("Your Name:")
print(
    name_field.get_attribute("value")
)

print()
print("Tool Name:")
print(
    tool_name_field.get_attribute("value")
)

print()
print("Tool URL:")
print(
    url_field.get_attribute("value")
)

print()
print("Short Description:")
print(
    description_field.get_attribute("value")
)

print(
    "Short Description Length:",
    len(
        description_field.get_attribute("value") or ""
    )
)

print()
print("Category:")
print(
    category_select.first_selected_option.text
)

print()
print("Email:")
print(
    email_field.get_attribute("value")
)

if free_radio is not None:

    print()
    print("Pricing:")

    print(
        "Free"
        if free_radio.is_selected()
        else "Free not selected"
    )


# ==================================================
# 15. CORRECTNESS CHECK
# ==================================================

print()
print("=" * 50)
print("CHECKING POPULATED VALUES")
print("=" * 50)

checks = {

    "Your Name":
        name_field.get_attribute("value")
        == SUBMITTER_NAME,

    "Tool Name":
        tool_name_field.get_attribute("value")
        == TOOL_NAME,

    "Tool URL":
        url_field.get_attribute("value")
        == WEBSITE_URL,

    "Short Description":
        description_field.get_attribute("value")
        == SHORT_DESCRIPTION,

    "Category":
        category_select.first_selected_option.text
        == CATEGORY,

    "Email":
        email_field.get_attribute("value")
        == EMAIL
}


if free_radio is not None:

    checks["Pricing"] = (
        free_radio.is_selected()
    )


all_correct = True

for field_name, result in checks.items():

    print(
        f"{field_name}: "
        f"{'PASS' if result else 'FAIL'}"
    )

    if not result:

        all_correct = False


# ==================================================
# 16. SUBMIT BUTTON CHECK ONLY
# ==================================================

print()
print("=" * 50)
print("SUBMIT BUTTON CHECK")
print("=" * 50)

submit_buttons = driver.find_elements(
    By.XPATH,
    "//button[@type='submit'] | //input[@type='submit']"
)

visible_submit_buttons = [
    button
    for button in submit_buttons
    if button.is_displayed()
]

for button in visible_submit_buttons:

    text = (
        button.text
        or button.get_attribute("value")
        or ""
    ).strip()

    print(
        f"Button: {repr(text)} | "
        f"Enabled: {button.is_enabled()}"
    )


# ==================================================
# 17. SAFE STOP
# ==================================================

print()
print("=" * 50)
print("SAFE STOP")
print("=" * 50)

if all_correct:

    print(
        "All mapped fields passed verification."
    )

else:

    print(
        "WARNING: One or more fields failed verification."
    )

print()
print("CAPTCHA was NOT bypassed.")
print("No submission was made.")
print("Submit button was NOT clicked.")

print()
print("Browser will remain open.")

input(
    "Press Enter to close the browser..."
)

driver.quit()