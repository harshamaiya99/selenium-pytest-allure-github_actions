import allure
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

class BasePage:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        """Find element with robust error handling for Timeouts."""
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            # Attach screenshot on failure to find element
            self.take_screenshot(f"Element_Not_Found_{locator}")
            raise TimeoutException(f"Element {locator} not visible after {self.timeout} seconds.")

    def click(self, locator):
        try:
            element = self.find(locator)
            self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except ElementClickInterceptedException:
            # Fallback: JavaScript click if normal click is intercepted
            element = self.driver.find_element(*locator)
            self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def select_by_text(self, locator, text):
        try:
            Select(self.find(locator)).select_by_visible_text(text)
        except NoSuchElementException:
            raise NoSuchElementException(f"Option '{text}' not found in dropdown {locator}")

    def select_radio_by_value(self, name, value):
        """Specific helper for radio button groups."""
        xpath = (By.XPATH, f"//input[@name='{name}' and @value='{value}']")
        self.click(xpath)

    def wait_for_title(self, title):
        try:
            self.wait.until(EC.title_contains(title))
        except TimeoutException:
            raise TimeoutException(f"Title '{title}' did not appear. Current title: {self.driver.title}")

    def handle_alert_if_present(self):
        try:
            alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            alert.accept()
        except TimeoutException:
            pass # No alert present, strictly acceptable

    def take_screenshot(self, name="screenshot"):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )