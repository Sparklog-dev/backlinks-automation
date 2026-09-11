from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import undetected_chromedriver as uc
import time


# ============================================================
# BROWSER SETUP
# ============================================================

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

# Prevent WinError 6 cleanup noise
uc.Chrome.__del__ = lambda self: None

wait = WebDriverWait(driver, 20)


# ============================================================
# Y2MAP DATA
# ============================================================

TOOL_NAME = "Y2Map"

WEBSITE_URL = "https://y2map.com"

DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that transforms "
    "YouTube videos, PDFs, books, and research content into easy-to-understand "
    "visual mind maps. It helps students, researchers, educators, founders, "
    "engineers, and lifelong learners understand complex topics faster by "
    "organizing important ideas, concepts, summaries, references, and related "
    "information into a structured visual format."
)

CONTACT_NAME = "Nikhil"

CONTACT_EMAIL = "sparklog.marketing@gmail.com"


# ============================================================
# OPEN HOMEPAGE
# ============================================================

driver.get("https://listai.cc/")

print("Opened ListAi.cc homepage")

time.sleep(3)


# ============================================================
# FIND ACTUAL SUBMIT TOOL LINK
# ============================================================

submit_links = driver.find_elements(
    By.XPATH,
    "//a[contains(normalize-space(.), 'Submit Tool')]"
)

print(f"Found {len(submit_links)} Submit Tool link(s)")

visible_submit_links = [
    link
    for link in submit_links
    if link.is_displayed()
]

if not visible_submit_links:

    print("ERROR: No visible Submit Tool link found.")

    input("Press Enter to close the browser...")
    driver.quit()

    raise SystemExit


submit_link = visible_submit_links[0]

print("Clicking visible Submit Tool link")
print("Link text:", repr(submit_link.text))
print("Link href:", submit_link.get_attribute("href"))

driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    submit_link
)

time.sleep(1)

submit_link.click()


# ============================================================
# WAIT FOR SUBMISSION PAGE
# ============================================================

try:

    wait.until(
        lambda d: "/submit" in d.current_url.lower()
    )

except TimeoutException:

    print(
        "WARNING: URL did not change to /submit within timeout."
    )

time.sleep(3)

print()
print("Current URL:", driver.current_url)
print("Submission page opened")


# ============================================================
# HELPER: FIND INPUT AFTER LABEL
# ============================================================

def find_input_after_label(label_text):

    # Look for an exact label
    labels = driver.find_elements(
        By.XPATH,
        f"//label[normalize-space(.)='{label_text}']"
    )

    for label in labels:

        if not label.is_displayed():
            continue

        # Input inside label
        try:

            element = label.find_element(
                By.XPATH,
                ".//input"
            )

            if element.is_displayed():
                return element

        except NoSuchElementException:
            pass

        # Input immediately following label
        try:

            element = label.find_element(
                By.XPATH,
                "following::input[1]"
            )

            if element.is_displayed():
                return element

        except NoSuchElementException:
            pass

    return None


# ============================================================
# INSPECT FORM
# ============================================================

print()
print("Inspecting visible form fields...")

inputs = driver.find_elements(
    By.XPATH,
    "//input"
)

textareas = driver.find_elements(
    By.XPATH,
    "//textarea"
)

selects = driver.find_elements(
    By.XPATH,
    "//select"
)

print(f"Inputs found: {len(inputs)}")
print(f"Textareas found: {len(textareas)}")
print(f"Selects found: {len(selects)}")


# ============================================================
# TOOL NAME
# ============================================================

print()
print("Looking for Tool Name field...")

tool_name = None

# IMPORTANT:
# Do NOT use the generic name="name" here.
# That appears to be the Your Name field.

tool_name = find_input_after_label("Tool Name")


# Fallback based on placeholder / attributes,
# but NEVER use the generic name="name".

if tool_name is None:

    for element in driver.find_elements(
        By.XPATH,
        "//input"
    ):

        if not element.is_displayed():
            continue

        input_type = (
            element.get_attribute("type") or ""
        ).lower()

        if input_type not in ["text", ""]:
            continue

        placeholder = (
            element.get_attribute("placeholder") or ""
        ).lower()

        name_attr = (
            element.get_attribute("name") or ""
        ).lower()

        id_attr = (
            element.get_attribute("id") or ""
        ).lower()

        if (
            "tool" in placeholder
            or "tool" in name_attr
            or "tool" in id_attr
        ):

            tool_name = element
            break


if tool_name is None:

    print("ERROR: Could not locate Tool Name field.")

    input("Press Enter to close the browser...")
    driver.quit()

    raise SystemExit


tool_name.clear()
tool_name.send_keys(TOOL_NAME)

print("Filled Tool Name")


# ============================================================
# CATEGORY
# ============================================================

category = None

for select_element in selects:

    if not select_element.is_displayed():
        continue

    try:

        select = Select(select_element)

        options_list = [
            option.text.strip()
            for option in select.options
        ]

        if "Education & Research" in options_list:

            category = select_element
            break

    except Exception:
        pass


if category is None:

    print("ERROR: Could not locate Category dropdown.")

    input("Press Enter to close the browser...")
    driver.quit()

    raise SystemExit


category_select = Select(category)

print(
    "Category options:",
    [
        option.text.strip()
        for option in category_select.options
    ]
)

category_select.select_by_visible_text(
    "Education & Research"
)

print("Selected category: Education & Research")


# ============================================================
# WEBSITE URL
# ============================================================

print()
print("Looking for Website URL field...")

website = None

website = find_input_after_label("Website URL")

if website is None:

    for element in driver.find_elements(
        By.XPATH,
        "//input[@type='url']"
    ):

        if element.is_displayed():

            website = element
            break


if website is None:

    print("ERROR: Could not locate Website URL field.")

    input("Press Enter to close the browser...")
    driver.quit()

    raise SystemExit


website.clear()
website.send_keys(WEBSITE_URL)

print("Filled Website URL")


# ============================================================
# DESCRIPTION
# ============================================================

print()
print("Looking for Description field...")

description = None

description_labels = driver.find_elements(
    By.XPATH,
    "//label[normalize-space(.)='Description']"
)

for label in description_labels:

    if not label.is_displayed():
        continue

    try:

        textarea = label.find_element(
            By.XPATH,
            ".//following::textarea[1]"
        )

        if textarea.is_displayed():

            description = textarea
            break

    except NoSuchElementException:
        pass


# Fallback
if description is None:

    for textarea in driver.find_elements(
        By.XPATH,
        "//textarea"
    ):

        if textarea.is_displayed():

            description = textarea
            break


if description is None:

    print("ERROR: Could not locate Description field.")

    input("Press Enter to close the browser...")
    driver.quit()

    raise SystemExit


description.clear()
description.send_keys(DESCRIPTION)

print("Filled Description")


# ============================================================
# YOUR NAME
# ============================================================

print()
print("Looking for Your Name field...")

name_field = None

name_field = find_input_after_label("Your Name")


# Fallback specifically for the generic name field
# AFTER Tool Name has already been identified.

if name_field is None:

    try:

        candidate = driver.find_element(
            By.XPATH,
            "//input[@name='name']"
        )

        if (
            candidate.is_displayed()
            and candidate != tool_name
        ):

            name_field = candidate

    except NoSuchElementException:
        pass


if name_field:

    name_field.clear()
    name_field.send_keys(CONTACT_NAME)

    print(
        "Filled Your Name:",
        CONTACT_NAME
    )

else:

    print(
        "WARNING: Your Name field could not be located."
    )


# ============================================================
# EMAIL
# ============================================================

print()
print("Looking for Contact Email field...")

email_fields = [
    element
    for element in driver.find_elements(
        By.XPATH,
        "//input[@type='email']"
    )
    if element.is_displayed()
]

print(
    f"Email fields found: {len(email_fields)}"
)


if not email_fields:

    print("ERROR: No visible email field found.")

    input("Press Enter to close the browser...")
    driver.quit()

    raise SystemExit


contact_email_field = email_fields[0]

contact_email_field.clear()
contact_email_field.send_keys(CONTACT_EMAIL)

print("Filled Contact Email")


# ============================================================
# WAIT
# ============================================================

time.sleep(2)


# ============================================================
# FINAL FORM VERIFICATION
# ============================================================

print()
print("==========================================")
print("FINAL FORM VERIFICATION")
print("==========================================")

print(
    "Tool Name:",
    tool_name.get_attribute("value")
)

print(
    "Website:",
    website.get_attribute("value")
)

print(
    "Category:",
    category_select.first_selected_option.text.strip()
)

print(
    "Description Length:",
    len(description.get_attribute("value"))
)

print(
    "Description:",
    description.get_attribute("value")
)

if name_field:

    print(
        "Your Name:",
        name_field.get_attribute("value")
    )

print(
    "Contact Email:",
    contact_email_field.get_attribute("value")
)


# ============================================================
# FIELD SEPARATION CHECK
# ============================================================

print()
print("==========================================")
print("FIELD SEPARATION CHECK")
print("==========================================")

tool_value = tool_name.get_attribute("value")

if tool_value == TOOL_NAME:

    print("✓ Tool Name is correctly set to Y2Map")

else:

    print(
        "✗ ERROR: Tool Name is:",
        repr(tool_value)
    )


if name_field:

    name_value = name_field.get_attribute("value")

    if name_value == CONTACT_NAME:

        print("✓ Your Name is correctly set to Nikhil")

    else:

        print(
            "✗ ERROR: Your Name is:",
            repr(name_value)
        )


# ============================================================
# FINAL SUBMIT CHECK
# ============================================================

print()
print("==========================================")
print("FINAL SUBMIT CHECK")
print("==========================================")

submit_buttons = driver.find_elements(
    By.XPATH,
    "//button[contains(normalize-space(.), 'Submit Tool')]"
)

visible_submit_buttons = [
    button
    for button in submit_buttons
    if button.is_displayed()
]

if visible_submit_buttons:

    final_submit = visible_submit_buttons[-1]

    print(
        "Visible submit button:",
        repr(final_submit.text)
    )

    print(
        "Enabled:",
        final_submit.is_enabled()
    )

else:

    print(
        "WARNING: Submit Tool button not found."
    )


# ============================================================
# SAFE STOP
# ============================================================

print()
print("==========================================")
print("SAFE STOP")
print("==========================================")

print("Form has been filled.")
print("Tool Name and Your Name were handled separately.")
print("No submission was made.")
print("Final Submit Tool button was NOT clicked.")

print()
print("Browser will remain open.")
print("Press Enter to close the browser...")

input()

driver.quit()