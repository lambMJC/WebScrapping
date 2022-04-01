from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import csv
import re

csvFile = open('ParcelID.csv', 'w')
writer = csv.writer(csvFile)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
print("LOADING, PLEASE WAIT.")

driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0).install()), options=chrome_options)

link = "http://eweb.washco.utah.gov:8080/recorder/web/login.jsp"
XP = '//*[@id="middle_left"]/form/input[1]'
AccountXP = '//*[@id="nav"]/ul/li[2]/a'
click = '//*[@id="middle_left"]/form/input[1]'
SearchXP = '//*[@id="ParcelNumID"]'
clickPIDSearch = '//*[@id="middle"]/form/table[6]/tbody/tr/td[1]/input'
results = '//*[@id="searchResultsTable"]/tbody/tr[2]/td[2]'
AccountSummary = '//*[@id="middle"]/table'

driver.get(link)
print("application is ", driver.current_url)

l = driver.find_element(by=By.XPATH, value=XP)
l.click()
print("New page is ", driver.current_url)

driver.find_element(by=By.XPATH, value=AccountXP).click()
print("The Account Search Website is ", driver.current_url)

s = driver.find_element(by=By.XPATH, value=SearchXP)
s.click()
print("Enter Parcel ID#: ")
s.send_keys(input())
f = driver.find_element(by=By.XPATH, value=clickPIDSearch)
f.click()
print("Showing the results ", driver.current_url)
for i in range(100):
    try:
        driver.find_element(by=By.XPATH, value=results).click()
        print("WE FOUND SOMETHING. EXPORTING, PLEASE WAIT")

        tbl = driver.find_element(by=By.XPATH, value=AccountSummary)
        print(tbl.text)

        i = 0
        for string in tbl.text.split(' '):
            if '\n' in string:
                break
            else:
                i += 1
        values = re.split('\n', tbl.text)

#       print("Everything is exported, try another one")

    except (ElementNotVisibleException, NoSuchElementException):
        driver.find_element(by=By.XPATH, value='//*[@id="nav"]/ul/li[2]/a').click()
        s2 = driver.find_element(by=By.XPATH, value=SearchXP)
        s2.click()
        print("Enter Parcel ID#:")
        s2.send_keys(input())
        f2 = driver.find_element(by=By.XPATH, value=clickPIDSearch)
        f2.click()
        print("Showing the results ", driver.current_url)


driver.quit()
