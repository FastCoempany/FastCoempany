from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from pandas import DataFrame
import random

import os
import time
import pandas as pd

print(pd.__version__)
print(pd.__file__)
print(dir(pd.DataFrame))

# Create a DataFrame
test_df = pd.DataFrame({'Name': [], 'Title': [], 'Company': []})

# Append a row to the DataFrame
test_df = pd.concat([test_df, pd.DataFrame({'Name': ["Test"], 'Title': ["Test"], 'Company': ["Test"]})], ignore_index=True)

# Print the DataFrame
print(test_df)

# Function Definitions
def save_to_excel(name, title, company):
    file_name = "organized alerts.xlsx"
    if file_name in os.listdir("dbase_slack_alerts"):
        df = pd.read_excel(os.path.join("dbase_slack_alerts", file_name), sheet_name="NewData", engine='openpyxl')
    else:
        df = DataFrame(columns=['Name', 'Title', 'Company'])
    df = pd.concat([df, pd.DataFrame([{'Name': name, 'Title': title, 'Company': company}])], ignore_index=True)
    with pd.ExcelWriter(os.path.join("dbase_slack_alerts", file_name), engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="NewData", index=False)

# Specify the path to chromedriver
chromedriver_path = "/Users/antaeus.coe/Desktop/dbase_slack_alerts/chromedriver"

# Initialize service
service = Service(chromedriver_path)

# Options to tackle the "DevToolsActivePort file doesn't exist" error and other options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
chrome_options.add_argument("--user-data-dir=dbase_slack_alerts")

# Initialize Chrome with the service
driver = webdriver.Chrome(service=service, options=chrome_options)

# Maximize browser window
driver.maximize_window()

# Navigate to LinkedIn login page
driver.get("https://www.linkedin.com")

# Login
wait = WebDriverWait(driver, 20)  # wait for a maximum of 20 seconds

# Input into the username field
username_field = driver.find_element(By.ID, "session_key")
username_field.send_keys("mrcoe7@gmail.com")

# Input into the password field
password_field = driver.find_element(By.ID, "session_password")
password_field.send_keys("11235185469638056709416")

password_field.send_keys(Keys.RETURN)  # Submit the login form

time.sleep(5)  # Optionally, wait for the login to complete.

# Check and switch to new window if opened
if len(driver.window_handles) > 1:
    driver.switch_to.window(driver.window_handles[-1])

# Navigate to the specific link
driver.get("https://www.linkedin.com/sales/search/people?savedSearchId=1742200389&sessionId=BWUQrZSBQv%2B1ro7vTohViQ%3D%3D")

time.sleep(random.uniform(5, 10))  # Adjust the numbers as per the expected load times

# Extract profiles and iterate through results pages
while True:
    profiles = driver.find_elements(By.XPATH, '//*[@id="search-results-container"]//div[contains(@class, "artdeco-entity-lockup") and contains(@class, "artdeco-entity-lockup--size-4")]')
    
    # XPaths for the various elements you want to extract
    name_xpath = './/span[@data-anonymize="person-name"]'
    title_xpath = './/span[@data-anonymize="title"]'
    company_xpath = './/a[@data-anonymize="company-name"]'

    # Extract data from each profile
    for profile in profiles:
        try:
            # Find the profile image as an anchor point
            profile_image = profile.find_element(By.XPATH, './/*[@data-anonymize="headshot-photo"]')

            # Navigate relative to the profile image to find name, title, and company
            name_element = profile_image.find_element(By.XPATH, f'./../following-sibling::div//{name_xpath}')
            title_element = profile_image.find_element(By.XPATH, f'./../following-sibling::div//{title_xpath}')
            company_element = profile_image.find_element(By.XPATH, f'./../following-sibling::div//{company_xpath}')

            name = name_element.text
            title = title_element.text
            company = company_element.text
            
            save_to_excel(name, title, company)  # You can update your function to save the location too
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"Caught exception: {type(e).__name__}: {str(e)}")
            break  # Break the loop if an error occurs while extracting data from a profile

            
    # Check for the "Next" button
    try:
        next_button = driver.find_element(By.XPATH, '//button[@aria-label="Next"]')
        driver.execute_script("arguments[0].scrollIntoView();", next_button)

    # If "Next" button is not disabled, click it to go to the next page
        if next_button.is_enabled():
            next_button.click()
            time.sleep(random.uniform(20, 30))  # Random sleep time between 3 and 5 seconds
        else:
            break  # Break the loop if "Next" button is disabled

    except Exception as e:
        print(f"Caught exception: {type(e).__name__}: {str(e)}")
        break  # Break the loop if an error occurs while finding/clicking the "Next" button

driver.quit()