from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException  # Add this import at the top of your script
import time

# Connect to the existing Chrome instance
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=options)

# # Navigate to Sent folder
# sent_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Sent")
# sent_link.click()

print(driver.current_url)
driver.save_screenshot('debug_screenshot.png')

# Wait for emails to load and find the one with the preview text
preview_text_xpath = "//span[@class='y2'][contains(text(),'⦿ ~30 seconds of happy')]"
email_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, preview_text_xpath)))

# Starting index
idx = 0

# Pagination loop
while True:
    try:
        # Dynamically fetch the idx-th email
        email_xpath = f"({preview_text_xpath})[{idx+1}]"
        email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, email_xpath)))

        # Check if the email is already logged
        if "Logged to:" not in email.text:
            email.click()
            time.sleep(2)

        # Check for the "Log email to HubSpot" button
        try:
            log_button = driver.find_element(By.XPATH, "//i18n-string[text()='Log email to HubSpot']")
            print("Found the log button!")
            log_button.click()
            time.sleep(2)

            try:
                # Replace 'Company Name' with the actual company name you are searching for, or make it dynamic.
                company_checkbox = driver.find_element(By.XPATH, "//div[@title='Company Name']/label")
                company_checkbox.click()
                print("Clicked the company checkbox!")
                time.sleep(2)
            except NoSuchElementException:
                print("No company checkbox found!")
                pass

            save_button = driver.find_element(By.CSS_SELECTOR, ".uiButton[data-button-use='tertiary']")
            print("Found the save button!")
            save_button.click()

            # Wait for a few seconds and then refresh
            time.sleep(3)
            driver.refresh()
            time.sleep(5)  # Give it some time after refresh

        except NoSuchElementException:
            print("Element not found!")
            pass

        # Navigate back to the list of emails
        driver.back()
        time.sleep(2)

        idx += 1  # Increment the index after successful processing

    except StaleElementReferenceException:
        print(f"Stale element encountered at index {idx}. Retrying...")
        continue
    except TimeoutException:
        # Ask the user to verify they're on the new page and have manually clicked next
        choice = input("Script couldn't locate the email. If you've already moved to the next page, press Enter. Otherwise, please click the 'Next' button manually and then press Enter.")

        if not choice.strip():  # If the user just pressed Enter without input
            driver.refresh()  # Refreshing the driver in case this helps with the stale email listings.
            time.sleep(5)  # give it a few seconds to ensure the page is loaded after refresh
            idx = 0
            continue
    except NoSuchElementException:
        print("Finished processing all pages.")
        break

# End the session
driver.quit()





















