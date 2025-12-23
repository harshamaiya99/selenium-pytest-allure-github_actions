from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):

    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "loginBtn")

    def open(self, base_url):
        self.driver.get(f"{base_url}/index.html")
        self.wait_for_title("Login")

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)
