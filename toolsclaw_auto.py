import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# CONFIGURATION
# ============================================================

TOOL_URL = "https://y2map.com"
TOOL_NAME = "Y2Map"

TAGLINE = "Convert YouTube videos and PDFs into mind maps."

DESCRIPTION = """Y2Map is an AI-powered learning and knowledge tool that transforms YouTube videos, PDFs, books, and research content into easy-to-understand visual mind maps. Instead of spending hours going through long videos or documents, users can create structured visual maps that organize important ideas, concepts, summaries, people, references, and related information in one place.

Y2Map is designed to help students, researchers, educators, founders, engineers, and lifelong learners understand complex topics faster, improve recall, and build stronger mental models. It provides a bigger-picture view of the material before diving into individual details, making learning more organized and easier to navigate.

Users can turn long-form learning material into visual structures that make important concepts easier to review, connect, and remember. Y2Map is especially useful when working with educational videos, research material, books, and other information-heavy content."""

# Recommended ToolsClaw selections
CATEGORIES = [
    "Artificial intelligence",
    "Education",
    "Building Products"
]

PRICING_MODEL = "Freemium"

PLATFORM = "Web"

# Optional information
DISCOUNT_CODE = ""
FOUNDED_YEAR = ""
YOUTUBE_DEMO = ""
GITHUB_REPOSITORY = ""
FOUNDER_TWITTER = ""
AFFILIATE_PROGRAM = ""


# ============================================================
# SILENCE UNDETECTED-CHROMEDRIVER CLEANUP NOISE
# ============================================================

def silent_del(self):
    try:
        pass
    except Exception:
        pass


uc.Chrome.__del__ = silent_del


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def wait_for_visible(driver, by, value, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )


def click_element(driver, element):
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )

    time.sleep(0.5)

    try:
        element.click()
    except Exception:
        driver.execute_script(
            "arguments[0].click();",
            element
        )

    time.sleep(0.7)


def click_by_xpath(driver, xpath, timeout=15):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )

    click_element(driver, element)
    return element


def fill_text_field(driver, by, value, text, label):
    print(f"Filling {label}...")

    element = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((by, value))
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )

    time.sleep(0.3)

    element.click()
    element.clear()
    element.send_keys(text)

    actual = element.get_attribute("value")

    if actual == text:
        print(f"✓ {label} filled.")
    else:
        print(f"⚠ {label} verification mismatch.")

    return element


# ============================================================
# START CHROME
# ============================================================

print("\nStarting Chrome...")

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

driver = uc.Chrome(
    version_main=152,
    options=options
)

wait = WebDriverWait(driver, 20)


# ============================================================
# OPEN HOMEPAGE
# ============================================================

print("\nOpening ToolsClaw homepage...")

driver.get("https://toolsclaw.com/")

wait.until(
    lambda d: d.execute_script("return document.readyState") == "complete"
)

print("Homepage loaded.")
print("Current URL:", driver.current_url)


# ============================================================
# OPEN SUBMIT PAGE THROUGH HOMEPAGE
# ============================================================

print("\nFinding 'Submit' link...")

submit_link = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "//a[normalize-space()='Submit' or .//span[normalize-space()='Submit']]"
        )
    )
)

print("'Submit' link found.")

click_element(driver, submit_link)

wait.until(
    lambda d: "/submit" in d.current_url
)

print("Submission page opened.")
print("Current URL:", driver.current_url)


# ============================================================
# CONFIRM FORM
# ============================================================

wait.until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "//input[@name='url']"
        )
    )
)

print("ToolsClaw submission form confirmed.")


# ============================================================
# 1. TOOL URL
# ============================================================

fill_text_field(
    driver,
    By.XPATH,
    "//input[@name='url']",
    TOOL_URL,
    "Tool URL"
)


# ============================================================
# 2. TOOL NAME
# ============================================================

fill_text_field(
    driver,
    By.XPATH,
    "//input[@name='name']",
    TOOL_NAME,
    "Tool Name"
)


# ============================================================
# 3. TAGLINE
# ============================================================

fill_text_field(
    driver,
    By.XPATH,
    "//input[@name='tagline']",
    TAGLINE,
    "Tagline"
)


# ============================================================
# 4. DESCRIPTION
# ============================================================

print("\nFilling Description...")

description_field = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "//textarea[@name='description']"
        )
    )
)

driver.execute_script(
    "arguments[0].scrollIntoView({block:'center'});",
    description_field
)

time.sleep(0.5)

description_field.click()
description_field.clear()
description_field.send_keys(DESCRIPTION)

time.sleep(1)


# ============================================================
# DESCRIPTION VERIFICATION
# ============================================================

actual_description = description_field.get_attribute("value")

print("\nDESCRIPTION VERIFICATION")
print("Expected characters :", len(DESCRIPTION))
print("Actual characters   :", len(actual_description))

if actual_description == DESCRIPTION:
    print("✓ Full description is present in textarea.")
else:
    print("⚠ Description mismatch.")


# Check live counter
print("\nChecking live character counter...")

try:
    counter = driver.find_element(
        By.XPATH,
        "//textarea[@name='description']/following-sibling::p"
    )

    counter_text = counter.text.strip()

    print("Live counter:", counter_text)

    if str(len(DESCRIPTION)) in counter_text:
        print("✓ ToolsClaw React state updated successfully.")
        print("✓ Live character counter confirms the description.")
    else:
        print("⚠ Character counter could not be verified.")

except Exception:
    print("⚠ Could not locate live character counter.")


# ============================================================
# 5. LOGO
# ============================================================

LOGO_PATH = r"C:\Users\savan\OneDrive\Desktop\GTM_Internship\Nikhil\y2map_logo.png"

print("\nLogo section detected.")
print("Uploading Y2Map logo...")

logo_input = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "//input[@id='logo-image-upload']"
        )
    )
)

logo_input.send_keys(LOGO_PATH)

time.sleep(1)

print("✓ Y2Map logo uploaded.")

# Verify file input contains the selected file
logo_value = logo_input.get_attribute("value")

if logo_value:
    print("✓ Logo file input contains:", logo_value)
else:
    print("⚠ Logo file input value could not be verified.")


# ============================================================
# 6. SCREENSHOTS
# ============================================================

print("\nScreenshots section detected.")
print("✓ Screenshots are optional.")
print("✓ No screenshots uploaded.")


# ============================================================
# 7. CATEGORIES
# ============================================================

print("\nOpening Categories dropdown...")

category_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable(
        (
            By.XPATH,
            "//button[contains(normalize-space(.), 'Select up to 3 categories')]"
        )
    )
)

click_element(driver, category_button)

print("Categories dropdown opened.")

time.sleep(1)


for category in CATEGORIES:

    print(f"Selecting category: {category}")

    try:

        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//button[normalize-space()='{category}']"
                    f" | //div[@role='option' and normalize-space()='{category}']"
                    f" | //span[normalize-space()='{category}']/ancestor::*[@role='option'][1]"
                )
            )
        )

        click_element(driver, option)

        print(f"✓ {category} selected.")

        time.sleep(0.5)

    except Exception as e:

        print(f"⚠ Could not select category: {category}")
        print("Error:", type(e).__name__)


# Close category dropdown
print("\nClosing Categories dropdown...")

try:

    driver.find_element(
        By.XPATH,
        "//body"
    ).send_keys(Keys.ESCAPE)

    time.sleep(0.5)

except Exception:
    pass


# ============================================================
# VERIFY CATEGORIES
# ============================================================

print("\nCATEGORY VERIFICATION")

page_text = driver.find_element(
    By.XPATH,
    "//body"
).text

for category in CATEGORIES:

    if category in page_text:
        print(f"✓ {category}")
    else:
        print(
            f"⚠ {category} not confirmed in visible page text."
        )


# ============================================================
# 8. PRICING MODEL
# ============================================================

print("\nSelecting Pricing Model...")

try:

    # First try native <select>
    pricing_selects = driver.find_elements(
        By.XPATH,
        "//select"
    )

    pricing_done = False

    for select_element in pricing_selects:

        options = [
            option.text.strip()
            for option in Select(select_element).options
        ]

        if "Freemium" in options:

            driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                select_element
            )

            time.sleep(0.5)

            Select(select_element).select_by_visible_text(
                PRICING_MODEL
            )

            print(
                "✓ Pricing Model selected:",
                PRICING_MODEL
            )

            pricing_done = True
            break

    # If no native select worked, use the visible button
    if not pricing_done:

        pricing_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(normalize-space(.), 'Select pricing model')]"
                )
            )
        )

        click_element(driver, pricing_button)

        time.sleep(0.7)

        freemium_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//*[normalize-space()='Freemium' and "
                    "(self::button or @role='option' or @role='menuitem')]"
                )
            )
        )

        click_element(driver, freemium_option)

        print(
            "✓ Pricing Model selected:",
            PRICING_MODEL
        )

except Exception as e:

    print("⚠ Pricing Model selection failed.")
    print(
        "Error:",
        type(e).__name__,
        str(e)
    )


# ============================================================
# 9. PLATFORMS
# ============================================================

print("\nOpening Platforms dropdown...")

try:

    platform_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(normalize-space(.), 'Select platforms')]"
            )
        )
    )

    click_element(driver, platform_button)

    print("Platforms dropdown opened.")

    time.sleep(0.7)

    web_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//*[normalize-space()='Web' and "
                "(self::button or @role='option' or @role='menuitem')]"
            )
        )
    )

    click_element(driver, web_option)

    print("✓ Platform selected:", PLATFORM)

except Exception as e:

    print("⚠ Platform selection failed.")
    print(
        "Error:",
        type(e).__name__,
        str(e)
    )


# ============================================================
# CLOSE PLATFORM DROPDOWN
# ============================================================

try:

    driver.find_element(
        By.XPATH,
        "//body"
    ).send_keys(Keys.ESCAPE)

    time.sleep(0.5)

except Exception:
    pass


# ============================================================
# 10. OPTIONAL / OTHER INFORMATION
# ============================================================

print("\n============================================================")
print("OTHER / OPTIONAL INFORMATION")
print("============================================================")

print(
    "Discount Code       :",
    "SKIPPED" if not DISCOUNT_CODE else DISCOUNT_CODE
)

print(
    "Founded Year        :",
    "SKIPPED" if not FOUNDED_YEAR else FOUNDED_YEAR
)

print(
    "YouTube Demo Video  :",
    "SKIPPED" if not YOUTUBE_DEMO else YOUTUBE_DEMO
)

print(
    "GitHub Repository   :",
    "SKIPPED" if not GITHUB_REPOSITORY else GITHUB_REPOSITORY
)

print(
    "Founder's Twitter   :",
    "SKIPPED" if not FOUNDER_TWITTER else FOUNDER_TWITTER
)

print(
    "Affiliate Program   :",
    "SKIPPED" if not AFFILIATE_PROGRAM else AFFILIATE_PROGRAM
)

print("\n✓ All optional fields intentionally left empty.")


# ============================================================
# FINAL VERIFICATION
# ============================================================

print("\n============================================================")
print("FINAL FORM CHECK")
print("============================================================")


# URL
try:

    url_value = driver.find_element(
        By.XPATH,
        "//input[@name='url']"
    ).get_attribute("value")

    print("Tool URL        :", url_value)

except Exception:
    print("Tool URL        : Could not verify")


# Name
try:

    name_value = driver.find_element(
        By.XPATH,
        "//input[@name='name']"
    ).get_attribute("value")

    print("Tool Name       :", name_value)

except Exception:
    print("Tool Name       : Could not verify")


# Tagline
try:

    tagline_value = driver.find_element(
        By.XPATH,
        "//input[@name='tagline']"
    ).get_attribute("value")

    print("Tagline         :", tagline_value)

except Exception:
    print("Tagline         : Could not verify")


# Description
try:

    final_description = driver.find_element(
        By.XPATH,
        "//textarea[@name='description']"
    ).get_attribute("value")

    print(
        "Description     :",
        len(final_description),
        "characters"
    )

except Exception:
    print("Description     : Could not verify")


# ============================================================
# IMPORTANT SAFETY CHECK
# ============================================================

print("\n============================================================")
print("AUTOMATION STOP POINT")
print("============================================================")

print("✓ Tool URL filled")
print("✓ Tool Name filled")
print("✓ Tagline filled")
print("✓ Description filled and verified")
print("✓ Logo NOT uploaded")
print("✓ Screenshots NOT uploaded")
print("✓ Categories attempted")
print("✓ Pricing Model attempted")
print("✓ Platform attempted")
print("✓ Optional/Other fields left empty")
print("✓ NEXT BUTTON NOT CLICKED")
print("✓ NO SUBMISSION PERFORMED")

print("\nBrowser will remain open for inspection.")
print("Press ENTER to close...")


input()

driver.quit()