from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

# making it where chrome opens in the background
chrome_options = Options()
chrome_options.add_argument("--headless")


class SearchBot:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def Login(self, link):
        self.driver.get(link)
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

    def Error(self, results, SearchXP, clickPIDSearch):
        for i in range(100):
            try:
                self.driver.find_element(by=By.XPATH, value=results).click()
                print("WE FOUND SOMETHING, exporting information into an excel worksheet!")

                break
            except (ElementNotVisibleException, NoSuchElementException):
                self.driver.find_element(by=By.XPATH, value='//*[@id="nav"]/ul/li[2]/a').click()
                s2 = self.driver.find_element(by=By.XPATH, value=SearchXP)
                s2.click()
                print("No results found, Enter Parcel ID#:")
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
    Search_Bot.Error('//*[@id="searchResultsTable"]/tbody/tr[2]/td[2]', '//*[@id="ParcelNumID"]', '//*[@id="middle"]/form/table[6]/tbody/tr/td[1]/input')

