from selenium.webdriver.common.by import By  # Locator strategies
from pages.base_page import BasePage  # Import base page helpers


class LoginPage(BasePage):

    USERNAME = (By.ID, "username")  # Username input locator
    PASSWORD = (By.ID, "password")  # Password input locator
    LOGIN_BTN = (By.ID, "loginBtn")  # Login button locator

    def open(self, base_url):
        url = f"{base_url}/index.html"  # Build URL for the login page
        self.log(f"Navigating to {url}")  # Log navigation step
        self.driver.get(url)  # Navigate the browser to the login page
        self.wait_for_title("Login")  # Wait until the page title contains 'Login'

    def login(self, username, password):
        self.type(self.USERNAME, username, "Username Input")  # Enter the username
        self.type(self.PASSWORD, password, "Password Input")  # Enter the password
        self.click(self.LOGIN_BTN, "Login Button")  # Click the login button