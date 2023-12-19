from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

import time
import json

chrome_options = Options()
chrome_options.binary_location = r".\geckodriver.exe"

browser = webdriver.Firefox(options=chrome_options)

browser.get('https://deprem.afad.gov.tr/last-earthquakes')
time.sleep(5)
xpath_to_click = "//*[@id='mainContent']/div/div/div/div[2]/div/div/kendo-grid/kendo-grid-toolbar/kendo-combobox/span/span[2]"
browser.find_element(By.XPATH, xpath_to_click).click()
time.sleep(2)
xpath_last_30_days = "//li[contains(text(), 'Last 30 Day')]"
browser.find_element(By.XPATH, xpath_last_30_days).click()


data_list = []

target_page_count = 167
page_count = 1

for page_count in range(1, target_page_count + 1):
    rows = browser.find_elements(By.XPATH, "//table[@class='k-grid-table']/tbody/tr")
    for row in rows:
        data = {
            'Date(TS)': row.find_element(By.XPATH, "./td[1]").text.strip(),
            'Latitude': row.find_element(By.XPATH, "./td[2]").text.strip(),
            'Longitude': row.find_element(By.XPATH, "./td[3]").text.strip(),
            'Depth': row.find_element(By.XPATH, "./td[4]").text.strip(),
            'Type': row.find_element(By.XPATH, "./td[5]").text.strip(),
            'Magnitude': row.find_element(By.XPATH, "./td[6]").text.strip(),
            'Location': row.find_element(By.XPATH, "./td[7]").text.strip(),
            'EventID': row.find_element(By.XPATH, "./td[8]").text.strip(),
        }
        data_list.append(data)

    try:
        if page_count < target_page_count:
            page_count = page_count + 1
            browser.find_element(By.XPATH, f"//*[@id='mainContent']/div/div/div/div[2]/div/div/kendo-grid/kendo-pager/kendo-pager-numeric-buttons/ul/li[{page_count}]/a").click()
            time.sleep(5)
    except Exception as e:
        print("Veri çekme tamamlandı.")
        break

time.sleep(5)

with open('earthquake_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=2)

browser.quit()
