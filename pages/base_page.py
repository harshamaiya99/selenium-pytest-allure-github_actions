import allure
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class BasePage:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def log(self, message):
        """Logs a message to Allure."""
        with allure.step(message):
            pass

    # Simplified 'find' to strictly handle waiting and returning.
    # We removed the manual try/catch/screenshot here. If this fails, it raises a standard TimeoutException which the test runner will catch and report.
    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator, description=None):
        desc = description or str(locator)
        self.log(f"Clicking on {desc}")
        try:
            # Explicitly waiting for element to be clickable is safer than just visible
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except ElementClickInterceptedException:
            self.log(f"Intercepted! Forcing JS click on {desc}")
            self.js_click(locator, description)

    def js_click(self, locator, description=None):
        desc = description or str(locator)
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text, description=None):
        desc = description or str(locator)
        # masking password in logs for security
        display_text = "*****" if "password" in desc.lower() else text

        self.log(f"Typing '{display_text}' into {desc}")
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def select_by_text(self, locator, text, description=None):
        desc = description or str(locator)
        self.log(f"Selecting '{text}' from {desc}")
        select = Select(self.find(locator))
        select.select_by_visible_text(text)

    def select_radio_by_value(self, name, value):
        self.log(f"Selecting Radio: name='{name}' value='{value}'")
        xpath = (By.XPATH, f"//input[@name='{name}' and @value='{value}']")
        self.js_click(xpath, description=f"Radio {value}")

    def wait_for_title(self, title_fragment):
        self.log(f"Waiting for title to contain '{title_fragment}'")
        self.wait.until(EC.title_contains(title_fragment))

    def handle_alert(self):
        try:
            alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            self.log(f"Accepting alert: {alert.text}")
            alert.accept()
        except TimeoutException:
            pass