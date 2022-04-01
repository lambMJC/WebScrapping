from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import csv
import re

csvFile = open('ParcelID.csv', 'w')
writer = csv.writer(csvFile)

# making it where chrome opens in the background
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

class SearchBot:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager(log_level=0).install()), options=chrome_options)

    def Login(self, link):
        self.driver.get(link)
        print("application is ", self.driver.current_url)

        # <input type="submit" name="submit" value="Public Login"> For the login button
    def LoginClick(self, XP):
        l = self.driver.find_element(by=By.XPATH, value=XP)
        l.click()
        print("New page is ", self.driver.current_url)

    def AccountSearchClick(self, XP):
        self.driver.find_element(by=By.XPATH, value=XP).click()
        print("The Account Search Website is ", self.driver.current_url)

        # clicking into the parcelID search box
    def SearchBox(self, XP, click):
        s = self.driver.find_element(by=By.XPATH, value=XP)
        s.click()
        print("Enter Parcel ID#: ")
        s.send_keys(input())
        f = self.driver.find_element(by=By.XPATH, value=click)
        f.click()
        print("Showing the results ", self.driver.current_url)

    def Error(self, results, AccountSummary, SearchXP, clickPIDSearch):
        for i in range(100):
            try:
                self.driver.find_element(by=By.XPATH, value=results).click()
                print("WE FOUND SOMETHING, PLEASE WAIT")

                tbl = self.driver.find_element(by=By.XPATH, value=AccountSummary)
                print(tbl.text)

                i = 0
                for string in tbl.text.split(' '):
                    if '\n' in string:
                        break
                    else:
                        i += 1
                values = re.split('\n', tbl.text)

            except (ElementNotVisibleException, NoSuchElementException):
                self.driver.find_element(by=By.XPATH, value='//*[@id="nav"]/ul/li[2]/a').click()
                s2 = self.driver.find_element(by=By.XPATH, value=SearchXP)
                s2.click()
                print("Enter Parcel ID#:")
                s2.send_keys(input())
                f2 = self.driver.find_element(by=By.XPATH, value=clickPIDSearch)
                f2.click()
                print("Showing the results ", self.driver.current_url)


if __name__ == "__main__":
    Search_Bot = SearchBot()
    Search_Bot.Login("http://eweb.washco.utah.gov:8080/recorder/web/login.jsp")
    Search_Bot.LoginClick('//*[@id="middle_left"]/form/input[1]')
    Search_Bot.AccountSearchClick('//*[@id="nav"]/ul/li[2]/a')
    Search_Bot.SearchBox('//*[@id="ParcelNumID"]', '//*[@id="middle"]/form/table[6]/tbody/tr/td[1]/input')
    Search_Bot.Error('//*[@id="searchResultsTable"]/tbody/tr[2]/td[2]', '//*[@id="middle"]/table', '//*[@id="ParcelNumID"]', '//*[@id="middle"]/form/table[6]/tbody/tr/td[1]/input')

