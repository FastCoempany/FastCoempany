#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.exceptions import NoSuchElementException
import time
import sys

print(sys.executable)

# Set up the driver for a new Chrome instance
driver = webdriver.Chrome()

# Navigate to Gmail for manual login
driver.get("https://mail.google.com/")
input("Press Enter in the console after you have logged in manually...")

# Navigate directly to the specific email after you've logged in
driver.get("https://mail.google.com/mail/u/0/#sent/FMfcgzGtxdZHdbnmwmvsgWfjDjXMQxfg")

# Wait for a few seconds to ensure the page is loaded
time.sleep(5)

# Start your logging function here
try:
    log_button = driver.find_element(By.XPATH, "//i18n-string[text()='Log email to HubSpot']")
    print("Found the log button!")
    log_button.click()
    time.sleep(2)

    try:
        # Replace 'Company Name' with the actual company name you're searching for, or make it dynamic.
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

    # Wait for a few seconds then refresh
    time.sleep(3)
    driver.refresh()
    time.sleep(5)  # Allow some time after refresh

except NoSuchElementException:
    print("Element not found!")
    pass


