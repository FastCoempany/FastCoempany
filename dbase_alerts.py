from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def login_to_stockanalysis():
    driver.get("https://stockanalysis.com/stocks/")
    close_popups()

    try:
        # Click the Log In button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log In']"))).click()
        print("Clicked on Log In button.")
    except Exception as e:
        print(f"Failed to click on Log In button: {e}")
        close_popups()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log In']"))).click()

    try:
        email_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > div > form > input:nth-child(2)")))
        email_box.send_keys("mrcoe7@gmail.com")
        print("Entered email.")
        
        password_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        password_box.send_keys("FpUXFp8!JypLC78")
        print("Entered password.")
        
        # Click the Log In button after entering credentials
        login_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log In']")))
        login_btn.click()
        print("Submitted login form.")
        
    except Exception as e:
        print(f"Failed to enter email and/or password: {e}")
        close_popups()
        email_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > div > form > input:nth-child(2)")))
        email_box.send_keys("mrcoe7@gmail.com")
        password_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        password_box.send_keys("FpUXFp8!JypLC78")
        login_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log In']")))
        login_btn.click()

def close_popups():
    try:
        # Close any pop-ups
        popup_close = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'close')]"))
        )
        popup_close.click()
    except Exception as e:
        print(f"Error while closing popups: {e}")
        # If there's no pop-up, it's fine, continue
        pass

def get_ticker_from_stockanalysis(company_name):
    try:
        company_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//td[text()='{company_name}']"))
        )
        ticker_element = company_element.find_element_by_xpath("../td[1]")
        return ticker_element.text.strip()
    except:
        print(f"Failed to find ticker for {company_name}")
        return None

def find_10k_link(ticker):
    if not ticker:
        return None
    url = "https://www.sec.gov/edgar/searchedgar/companysearch.html"
    driver.get(url)
    time.sleep(2)

    search_box = driver.find_element(By.ID, "edgar-company-person")
    search_box.send_keys(ticker)
    time.sleep(1)

    # Use the dropdown to select the ticker 
    try:
        # More generic XPath in case the exact title match isn't working
        dropdown_item = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(),'{ticker}')]"))
        )
        dropdown_item.click()
    except:
        print(f"Failed to find dropdown for {ticker}")
        return None
    
    time.sleep(1)

    # Click the "Search" button on the EDGAR page
    try:
        search_btn = driver.find_element(By.XPATH, "//button[text()='Search']")
        search_btn.click()
    except:
        print("Failed to find or click the Search button on EDGAR. Pressing RETURN instead.")
        search_box.send_keys(Keys.RETURN)  # If button isn't found or fails, try pressing RETURN instead.
    
    time.sleep(3)

    expand_button = driver.find_element_by_xpath("//a[text()='[+]']")
    expand_button.click()
    time.sleep(2)

    ten_k_link_element = driver.find_element_by_xpath("//h5[contains(text(), '10-K')]/following-sibling::table//a")
    ten_k_link = ten_k_link_element.get_attribute("href")

    return ten_k_link

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.maximize_window()

login_to_stockanalysis()

file_path = '~/Desktop/dbase_slack_alerts/Organized Alerts.xlsx'
df = pd.read_excel(file_path)

unique_companies = df['Account'].unique()

ticker_mapping = {}
ten_k_link_mapping = {}

for company in unique_companies:
    ticker = get_ticker_from_stockanalysis(company)
    ticker_mapping[company] = ticker
    if ticker:
        ten_k_link = find_10k_link(ticker)
        ten_k_link_mapping[company] = ten_k_link

df['Ticker'] = df['Account'].map(ticker_mapping)
df['10-K Link'] = df['Account'].map(ten_k_link_mapping)
df.to_excel(file_path, index=False)

driver.quit()











