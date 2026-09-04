import json
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Step 1: Programmatically resolve relative folder paths for execution stability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, 'app_config.json')

# Load unified SaaS application payload configuration parameters
with open(CONFIG_PATH, 'r') as f:
    PAYLOAD = json.load(f)

# Core target footprint loop tracking verified identical templates mapping uniform elements
TARGET_DOMAINS = [
    "softwarebolt.com",
    "thecoretools.com",
    "smartkithub.com",
    "appalist.com",
    "weliketools.com"
]

# Initialize specific stealth Chrome options to bypass Google's anti-bot framework detection tags
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize local WebDriver properties mirroring your open asr script conventions
driver = webdriver.Chrome(options=chrome_options)

# Extra stealth flag to override navigator.webdriver properties via structural layout scripts
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

try:
    print("\n🛑 [OAUTH STEP] Navigating to the first target node for profile handshake.")
    
    # Start authentication on the initial entry gate sub-path
    initial_url = f"https://{TARGET_DOMAINS[0]}/get-started"
    driver.get(initial_url)
    
    # Absolute manual override gate. The script will halt here until you declare success.
    print("\n👉 STEP 1: Go to the opened Chrome window and create your account / Sign in with Google.")
    print("👉 STEP 2: Once you are fully logged in and looking at the dashboard, come back here.")
    input("👉 STEP 3: Press [ENTER] in this terminal window to unleash the automated cascade... ")
    
    print("\n🔒 [OAUTH CONFIRMED] Commencing automated loop cascade across matrix...")
    time.sleep(2)

    # Run execution cascade sequentially across the footprint loop array using established session tokens
    for domain in TARGET_DOMAINS:
        target_submission_url = f"https://{domain}/submit"
        print(f"\nLOG: Navigating to layout tree form page: {domain}")
        driver.get(target_submission_url)
        time.sleep(6) # Let the layout wrappers render fully
        
        # Fall back to base /get-started if the dashboard link returns a 404 block path or requires an onboarding gate
        if "404" in driver.title or "login" in driver.current_url or len(driver.find_elements(By.XPATH, "//*[contains(text(), 'Not Found')]")) > 0 or len(driver.find_elements(By.XPATH, "//*[contains(text(), '404')]")) > 0:
            driver.get(f"https://{domain}/get-started")
            time.sleep(5)

        print(" -> Waiting for form fields to mount...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )
        
        # Scrape all input fields and textareas currently active on the page structure
        inputs = driver.find_elements(By.XPATH, "//input[@type='text' or @type='url' or not(@type)]")
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        
        # Filter down to only interactive, visible layout input elements
        visible_inputs = [el for el in inputs if el.is_displayed()]
        visible_textareas = [el for el in textareas if el.is_displayed()]
        
        if len(visible_inputs) >= 2:
            print(f" -> Mapping variables sequentially via clean JavaScript attribute strings...")
            
            # Use absolute JS property sets to handle input fields smoothly
            def force_inject_value_js(element, value):
                driver.execute_script("""
                    arguments[0].scrollIntoView({block: 'center'});
                    arguments[0].removeAttribute('disabled');
                    arguments[0].removeAttribute('readonly');
                    arguments[0].value = arguments[1];
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                """, element, value)
                time.sleep(0.5)

            # Input 1 (Index 0): Product Title / Name
            force_inject_value_js(visible_inputs[0], PAYLOAD["product_name"])
            
            # Input 2 (Index 1): Platform Target Landing Page URL
            force_inject_value_js(visible_inputs[1], PAYLOAD["product_url"])
            
            # Input 3 (Index 2 - If available): Tagline or Short Description
            if len(visible_inputs) >= 3:
                force_inject_value_js(visible_inputs[2], PAYLOAD["tagline"])
            
            # Textarea 1: Extensive description canvas paragraph
            if visible_textareas:
                force_inject_value_js(visible_textareas[0], PAYLOAD["description"])
            elif len(visible_inputs) >= 4:
                force_inject_value_js(visible_inputs[3], PAYLOAD["description"])
                
            # Locate and safely trigger form submission button layout wrapper
            submit_btn = driver.find_elements(By.XPATH, "//button[@type='submit' or contains(text(), 'Submit') or contains(text(), 'Add')]")
            if submit_btn:
                # driver.execute_script("arguments[0].click();", submit_btn[0]) # Uncomment when ready to execute active database updates
                pass
                
            print(f"✅ SUCCESS: White label fields successfully populated for {domain}!")
            time.sleep(3)
        else:
            print(f"⚠️ Warning: Found insufficient visible text entry elements ({len(visible_inputs)}) on {domain}")

except Exception as e:
    print(f"⚠️ Process stopped or execution element mismatch encountered: {e}")

finally:
    print("\n🏁 Matrix clone loop sequence finished processing. Holding viewport open for check.")
    time.sleep(10)
    driver.quit()
