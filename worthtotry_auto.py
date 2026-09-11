# ============================================================
# FILENAME: worthtotry_auto.py
# WEBSITE : WorthToTry
# PURPOSE : Map and prepare Y2Map submission
# IMPORTANT: Stops before final submission / login
# SELECTORS: XPath only
# ============================================================

import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# Y2MAP DATA
# ============================================================

PRODUCT_NAME = "Y2Map"

WEBSITE_URL = "https://y2map.com"

EMAIL = "sparklog.marketing@gmail.com"

SHORT_DESCRIPTION = (
    "Turn YouTube videos and PDFs into clear visual mind maps."
)

LONG_DESCRIPTION = (
    "Y2Map is an AI-powered learning and knowledge tool that transforms "
    "YouTube videos, PDFs, books, and research content into easy-to-understand "
    "visual mind maps. It helps students, researchers, educators, founders, "
    "engineers, and lifelong learners understand complex topics faster by "
    "organizing important ideas, concepts, summaries, references, and related "
    "information into a structured visual format. Instead of spending hours "
    "going through lengthy videos or documents, users can create a visual "
    "overview that makes information easier to explore, review, connect, "
    "and remember."
)


# ============================================================
# CHROME SETUP
# ============================================================

options = uc.ChromeOptions()
options.add_argument("--start-maximized")

# Prevent WinError 6 cleanup noise from undetected_chromedriver
uc.Chrome.__del__ = lambda self: None

driver = uc.Chrome(
    version_main=152,
    options=options
)

wait = WebDriverWait(driver, 20)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def print_page_state():
    print()
    print("=" * 70)
    print("CURRENT PAGE")
    print("=" * 70)
    print(f"URL   : {driver.current_url}")
    print(f"TITLE : {driver.title}")
    print("=" * 70)
    print()


def wait_for_xpath(xpath, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )


def click_xpath(xpath, description="", timeout=20):
    element = WebDriverWait(
        driver,
        timeout
    ).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        element
    )

    time.sleep(0.7)

    try:
        element.click()
    except Exception:
        driver.execute_script(
            "arguments[0].click();",
            element
        )

    if description:
        print(f"✓ Clicked: {description}")

    return element


def set_value_js(xpath, value, description="", timeout=20):
    element = wait_for_xpath(xpath, timeout)

    driver.execute_script(
        """
        arguments[0].scrollIntoView({block:'center'});

        const element = arguments[0];
        const value = arguments[1];

        const descriptor =
            Object.getOwnPropertyDescriptor(
                HTMLInputElement.prototype,
                'value'
            ) ||
            Object.getOwnPropertyDescriptor(
                HTMLTextAreaElement.prototype,
                'value'
            );

        if (descriptor && descriptor.set) {
            descriptor.set.call(element, value);
        } else {
            element.value = value;
        }

        element.dispatchEvent(
            new Event('input', {bubbles: true})
        );

        element.dispatchEvent(
            new Event('change', {bubbles: true})
        );

        element.dispatchEvent(
            new Event('blur', {bubbles: true})
        );
        """,
        element,
        value
    )

    if description:
        print(f"✓ Filled: {description}")

    return element


def find_first_existing(xpaths, timeout_each=4):
    for xpath in xpaths:
        try:
            element = WebDriverWait(
                driver,
                timeout_each
            ).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)
                )
            )

            return element, xpath

        except Exception:
            continue

    return None, None


# ============================================================
# START
# ============================================================

try:

    print()
    print("Opening WorthToTry homepage...")
    print()

    driver.get("https://worthtotry.com/")

    time.sleep(5)

    print_page_state()


    # ========================================================
    # STEP 1 — FIND ACTUAL "LIST YOUR TOOL" LINK
    # ========================================================

    print("Looking for the actual 'List your tool' link...")

    submit_link_xpaths = [

        "//a[contains(@href, '#submit') "
        "and "
        "contains("
        "translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'list your tool'"
        ")]",

        "//a[contains(translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'list your tool')]"
    ]


    submit_link, submit_xpath = find_first_existing(
        submit_link_xpaths,
        timeout_each=5
    )


    if submit_link is None:

        print("❌ Could not find the homepage submission link.")

        print()
        print("Available links containing submit/list:")

        links = driver.find_elements(
            By.XPATH,
            "//a"
        )

        for link in links:

            try:
                text = link.text.strip()
                href = link.get_attribute("href")

                if (
                    "submit" in text.lower()
                    or
                    "list" in text.lower()
                ):
                    print(
                        f"  TEXT: {text} | HREF: {href}"
                    )

            except Exception:
                pass

        input("Press Enter to close the browser...")
        raise SystemExit


    submit_href = submit_link.get_attribute("href")

    print("✓ Homepage submission link found")
    print(f"  HREF: {submit_href}")


    # ========================================================
    # STEP 2 — CLICK HOMEPAGE LINK
    # ========================================================

    old_windows = driver.window_handles.copy()

    print()
    print("Clicking homepage → List your tool...")

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        submit_link
    )

    time.sleep(1)

    try:
        submit_link.click()
    except Exception:
        driver.execute_script(
            "arguments[0].click();",
            submit_link
        )

    print("✓ Homepage click executed")

    time.sleep(5)


    # ========================================================
    # STEP 3 — CHECK NEW TAB
    # ========================================================

    new_windows = driver.window_handles

    if len(new_windows) > len(old_windows):

        print("✓ New tab/window detected")

        for window in new_windows:

            if window not in old_windows:

                driver.switch_to.window(window)

                print("✓ Switched to new tab/window")

                break

        time.sleep(3)


    print()
    print(f"Current URL after click: {driver.current_url}")


    # ========================================================
    # STEP 4 — FALLBACK TO DISCOVERED HREF
    # ========================================================

    if (
        "/submit" not in driver.current_url
        and
        "#submit" not in driver.current_url
    ):

        print()
        print("⚠ Homepage click did not reach the submission flow.")
        print("Using the HREF discovered from the homepage...")

        driver.get(submit_href)

        time.sleep(5)


    print_page_state()


    # ========================================================
    # STEP 5 — FIND PRODUCT URL INPUT
    # ========================================================

    print("Looking for 'Your tool's URL' input...")

    url_xpaths = [

        "//input[@type='url']",

        "//input[contains("
        "translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'url'"
        ")]",

        "//input[contains("
        "translate(@name,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'url'"
        ")]",

        "//input[contains("
        "translate(@id,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'url'"
        ")]",

        "//input[contains("
        "translate(@aria-label,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'url'"
        ")]"
    ]


    url_element, url_xpath = find_first_existing(
        url_xpaths,
        timeout_each=5
    )


    if url_element is None:

        print("❌ Could not identify the URL input.")

        print()
        print("Available inputs:")

        inputs = driver.find_elements(
            By.XPATH,
            "//input"
        )

        for index, element in enumerate(inputs, start=1):

            try:
                print(
                    f"  [{index}] "
                    f"type={element.get_attribute('type')} "
                    f"name={element.get_attribute('name')} "
                    f"id={element.get_attribute('id')} "
                    f"placeholder={element.get_attribute('placeholder')}"
                )

            except Exception:
                pass

        input("Press Enter to close the browser...")
        raise SystemExit


    print("✓ URL input identified")
    print(f"  XPath: {url_xpath}")


    # ========================================================
    # STEP 6 — ENTER Y2MAP URL
    # ========================================================

    set_value_js(
        url_xpath,
        WEBSITE_URL,
        "Y2Map website URL"
    )

    time.sleep(1)


    # ========================================================
    # STEP 7 — LOOK FOR CONTINUE / CHECK / NEXT
    # ========================================================

    print()
    print("Looking for Continue / Check / Next button...")


    continue_xpaths = [

        "//button[contains("
        "translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'continue'"
        ")]",

        "//button[contains("
        "translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'check'"
        ")]",

        "//button[contains("
        "translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'next'"
        ")]",

        "//button[contains("
        "translate(normalize-space(.),"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'audit'"
        ")]",

        "//input[@type='submit']",

        "//button[@type='submit']"
    ]


    continue_element, continue_xpath = find_first_existing(
        continue_xpaths,
        timeout_each=4
    )


    if continue_element is None:

        print("❌ Could not find Continue/Check button.")

        print()
        print("Available buttons:")

        buttons = driver.find_elements(
            By.XPATH,
            "//button"
        )

        for index, button in enumerate(buttons, start=1):

            try:
                print(
                    f"  [{index}] "
                    f"text='{button.text.strip()}' "
                    f"type={button.get_attribute('type')}"
                )

            except Exception:
                pass

        input("Press Enter to close the browser...")
        raise SystemExit


    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        continue_element
    )

    time.sleep(0.7)

    try:
        continue_element.click()
    except Exception:
        driver.execute_script(
            "arguments[0].click();",
            continue_element
        )

    print("✓ Clicked: Continue / Check")


    # ========================================================
    # STEP 8 — WAIT FOR AUDIT / DRAFT
    # ========================================================

    print()
    print("Waiting for WorthToTry to audit Y2Map...")

    time.sleep(10)

    print_page_state()


    # ========================================================
    # STEP 9 — CHECK FOR LOGIN / MAGIC LINK
    # ========================================================

    current_url = driver.current_url.lower()
    page_text = driver.find_element(
        By.XPATH,
        "//body"
    ).text.lower()


    if (
        "/login" in current_url
        or
        "sign in" in page_text
        or
        "magic link" in page_text
        or
        "need an account" in page_text
    ):

        print()
        print("=" * 70)
        print("WORTHTOTRY RESULT")
        print("=" * 70)

        print("STATUS : LOGIN REQUIRED TO OPEN DRAFT")
        print()
        print("✓ Homepage flow verified")
        print("✓ 'List your tool' link verified")
        print("✓ Submission flow verified")
        print("✓ Y2Map URL entered")
        print("✓ Audit/check flow reached")
        print("✓ No final submission performed")
        print("✓ No account created")
        print("✓ No payment made")
        print()
        print("WorthToTry requires sign-in with a magic link")
        print("to open the generated submission draft.")
        print()
        print("ACTION : Stop here and inspect manually.")
        print("=" * 70)
        print()

        input("Press Enter to close the browser...")
        raise SystemExit


    # ========================================================
    # STEP 10 — LOOK FOR GENERATED DRAFT FIELDS
    # ========================================================

    print("No obvious login gate detected.")
    print()
    print("Looking for generated draft fields...")


    # --------------------------------------------------------
    # TOOL NAME
    # --------------------------------------------------------

    name_xpaths = [

        "//input[contains("
        "translate(@name,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'name'"
        ")]",

        "//input[contains("
        "translate(@id,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'name'"
        ")]",

        "//input[contains("
        "translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'tool name'"
        ")]"
    ]


    name_element, name_xpath = find_first_existing(
        name_xpaths,
        timeout_each=3
    )


    if name_element is not None:

        field_type = name_element.get_attribute("type")

        if field_type not in ["url", "email"]:

            set_value_js(
                name_xpath,
                PRODUCT_NAME,
                "Tool Name"
            )

    else:

        print("ℹ Tool Name field not detected")


    # --------------------------------------------------------
    # DESCRIPTION
    # --------------------------------------------------------

    description_xpaths = [

        "//textarea[contains("
        "translate(@name,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'description'"
        ")]",

        "//textarea[contains("
        "translate(@id,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'description'"
        ")]",

        "//textarea[contains("
        "translate(@placeholder,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'description'"
        ")]"
    ]


    description_element, description_xpath = find_first_existing(
        description_xpaths,
        timeout_each=3
    )


    if description_element is not None:

        set_value_js(
            description_xpath,
            LONG_DESCRIPTION,
            "Description"
        )

    else:

        print("ℹ Description field not detected")


    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    email_xpaths = [

        "//input[@type='email']",

        "//input[contains("
        "translate(@name,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'email'"
        ")]",

        "//input[contains("
        "translate(@id,"
        "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
        "'abcdefghijklmnopqrstuvwxyz'),"
        "'email'"
        ")]"
    ]


    email_element, email_xpath = find_first_existing(
        email_xpaths,
        timeout_each=3
    )


    if email_element is not None:

        set_value_js(
            email_xpath,
            EMAIL,
            "Email"
        )

    else:

        print("ℹ Email field not detected")


    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("=" * 70)
    print("WORTHTOTRY MAPPING RESULT")
    print("=" * 70)

    print(f"Current URL : {driver.current_url}")
    print(f"Page title  : {driver.title}")

    print()
    print("Y2Map data was entered where matching fields were found.")

    print()
    print("IMPORTANT:")
    print("✓ No final submission clicked")
    print("✓ No payment selected")
    print("✓ No account created")
    print("✓ Browser remains open for inspection")

    print("=" * 70)
    print()


    # ========================================================
    # KEEP BROWSER OPEN
    # ========================================================

    input("Press Enter to close the browser...")


finally:

    try:
        driver.quit()
    except Exception:
        pass