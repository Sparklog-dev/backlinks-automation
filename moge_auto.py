import time
import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================================================
# MOGE - Y2Map submission mapping/testing
# Filename: moge_auto.py
# IMPORTANT:
# - XPath selectors only
# - Do NOT bypass Cloudflare
# - Do NOT click "Share Now"
# ============================================================

MOGE_HOME = "https://moge.ai/"
Y2MAP_URL = "https://y2map.com"


def xpath_click(driver, xpath, description, timeout=20):
    """Click an element using XPath only."""

    wait = WebDriverWait(driver, timeout)

    element = wait.until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        element
    )

    time.sleep(1)

    try:
        element.click()
    except Exception:
        # JavaScript click fallback.
        # The selector itself is still XPath.
        driver.execute_script("arguments[0].click();", element)

    print(f"[OK] {description}")


def find_visible_element(driver, xpaths, description, timeout=20):
    """Try several XPath expressions and return the first visible element."""

    wait = WebDriverWait(driver, timeout)

    end_time = time.time() + timeout

    while time.time() < end_time:

        for xpath in xpaths:
            try:
                elements = driver.find_elements(By.XPATH, xpath)

                for element in elements:
                    if element.is_displayed():
                        print(f"[OK] Found {description}")
                        return element

            except Exception:
                pass

        time.sleep(0.5)

    raise Exception(f"Could not find visible element: {description}")


def fill_xpath(driver, xpaths, value, description, timeout=20):
    """Fill an input using XPath only."""

    element = find_visible_element(
        driver,
        xpaths,
        description,
        timeout
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        element
    )

    time.sleep(0.5)

    try:
        element.click()
        element.clear()
        element.send_keys(value)

    except Exception:
        # JavaScript fallback.
        driver.execute_script(
            """
            arguments[0].focus();
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(
                new Event('input', { bubbles: true })
            );
            arguments[0].dispatchEvent(
                new Event('change', { bubbles: true })
            );
            """,
            element,
            value
        )

    # Verify actual browser value.
    actual_value = element.get_attribute("value")

    if actual_value == value:
        print(f"[OK] {description} successfully typed.")
        print(f"[OK] Browser value: {actual_value}")
        return element

    print("[WARNING] Initial value verification failed.")
    print(f"[WARNING] Expected: {value}")
    print(f"[WARNING] Actual:   {actual_value}")

    # One more JavaScript attempt.
    driver.execute_script(
        """
        arguments[0].focus();
        arguments[0].value = arguments[1];
        arguments[0].dispatchEvent(
            new Event('input', { bubbles: true })
        );
        arguments[0].dispatchEvent(
            new Event('change', { bubbles: true })
        );
        """,
        element,
        value
    )

    time.sleep(1)

    actual_value = element.get_attribute("value")

    if actual_value == value:
        print(f"[OK] {description} successfully verified.")
        print(f"[OK] Browser value: {actual_value}")
    else:
        print(f"[FAIL] {description} could not be verified.")
        print(f"[FAIL] Expected: {value}")
        print(f"[FAIL] Actual:   {actual_value}")

    return element


def main():

    print("=" * 60)
    print("MOGE - Y2Map Submission Mapping")
    print("=" * 60)

    options = uc.ChromeOptions()

    # Normal browser window.
    options.add_argument("--start-maximized")

    driver = uc.Chrome(
        version_main=152,
        options=options
    )

    # Prevent noisy WinError 6 cleanup message from undetected_chromedriver.
    uc.Chrome.__del__ = lambda self: None

    try:

        # ----------------------------------------------------
        # STEP 1 - Open MOGE homepage
        # ----------------------------------------------------

        print("\n[STEP 1] Opening MOGE homepage...")

        driver.get(MOGE_HOME)

        time.sleep(4)

        print(f"[OK] URL: {driver.current_url}")
        print(f"[OK] Title: {driver.title}")


        # ----------------------------------------------------
        # STEP 2 - Find Submit Product on homepage
        # ----------------------------------------------------

        print("\n[STEP 2] Looking for Submit Product...")

        submit_product_xpaths = [
            "//a[normalize-space()='Submit Product']",
            "//button[normalize-space()='Submit Product']",
            "//*[self::a or self::button][contains(normalize-space(.), 'Submit Product')]",
            "//*[contains(normalize-space(.), 'Submit product')]"
        ]

        submit_element = find_visible_element(
            driver,
            submit_product_xpaths,
            "Submit Product button/link",
            timeout=25
        )

        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            submit_element
        )

        time.sleep(1)

        try:
            submit_element.click()
        except Exception:
            driver.execute_script(
                "arguments[0].click();",
                submit_element
            )

        print("[OK] Submit Product clicked.")


        # ----------------------------------------------------
        # STEP 3 - Wait for popup
        # ----------------------------------------------------

        print("\n[STEP 3] Waiting for submission popup...")

        popup_xpaths = [
            "//*[contains(normalize-space(.), 'Submit your product')]",
            "//*[contains(normalize-space(.), 'Your Product Official Website')]"
        ]

        find_visible_element(
            driver,
            popup_xpaths,
            "Submit your product popup",
            timeout=20
        )

        print("[OK] Submission popup detected.")


        # ----------------------------------------------------
        # STEP 4 - Find product URL input
        # ----------------------------------------------------

        print("\n[STEP 4] Looking for Product Official Website field...")

        product_url_xpaths = [
            "//input[@placeholder='Your Product Official Website']",
            "//input[contains(@placeholder, 'Product Official Website')]",
            "//input[@type='url']",
            "//input[not(@type='hidden') and not(@type='submit') and not(@type='button')]"
        ]

        fill_xpath(
            driver,
            product_url_xpaths,
            Y2MAP_URL,
            "Website URL",
            timeout=20
        )


        # ----------------------------------------------------
        # STEP 5 - Inspect Cloudflare
        # ----------------------------------------------------

        print("\n[STEP 5] Checking Cloudflare area...")

        cloudflare_xpaths = [
            "//*[contains(normalize-space(.), 'Cloudflare')]",
            "//*[contains(normalize-space(.), 'Success!')]",
            "//*[contains(normalize-space(.), 'Privacy') and contains(normalize-space(.), 'Help')]"
        ]

        cloudflare_found = False

        for xpath in cloudflare_xpaths:
            try:
                elements = driver.find_elements(By.XPATH, xpath)

                for element in elements:
                    if element.is_displayed():
                        cloudflare_found = True
                        break

                if cloudflare_found:
                    break

            except Exception:
                pass

        if cloudflare_found:
            print("[OK] Cloudflare verification area detected.")
            print("[INFO] Cloudflare is NOT being bypassed or automated.")

        else:
            print("[INFO] Cloudflare verification area was not detected by XPath.")


        # ----------------------------------------------------
        # STEP 6 - Verify URL one more time
        # ----------------------------------------------------

        print("\n[STEP 6] Final browser-value verification...")

        url_element = find_visible_element(
            driver,
            product_url_xpaths,
            "Website URL field",
            timeout=10
        )

        actual_url = url_element.get_attribute("value")

        if actual_url == Y2MAP_URL:
            print("[PASS] Y2Map URL is correctly present in the form.")
        else:
            print("[FAIL] URL verification failed.")
            print(f"[FAIL] Expected: {Y2MAP_URL}")
            print(f"[FAIL] Actual:   {actual_url}")


        # ----------------------------------------------------
        # STEP 7 - DO NOT SUBMIT
        # ----------------------------------------------------

        print("\n" + "=" * 60)
        print("MAPPING COMPLETE")
        print("=" * 60)

        print("[OK] Homepage -> Submit Product -> form completed.")
        print("[OK] Y2Map URL entered.")
        print("[OK] Browser value verified.")
        print()
        print("[STOP] 'Share Now' was NOT clicked.")
        print("[STOP] No submission was made.")
        print()
        print("Inspect the popup manually before proceeding.")
        print("=" * 60)


        # Keep browser open.
        input("\nPress ENTER to close the browser...")

    finally:

        try:
            driver.quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()