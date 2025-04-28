from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
import time
from datetime import datetime
from pathlib import Path
import shutil


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

years = []
if int(current_month) < 12: 
    for i in range(start_year, current_year + 1, 1):
        years.append(str(i))
else:
    for i in range(start_year, current_year, 1):
        years.append(str(i))

#  Debugging statements
# print(years)
# print(type(years[0]))

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


station_link = WebDriverWait(driver,5).until(
    EC.element_to_be_clickable((By.ID,"cityname"))
)
station_link.click()
time.sleep(1)


for year in years:
    last_href = ""
    print(f"Processing year: {year}")     
    dropdown_year = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "year"))
            )
    dropdown_year.click()

    year_link = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.LINK_TEXT, year))
    )
    year_link.click()

    time.sleep(1)

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

            found = False
            try:
                january_item = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, month))  # where month = "January"
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", january_item)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", january_item)
                print(f"✅ Clicked {month} successfully")
                found = True

                time.sleep(1)
                
                # 1. Scroll back to top of the page
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)  # Let the scroll settle

                # 2. Re-fetch the month dropdown to ensure it's fresh in the DOM
                try:
                    dropdown_month = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "month"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown_month)
                    print("🔼 Scrolled back to month dropdown")
                except Exception as e:
                    print(f"⚠️ Failed to scroll back to dropdown: {e}")
                    continue  # Skip to next month/year if dropdown can't be found

            except:
                print(f"⚠️ {month} not visible after April scroll — falling back to incremental scroll...")


            time.sleep(1)
    
            # driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", month_link)

            print("Month Clicked", month)

            # Wait for the "display" button to be clickable and then click it
            display_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "display"))
            )
            display_button.click()  

            time.sleep(1)

            def new_href_loaded(driver):
                try:
                    link = driver.find_element(By.CSS_SELECTOR, "a.myload[href$='.csv']")
                    href = link.get_attribute("href")
                    return href if href != last_href else False
                except:
                    return False
                
            csv_href = WebDriverWait(driver,10).until(new_href_loaded)
            last_href = csv_href

            try:
                csv_link = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, f"a.myload[href='{csv_href}']"))
                )
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", csv_link)
                time.sleep(1)
                driver.execute_script("arguments[0].click();", csv_link)
                print("Download triggered:", csv_href)
            except Exception as e:
                print(f"⚠️ Failed to click CSV for {month} {year}: {e}")
                continue

            # Wait for download to complete (basic wait)
            # time.sleep(2)
            # Wait up to 10 seconds for file to appear
            wait_time = 0
            while not source_path.exists() and wait_time < 10:
                time.sleep(1)
                wait_time += 1

            if source_path.exists():
                shutil.move(str(source_path), str(target_path))
                print(f"📁 Moved {filename} to {target_path}")
            else:
                print(f"⚠️ File not found after waiting 10s: {filename}")

            # Move downloaded file to the correct folder
            station_name = "Changi"
            output_folder = Path("downloads") / station_name / f"{year}"
            output_folder.mkdir(parents=True, exist_ok=True)

            filename = csv_href.split("/")[-1]
            source_path = Path.home() / "Downloads" / filename
            target_path = output_folder / filename

            try:
                shutil.move(str(source_path), str(target_path))
                print(f"📁 Moved {filename} to {target_path}")
            except FileNotFoundError:
                print(f"⚠️ File not found (maybe download not finished yet?): {filename}")




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



