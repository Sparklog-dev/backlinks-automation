import os
import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# ==================================================
# Y2MAP DATA
# ==================================================

TOOL_NAME = "Y2Map"

WEBSITE_URL = "https://y2map.com"

TAGLINE = "Turn YouTube videos and PDFs into clear visual mind maps."

DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that transforms "
    "YouTube videos, PDFs, books, and research content into easy-to-understand "
    "visual mind maps. It helps students, researchers, educators, founders, "
    "engineers, and lifelong learners understand complex topics faster by "
    "organizing important ideas, concepts, summaries, references, and related "
    "information into a structured visual format."
)

EMAIL = "sparklog.marketing@gmail.com"

TAGS = "AI, mind maps, YouTube, PDF, education, learning, productivity"

LOGO_PATH = os.path.abspath("y2map_logo.png")


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

driver.get("https://www.switchtools.io/")

print("Opened SwitchTools homepage")

time.sleep(3)


# ==================================================
# 2. FIND VISIBLE SUBMIT TOOL LINK
# ==================================================

submit_links = driver.find_elements(
    By.XPATH,
    "//a[contains(translate(normalize-space(), "
    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
    "'abcdefghijklmnopqrstuvwxyz'), 'submit tool')]"
)

visible_submit_links = [
    link
    for link in submit_links
    if link.is_displayed()
]

print(
    f"Found {len(visible_submit_links)} visible Submit Tool link(s)"
)


if not visible_submit_links:

    print("ERROR: Submit Tool link not found")

    input("Press Enter to close the browser...")

    driver.quit()

    raise SystemExit


# ==================================================
# 3. CLICK SUBMIT TOOL
# ==================================================

submit_link = visible_submit_links[0]

print()
print("Clicking visible Submit Tool link")

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

time.sleep(3)

print()
print("Current URL:", driver.current_url)


# ==================================================
# 4. FIND FREE STARTER OPTION
# ==================================================

print()
print("=" * 50)
print("CHECKING LISTING PLAN")
print("=" * 50)


free_links = driver.find_elements(
    By.XPATH,
    "//*[self::a or self::button]"
    "[contains(translate(normalize-space(), "
    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', "
    "'abcdefghijklmnopqrstuvwxyz'), 'get free listing')]"
)

visible_free_links = [
    link
    for link in free_links
    if link.is_displayed()
]


print(
    "Visible Get Free Listing options:",
    len(visible_free_links)
)


if not visible_free_links:

    print(
        "ERROR: Could not find Get Free Listing option."
    )

    input("Press Enter to close the browser...")

    driver.quit()

    raise SystemExit


free_link = visible_free_links[0]

print(
    "Free option text:",
    repr(free_link.text)
)

print(
    "Free option href:",
    free_link.get_attribute("href")
)


# ==================================================
# 5. CLICK FREE STARTER
# ==================================================

print()
print("Clicking Get Free Listing...")

driver.execute_script(
    "arguments[0].click();",
    free_link
)

time.sleep(3)


# ==================================================
# 6. VERIFY PLAN USING FORM ELEMENTS
# ==================================================

print()
print("=" * 50)
print("VERIFYING SELECTED PLAN")
print("=" * 50)


# Inspect radios on the page
radio_inputs = driver.find_elements(
    By.XPATH,
    "//input[@type='radio']"
)

visible_radios = [
    radio
    for radio in radio_inputs
    if radio.is_displayed()
]


print(
    "Visible radio buttons:",
    len(visible_radios)
)


for i, radio in enumerate(
    visible_radios,
    start=1
):

    print(
        f"Radio {i}: "
        f"name={radio.get_attribute('name')} | "
        f"value={radio.get_attribute('value')} | "
        f"checked={radio.is_selected()}"
    )


# Read the page text around plan information
page_text = driver.find_element(
    By.TAG_NAME,
    "body"
).text

lower_text = page_text.lower()


print()
print("Plan-related text:")

for line in page_text.splitlines():

    line_lower = line.lower()

    if (
        "plan:" in line_lower
        or "starter listing" in line_lower
        or "verified listing" in line_lower
    ):

        print(
            line.strip()
        )


# ==================================================
# 7. SAFETY CHECK
# ==================================================

if (
    "plan: verified listing" in lower_text
    and "plan: starter" not in lower_text
):

    print()
    print("=" * 50)
    print("SAFETY STOP")
    print("=" * 50)

    print(
        "The page still appears to have the paid Verified plan."
    )

    print(
        "We will NOT continue filling the form."
    )

    print(
        "No payment was made."
    )

    print(
        "No submission was made."
    )

    input(
        "Press Enter to close the browser..."
    )

    driver.quit()

    raise SystemExit


# ==================================================
# 8. FIND FORM FIELDS
# ==================================================

print()
print("=" * 50)
print("FINDING FORM FIELDS")
print("=" * 50)


name_field = driver.find_element(
    By.NAME,
    "name"
)

url_field = driver.find_element(
    By.NAME,
    "link"
)

tagline_field = driver.find_element(
    By.NAME,
    "tagline"
)

description_field = driver.find_element(
    By.ID,
    "f-desc"
)

tags_field = driver.find_element(
    By.NAME,
    "tags"
)

email_field = driver.find_element(
    By.NAME,
    "email"
)

category_field = driver.find_element(
    By.NAME,
    "category_id"
)

pricing_field = driver.find_element(
    By.NAME,
    "pricing_model"
)

logo_field = driver.find_element(
    By.NAME,
    "logo"
)


print("Tool Name field: found")
print("Website URL field: found")
print("Tagline field: found")
print("Description field: found")
print("Tags field: found")
print("Email field: found")
print("Category field: found")
print("Pricing field: found")
print("Logo field: found")


# ==================================================
# 9. FILL BASIC FIELDS
# ==================================================

print()
print("=" * 50)
print("FILLING FORM")
print("=" * 50)


name_field.clear()
name_field.send_keys(TOOL_NAME)

print("Filled Tool Name")


url_field.clear()
url_field.send_keys(WEBSITE_URL)

print("Filled Website URL")


tagline_field.clear()
tagline_field.send_keys(TAGLINE)

print("Filled Tagline")

print(
    "Tagline length:",
    len(TAGLINE)
)


# ==================================================
# 10. DESCRIPTION
# ==================================================

print()
print("=" * 50)
print("FILLING DESCRIPTION")
print("=" * 50)

description_field = driver.find_element(
    By.ID,
    "f-desc"
)

print("Description field found")
print("Tag:", description_field.tag_name)
print("ID:", description_field.get_attribute("id"))
print("Name:", description_field.get_attribute("name"))


# Scroll the actual textarea into view
driver.execute_script(
    """
    arguments[0].scrollIntoView({
        block: 'center',
        inline: 'nearest'
    });
    """,
    description_field
)

time.sleep(1)


# Click the actual visible textarea
description_field.click()

time.sleep(0.3)


# Clear any existing text
description_field.clear()

time.sleep(0.2)


# Type the description like a real user
description_field.send_keys(
    DESCRIPTION
)

time.sleep(1)


print(
    "Description after typing:",
    repr(
        description_field.get_attribute("value")
    )
)

print(
    "Description length:",
    len(
        description_field.get_attribute("value") or ""
    )
)


# Move focus away so the site's normal blur/change handling runs
driver.execute_script(
    "arguments[0].blur();",
    description_field
)

time.sleep(1)


print(
    "Description after blur:",
    repr(
        description_field.get_attribute("value")
    )
)


# ==================================================
# 11. TAGS
# ==================================================

print()
print("Filling Tags...")

tags_field = driver.find_element(
    By.NAME,
    "tags"
)

# Scroll the field into view
driver.execute_script(
    """
    arguments[0].scrollIntoView({
        block: 'center',
        inline: 'nearest'
    });
    """,
    tags_field
)

time.sleep(0.5)

# Use JavaScript to avoid click interception
driver.execute_script(
    """
    const element = arguments[0];
    const value = arguments[1];

    const prototype = Object.getPrototypeOf(element);

    const descriptor = Object.getOwnPropertyDescriptor(
        prototype,
        'value'
    );

    if (descriptor && descriptor.set) {
        descriptor.set.call(element, value);
    } else {
        element.value = value;
    }

    element.dispatchEvent(
        new Event('input', {
            bubbles: true
        })
    );

    element.dispatchEvent(
        new Event('change', {
            bubbles: true
        })
    );
    """,
    tags_field,
    TAGS
)

time.sleep(0.5)

print(
    "Tags:",
    tags_field.get_attribute("value")
)


# ==================================================
# 12. EMAIL
# ==================================================

print()
print("Filling Email...")

wait.until(
    EC.visibility_of_element_located(
        (By.NAME, "email")
    )
)

email_field = driver.find_element(
    By.NAME,
    "email"
)

email_field.click()
email_field.clear()
email_field.send_keys(EMAIL)

print(
    "Email:",
    email_field.get_attribute("value")
)


# ==================================================
# 13. CATEGORY
# ==================================================

print()
print("Selecting Category...")

wait.until(
    EC.visibility_of_element_located(
        (By.NAME, "category_id")
    )
)

category_field = driver.find_element(
    By.NAME,
    "category_id"
)

category_select = Select(
    category_field
)

print("Available categories:")

for option in category_select.options:

    text = option.text.strip()

    if text:
        print(" -", text)


category_select.select_by_visible_text(
    "AI Productivity Tools"
)

print(
    "Selected Category:",
    category_select.first_selected_option.text
)


# ==================================================
# 14. PRICING
# ==================================================

print()
print("Selecting Pricing Model...")

wait.until(
    EC.visibility_of_element_located(
        (By.NAME, "pricing_model")
    )
)

pricing_field = driver.find_element(
    By.NAME,
    "pricing_model"
)

pricing_select = Select(
    pricing_field
)

print("Available pricing models:")

for option in pricing_select.options:

    text = option.text.strip()

    if text:
        print(" -", text)


pricing_select.select_by_visible_text(
    "Free"
)

print(
    "Selected Pricing:",
    pricing_select.first_selected_option.text
)


# ==================================================
# 15. TARGET AUDIENCE
# ==================================================

print()
print("Checking Target Audience...")

audience_field = driver.find_element(
    By.NAME,
    "target_audience"
)

audience_select = Select(
    audience_field
)

print("Target Audience options:")

for option in audience_select.options:

    text = option.text.strip()

    if text:
        print(" -", text)

# We intentionally leave Target Audience blank.
# It is optional.


# ==================================================
# 16. LOGO
# ==================================================

print()
print("=" * 50)
print("LOGO CHECK")
print("=" * 50)

if os.path.exists(LOGO_PATH):

    print("Logo file found:")
    print(LOGO_PATH)

    logo_field = driver.find_element(
        By.NAME,
        "logo"
    )

    logo_field.send_keys(
        LOGO_PATH
    )

    print("Logo uploaded.")

else:

    print("Logo file NOT found.")
    print("Expected:")
    print(LOGO_PATH)
    print("Logo upload skipped.")


# ==================================================
# 17. VERIFY ALL FORM VALUES
# ==================================================

print()
print("=" * 50)
print("FINAL FORM VERIFICATION")
print("=" * 50)

# Re-read the fields from the page
name_field = driver.find_element(
    By.NAME,
    "name"
)

url_field = driver.find_element(
    By.NAME,
    "link"
)

tagline_field = driver.find_element(
    By.NAME,
    "tagline"
)

# IMPORTANT:
# The actual visible Description textarea is #f-desc.
description_field = driver.find_element(
    By.ID,
    "f-desc"
)

tags_field = driver.find_element(
    By.NAME,
    "tags"
)

email_field = driver.find_element(
    By.NAME,
    "email"
)

category_field = driver.find_element(
    By.NAME,
    "category_id"
)

pricing_field = driver.find_element(
    By.NAME,
    "pricing_model"
)


# ==================================================
# 18. BASIC CORRECTNESS CHECK
# ==================================================

print()
print("=" * 50)
print("CHECKING POPULATED VALUES")
print("=" * 50)


checks = {

    "Tool Name":
        name_field.get_attribute("value") == TOOL_NAME,

    "Website":
        url_field.get_attribute("value") == WEBSITE_URL,

    "Tagline":
        tagline_field.get_attribute("value") == TAGLINE,

    "Description":
        description_field.get_attribute("value") == DESCRIPTION,

    "Tags":
        tags_field.get_attribute("value") == TAGS,

    "Email":
        email_field.get_attribute("value") == EMAIL,

    "Category":
        category_select.first_selected_option.text
        == "AI Productivity Tools",

    "Pricing":
        pricing_select.first_selected_option.text
        == "Free"
}


all_correct = True

for field_name, result in checks.items():

    print(
        f"{field_name}: "
        f"{'PASS' if result else 'FAIL'}"
    )

    if not result:
        all_correct = False


# ==================================================
# 19. FINAL SUBMIT BUTTON CHECK
# ==================================================

print()
print("=" * 50)
print("FINAL SUBMIT CHECK")
print("=" * 50)

buttons = driver.find_elements(
    By.XPATH,
    "//button | //input[@type='submit']"
)

visible_buttons = [
    button
    for button in buttons
    if button.is_displayed()
]


if not visible_buttons:

    print("No visible submit buttons found.")

else:

    for button in visible_buttons:

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
# 20. SAFE STOP
# ==================================================

print()
print("=" * 50)
print("SAFE STOP")
print("=" * 50)


if all_correct:

    print(
        "All populated fields passed verification."
    )

else:

    print(
        "WARNING: One or more fields failed verification."
    )


print()
print("Logo status:")

if os.path.exists(LOGO_PATH):
    print("Logo uploaded.")
else:
    print("Logo still pending.")


print()
print("No payment was made.")
print("No final submission was made.")
print("Final submit button was NOT clicked.")

print()
print("Browser will remain open.")

input(
    "Press Enter to close the browser..."
)

driver.quit()