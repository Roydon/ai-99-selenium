import time
# from datetime import datetime
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# List of new prompts
prompts = [
       "Explain in detail the following Kubernetes Cluster Architecture, Installation & Configuration concepts. For each, cover its core principles, typical CKA exam-relevant configuration details (including YAML examples where applicable), key command-line tools and `kubectl` commands, its role in the Kubernetes ecosystem, and how it interacts with other components. Focus on practical knowledge needed for the CKA exam.",
       "Explain in detail the following Kubernetes Services & Networking concepts. For each, cover its core principles, typical CKA exam-relevant configuration details (including YAML examples where applicable), key `kubectl` commands for management/inspection/troubleshooting, its role in the Kubernetes ecosystem, and how it interacts with other components. Focus on practical knowledge needed for the CKA exam",
       "Explain the core concepts and unique configuration details of the following Kubernetes storage components, providing clear examples where possible. For each component, describe its purpose, how it interacts with other storage components, and key YAML configuration fields or `kubectl` commands relevant for CKA exam preparation",
       "Explain in detail the following Kubernetes Workloads and Scheduling concepts, focusing on their core principles, use cases, key `kubectl` commands for management/inspection, important YAML manifest fields with configuration examples, and how they interact with each other. Tailor the explanation for CKA exam preparation, emphasizing practical application and troubleshooting."
   ]

# Configure Chrome
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--headless")  # Optional: Run in headless mode for better performance
chrome_options.add_argument("--verbose")  # Enable verbose logging for ChromeDriver

chrome_options.debugger_address = "127.0.0.1:9222"  # Connect to existing Chrome instance

# Initialize the browser
driver = webdriver.Chrome(options=chrome_options)

try:
    for current_prompt in prompts:
        # Open a new tab
        driver.execute_script("window.open('');")  # Opens a blank new tab
        driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
        driver.execute_script("window.blur();")  # Minimize the browser's focus
        print("New tab opened.")

        # Open the webpage in the new tab
        driver.get("https://gemini.google.com/app")

        # Wait for the dropdown toggle button to be clickable and open it
        dropdown_toggle = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='bard-mode-menu-button']"))
        )
        dropdown_toggle.click()

        # Wait for the dropdown options to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cdk-overlay-0"))
        )

        # Locate and click the desired option: "2.5 Pro with Deep Research"
        desired_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button//span[contains(text(), '2.5 Pro with Deep Research')]")
            )
        )
        desired_option.click()

        print("Successfully selected '2.5 Pro with Deep Research'")

        # Wait for the input field to load
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ql-editor"))
        )

        # Focus on the input field and type the current company
        prompt = current_prompt

        input_field.click()
        input_field.send_keys(prompt)

        # Simulate pressing Enter
        input_field.send_keys(Keys.RETURN)

        # Wait for the "Start research" button to appear with retry
        for attempt in range(3):  # Retry up to 3 times
            try:
                start_research_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@data-test-id='confirm-button' and @aria-label='Start research']"))
                )
                # Click the "Start research" button
                start_research_button.click()
                print(f"Successfully clicked 'Start research' button for prompt: {current_prompt[:50]}...")
                break  # Exit the retry loop if successful
            except Exception as e:
                if attempt < 2:  # Retry only if attempts remain
                    print(f"Retrying to find and click 'Start research' button due to: {e}")
                    time.sleep(2)  # Small delay before retrying
                else:
                    print(f"Failed to click 'Start research' button for prompt: {current_prompt[:50]}... after 3 attempts")
                    raise  # Re-raise the exception after exhausting retries

        # Wait for the research to complete
        print("Waiting for research to complete...", end="", flush=True)
        start_time = time.time()
        timeout = 1200  # 20 minutes
        interval = 5  # Check every 5 seconds

        while True:
            open_in_docs_button = driver.find_elements(By.XPATH, "//button[@data-test-id='open-in-docs-button']")
            if open_in_docs_button:
                elapsed_time = time.time() - start_time
                print(f"\nResearch completed in {int(elapsed_time // 60)} minutes and {int(elapsed_time % 60)} seconds.")
                # open_in_docs_button[0].click()
                driver.find_element(By.XPATH, "//button[@data-test-id='open-in-docs-button']").click()
                break

            # Print a dot for each checkpoint
            print(".", end="", flush=True)
            time.sleep(interval)

        # Wait for the second "Open Docs" button to appear
        print("Waiting for the 'Open Docs' button to appear...", end="", flush=True)
        start_time = time.time()

        while True:
            open_docs_buttons = driver.find_elements(By.XPATH, "//button[@class='mat-mdc-snack-bar-action mdc-snackbar__action action-button mdc-button mat-mdc-button mat-unthemed mat-mdc-button-base ng-star-inserted']")
            if open_docs_buttons:
                elapsed_time = time.time() - start_time
                print(f"\n'Open Docs button appeared after {int(elapsed_time // 60)} minutes and {int(elapsed_time % 60)} seconds.")
                print(f"\n'Report saved for prompt: {current_prompt[:50]}...")
                # open_docs_buttons[0].click()
                driver.find_element(By.XPATH, "//button[@class='mat-mdc-snack-bar-action mdc-snackbar__action action-button mdc-button mat-mdc-button mat-unthemed mat-mdc-button-base ng-star-inserted']").click()
                break

            # Print a dot for each checkpoint
            print(".", end="", flush=True)
            time.sleep(interval)

        # Close the current tab
        time.sleep(interval)
        driver.close()
        print("Tab closed successfully.")

        # Switch back to the main tab
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])
            print("Switched back to the main tab.")

except Exception as e:
    print(f"\nError occurred: {e}")

finally:
    print("Script execution completed")
