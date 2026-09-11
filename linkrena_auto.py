import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# --------------------------------------------------
# Y2Map details
# --------------------------------------------------

TOOL_NAME = "Y2Map"

WEBSITE_URL = "https://y2map.com"

DESCRIPTION = "Turn YouTube videos and PDFs into clear visual mind maps."

EMAIL = "sparklog.marketing@gmail.com"


# --------------------------------------------------
# Chrome setup
# --------------------------------------------------

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

uc.Chrome.__del__ = lambda self: None

wait = WebDriverWait(driver, 20)


# --------------------------------------------------
# STEP 1 — Open homepage
# --------------------------------------------------

driver.get("https://linkrena.com/")

print("Opened Linkrena homepage")

time.sleep(3)


# --------------------------------------------------
# STEP 2 — Find visible Submit link
# --------------------------------------------------

submit_links = driver.find_elements(
    By.XPATH,
    "//a[contains(normalize-space(), 'Submit')]"
)

visible_submit_links = [
    link
    for link in submit_links
    if link.is_displayed()
]

print(
    f"Found {len(visible_submit_links)} visible Submit link(s)"
)

if not visible_submit_links:

    print("ERROR: Could not find visible Submit link")

    input("Press Enter to close the browser...")
    driver.quit()
    raise SystemExit


# Prefer the first visible Submit link
submit_link = visible_submit_links[0]

print("Clicking visible Submit link")

print(
    f"Link text: '{submit_link.text}'"
)

print(
    f"Link href: {submit_link.get_attribute('href')}"
)

driver.execute_script(
    "arguments[0].click();",
    submit_link
)


# --------------------------------------------------
# STEP 3 — Verify submission page
# --------------------------------------------------

wait.until(
    EC.url_contains("/submit")
)

print()
print("Current URL:", driver.current_url)
print("Submission page opened")

time.sleep(2)


# --------------------------------------------------
# STEP 4 — Inspect visible form fields
# --------------------------------------------------

print()
print("Inspecting visible form fields...")

inputs = [
    element
    for element in driver.find_elements(
        By.XPATH,
        "//input"
    )
    if element.is_displayed()
]

textareas = [
    element
    for element in driver.find_elements(
        By.XPATH,
        "//textarea"
    )
    if element.is_displayed()
]

selects = [
    element
    for element in driver.find_elements(
        By.XPATH,
        "//select"
    )
    if element.is_displayed()
]

print("Inputs found:", len(inputs))
print("Textareas found:", len(textareas))
print("Selects found:", len(selects))


# --------------------------------------------------
# STEP 5 — Print field details
# --------------------------------------------------

print()
print("Visible input details:")

for i, element in enumerate(inputs, start=1):

    print(
        f"{i}. "
        f"type={element.get_attribute('type')} | "
        f"name={element.get_attribute('name')} | "
        f"id={element.get_attribute('id')} | "
        f"placeholder={element.get_attribute('placeholder')}"
    )


# --------------------------------------------------
# STEP 6 — Product URL
# --------------------------------------------------

print()
print("Looking for Product URL field...")

url_field = driver.find_element(
    By.XPATH,
    "//input[@name='url']"
)

url_field.clear()
url_field.send_keys(WEBSITE_URL)

print("Filled Product URL")


# --------------------------------------------------
# STEP 7 — Tool Name
# --------------------------------------------------

print()
print("Looking for Tool Name field...")

name_field = driver.find_element(
    By.XPATH,
    "//input[@name='name']"
)

name_field.clear()
name_field.send_keys(TOOL_NAME)

print("Filled Tool Name")


# --------------------------------------------------
# STEP 8 — One-line description
# --------------------------------------------------

print()
print("Looking for One-line description field...")

tagline_field = driver.find_element(
    By.XPATH,
    "//input[@name='tagline']"
)

tagline_field.clear()
tagline_field.send_keys(DESCRIPTION)

print("Filled One-line description")

print(
    "Description length:",
    len(DESCRIPTION)
)


# --------------------------------------------------
# STEP 9 — Email
# --------------------------------------------------

print()
print("Looking for Email field...")

email_field = driver.find_element(
    By.XPATH,
    "//input[@name='email']"
)

email_field.clear()
email_field.send_keys(EMAIL)

print("Filled Email")


# --------------------------------------------------
# STEP 10 — Final verification
# --------------------------------------------------

print()
print("=" * 50)
print("FINAL FORM VERIFICATION")
print("=" * 50)

print(
    "Tool Name:",
    name_field.get_attribute("value")
)

print(
    "Website:",
    url_field.get_attribute("value")
)

print(
    "One-line description:",
    tagline_field.get_attribute("value")
)

print(
    "Description Length:",
    len(tagline_field.get_attribute("value"))
)

print(
    "Email:",
    email_field.get_attribute("value")
)


# --------------------------------------------------
# STEP 11 — Find final Submit button
# --------------------------------------------------

print()
print("=" * 50)
print("FINAL SUBMIT CHECK")
print("=" * 50)

buttons = driver.find_elements(
    By.XPATH,
    "//button"
)

visible_buttons = [
    button
    for button in buttons
    if button.is_displayed()
]

submit_button = None

for button in visible_buttons:

    text = (
        button.text or ""
    ).strip().lower()

    if "submit" in text:

        submit_button = button
        break


if submit_button:

    print(
        "Visible submit button:",
        repr(submit_button.text)
    )

    print(
        "Enabled:",
        submit_button.is_enabled()
    )

else:

    print(
        "WARNING: Could not find visible Submit button"
    )


# --------------------------------------------------
# SAFETY STOP
# --------------------------------------------------

print()
print("=" * 50)
print("SAFE STOP")
print("=" * 50)

print("Form has been filled.")
print("No submission was made.")
print("Final Submit button was NOT clicked.")

print()
print("Browser will remain open.")
print("Press Enter to close the browser...")

input()

driver.quit()