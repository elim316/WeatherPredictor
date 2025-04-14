from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
import time
from datetime import datetime

# What I want to do for this webscraper
# 1. Open the website
# 2. Download the data in csv for the month for the selected station
# 3. Click the dropdown box to navigate to the previous month
# 4. Repeat the process for the previous month
# 5. Stop when there is 5 years of data
# 6. Save the data in a folder named after the station
# 7. Repeat on other stations

# Get current date and time
now = datetime.now()
current_month = now.month
current_year = now.year

start_year = current_year - 5
start_month = current_month

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

target_months = []
for year in range(start_year, current_year, 1):
    for i, month in enumerate(months, 1):
        if (year == current_year and i > current_month):
            break # this is future months
        target_months.append((month,year))


# print(target_months)

# Make the browser visible
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # keeps browser open

driver = webdriver.Chrome(options=options)
driver.get("https://www.weather.gov.sg/climate-historical-daily/")


last_href = ""


# Select the month
for month in months:
    try:
        print(f"\nProcessing: {month}")

        # First click drowndown 
        dropdown_month = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "month"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_month)
        dropdown_month.click()

        # Select the month
        month_link = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.LINK_TEXT, month))
        )
        month_link.click()
        print("Month Clicked", month)

        # Wait for the "display" button to be clickable and then click it
        display_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "display"))
        )
        display_button.click()  

        def new_href_loaded(driver):
            try:
                link = driver.find_element(By.CSS_SELECTOR, "a.myload[href$='.csv']")
                href = link.get_attribute("href")
                return href if href != last_href else False
            except:
                return False
            
        csv_href = WebDriverWait(driver,10).until(new_href_loaded)
        last_href = csv_href

        # Click on download CSV format
        csv_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.myload[href$='.csv']"))
        )    
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", csv_link)
        time.sleep(0.5)
        print("Found CSV link:", csv_link.get_attribute("href"))
        csv_link.click()

        time.sleep(1)

        # Scroll back up for next month
        dropdown_month = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "month"))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_month)
        time.sleep(2)



    

    except Exception as e:
        print(f"Error occurred for month {month}: {e}")




driver.close()
driver.quit()



