from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import random

import pandas as pd
import os
import time

# Function Definitions
def save_to_excel(name, title, company):
    file_name = "organized alerts.xlsx"
    if file_name in os.listdir("dbase_slack_alerts"):
        df = pd.read_excel(os.path.join("dbase_slack_alerts", file_name), sheet_name="NewData", engine='openpyxl')
    else:
        df = pd.DataFrame(columns=['Name', 'Title', 'Company'])
    df = df.append({'Name': name, 'Title': title, 'Company': company}, ignore_index=True)
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

# Maximize browser window
driver.maximize_window()

# Navigate to the specific link
driver.get("https://www.linkedin.com/sales/search/people?viewAllFilters=true")
time.sleep(7)  # Let the page load for about 7 seconds

# Expand 'current company' filter
company_expand_btn_xpath = '//fieldset[@data-x-search-filter="CURRENT_COMPANY"]//button[contains(@class, "search-filter__focus-target--button")]'
company_expand_btn = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, company_expand_btn_xpath))
)
company_expand_btn.click()

# Input and search company names one-by-one
company_names = "6sense, AbbVie, Above The Line, LLC an Authorized Sandler Training Franchisee, Accenture, Acosta, Inc., ACT Fibernet, Acuity Brands, ADP, Aerotek, Aflac, AGILE Infoways, AIA, AIG, Airbus S.A.S., Airgas, Allied Universal, Amazon, Anheuser-Busch InBev, aramark, Arcadis, Archer Daniels Midland Company, Arise, Ascential, Atkinson, Andelson, Loya, Ruud & Romo, Atlassian, Autodesk Inc., Avery Dennison, AVI-SPL, Bank of America, Barracuda Networks, Inc., Baxter International Inc., Bayer, Bed Bath & Beyond, Beeline, Bentley Systems, berkeley college, Blue Cross Blue Shield of Michigan, Boeing, Bose Corporation, Bp P.l.c., Broadridge Financial Solutions, Inc., Brooklyn College, ByteDance, C.H. Robinson, California Department of Human Resources (CalHR), Capital One, CarMax, Carrier Enterprise, Carter's | OshKosh B'gosh, CDW, Change Healthcare, Chevron, CIBC, Ciena, Citadel, Citi, Clarivate, Cognizant, Columbia Sportswear Company, Consultant, cornell university, Cox Automotive Inc., Cuatrecasas, Cummins Inc., Cushman & Wakefield, Cvent, Cystic Fibrosis Foundation, Deloitte, Deltek, DISYS, Drexel University, Driven Brands Inc., DXC Technology, Ecolab, Emerson Automation Solutions, EPAM Systems, Inc., Epic Games, Essent, eteam, Exelon, Ferguson Enterprises, Ferrara, Fidelity Investments, First Advantage, FIS, Flaire, Ford Motor Company, Fresenius Medical Care, FTI Consulting, Fujifilm Corporation, General Electric, General Motors, Georgetown University, Georgia Institute of Technology, Gilead Sciences, Inc., Glovo, Goenvy, Goldberg Segalla, Gordon Food Service, Greenberg Traurig, LLP, Greystar, Groupon, Grupo Bimbo, GSK, Hanson Bridgett LLP, HARMAN International, Haworth, HCL Technologies Limited, Hodgson Russ LLP, HP, Humana, Hyperoptic, IBM, IHG, IMG, Indeed, Ingenious Management Consulting, Inova Health System, Insight Global, Intuitive, Jacobs, JFrog Ltd, JM Family Enterprises, Inc., Johnson & Johnson, Johnson Controls, Juniper Networks, Kaplan, Kyndryl, Landis+Gyr, Levio, LG Electronics, Liberty University, Littelfuse, Logitech, London Stock Exchange, Lumen Technologies, Luxoft, Luxottica, Magic Leap, Magna International, MATRIX, Mattel, Inc., McKesson, Medline Industries, LP, Merkle, Meta, MetLife, Micron Technology, Microsoft, MicroStrategy, Montclair State University, Motorola Solutions, Mspark, NBCUniversal Media, LLC, nestle, NI (National Instruments), Nichols College Graduate and Professional Studies, North Carolina Department of Commerce, Northrop Grumman, Nova, Novartis, Novocure, NTT DATA Services, NXP Semiconductors, NYU college, Ogletree Deakins, OMSAR - Lebanon, Optum, Oracle, Orange County Public Schools, Otis Elevator Co., Panasonic Energy of North America, Paramount, Paypal, Pearson PLC, PepsiCo, Pfizer, PNC, Pontoon Solutions, primerica, Proskauer Rose LLP, Providence St. Joseph Health, PwC, Pyramid Consulting, Qlik, R.R. Donnelley & Sons Company, Red Hat, Inc, RITE AID, Riverbed, Rutgers University, Salesforce, Salesforce.com, Samsung (Laurent Moquet - l.moquet@samsung.com), Sanoma, SCI Solutions, Seyfarth Shaw LLP, Sheppard Mullin Richter & Hampton LLP, Shipt, SHRM, Silgan Plastics, Sonoco, Staffing Industry Analysts, State of Minnesota, Stoel Rives LLP, Stryker, Sutherland, Target, Tata Consultancy Services, TE Connectivity, Tech Mahindra Limited, TEKsystems, Teleflex Incorporated, TELUS International, Tenable, Tesla, The Carlyle Group, The George Washington University, The Home Depot, The Judge Group, The New York Times, The State University of New York, Thermo Fisher Scientific, Timeless Production, Travelers, Trend Micro, U.S. Bank, U.S. Department of Veterans Affairs, U.S. Small Business Administration, Uber, Ultimate Software, UPS, USAA, USDA OCIO-DISC Enterprise Network Services, Veolia, Vestas, VF Corporation, Vimeo, Visteon Corporation, VITAS Healthcare, Volvo Cars, W. L. Gore & Associates, Wabtec Corporation, Wake Forest Baptist Health, Walmart, Western Digital, WilsonHCG, Wolverine Worldwide, Zebra Technologies"
company_list = [company.strip() for company in company_names.split(",")]
company_input = driver.find_element(By.CSS_SELECTOR, '.artdeco-typeahead__input[placeholder="Add current companies and account lists"]')

for company in company_list:
    company_input.send_keys(company)
    time.sleep(4)  # Pause after typing the company name

    # Check if the name is present in the box (or if the correct suggestion has been made)
    if company not in company_input.get_attribute("value"):
        # Clear the input box and try again
        company_input.clear()
        company_input.send_keys(company)
        time.sleep(4)

    company_input.send_keys(Keys.RETURN)
    time.sleep(4)  # Pause after pressing ENTER

try:
    # Identify the dropdown button and click it
    dropdown_button_xpath = '//fieldset[@data-x-search-filter="CURRENT_TITLE"]//button[@aria-expanded="false"]'
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, dropdown_button_xpath))
    )
    dropdown_button.click()

    # Your provided input field HTML code
    title_input_xpath = '//input[@placeholder="Add current titles"]'
    title_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, title_input_xpath))
    )

# Input and search job titles one-by-one immediately after click
    titles = "procurement"
    title_list = [title.strip() for title in titles.split(",")]

    for title in title_list:
        title_input.clear()  # Clear the input field
        title_input.send_keys(title)  # Send the job title
        title_input.send_keys(Keys.RETURN)  # Press RETURN/Enter to begin the search
        time.sleep(random.uniform(3, 5))  # Random wait

except TimeoutException:
    print("Timed out waiting for the element to appear.")
    driver.save_screenshot('timeout_exception.png')
    print(driver.page_source[:1000])  # Print the first 1000 characters of the page source
    
except Exception as e:
    print(f"An error occurred: {str(e)}")

    time.sleep(30)  # Waiting after entering job titles

# Extract profiles and iterate through results pages
while True:
    profiles = driver.find_elements(By.XPATH, '//*[@id="search-results-container"]/*')
    
    # Extract data from each profile
    for profile in profiles:
        try:
            # Extraction logic based on provided selectors
            name_element = profile.find_element(By.XPATH, './/span[@data-anonymize="person-name"]')  
            title_element = profile.find_element(By.XPATH, './/span[@data-anonymize="title"]')  
            company_element = profile.find_element(By.XPATH, './/a[@data-anonymize="company-name"]')  
            
            name = name_element.text
            title = title_element.text
            company = company_element.text
            
            save_to_excel(name, title, company)
        except Exception as e:
            print(f"Error extracting profile data: {e}")

    # Scroll to the bottom of the right-pane search results
    scroll_to_element(driver, driver.find_element(By.CSS_SELECTOR, '.search-results-container'))

    # Wait for the 'next button' to be visible and clickable
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.pagination__next-button')))

    # Click next page if available
    try:
        next_button = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Next")]')
        if not next_button.is_enabled():
            break
        next_button.click()
        time.sleep(5)  # Give the page some time to load

    except Exception as e:
        print(f"Error encountered: {e}")
        break

driver.quit()
