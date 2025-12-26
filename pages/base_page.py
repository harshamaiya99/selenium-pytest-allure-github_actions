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

    def log(self, message, screenshot=False):
        """Logs a message to Allure and optionally takes a screenshot."""
        with allure.step(message):
            print(message)
            if screenshot:
                self.take_screenshot(message)

    def find(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            self.take_screenshot(f"Element_Not_Found_{locator}")
            raise TimeoutException(f"Element {locator} not visible after {self.timeout} seconds.")

    def click(self, locator, description=None):
        element_desc = description or str(locator)
        self.log(f"Clicking on {element_desc}")
        try:
            element = self.find(locator)
            self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except ElementClickInterceptedException:
            self.log(f"Intercepted! forcing JS click on {element_desc}")
            self.js_click(locator, description)

    def js_click(self, locator, description=None):
        """Forces a click using JavaScript, bypassing overlay/coordinate issues."""
        element_desc = description or str(locator)
        self.log(f"JS Clicking on {element_desc}")
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text, description=None):
        element_desc = description or str(locator)
        log_text = "*****" if "password" in element_desc.lower() else text
        self.log(f"Typing '{log_text}' into {element_desc}")
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def select_by_text(self, locator, text, description=None):
        element_desc = description or str(locator)
        self.log(f"Selecting '{text}' from {element_desc}")
        try:
            Select(self.find(locator)).select_by_visible_text(text)
        except NoSuchElementException:
            self.take_screenshot(f"Option_Not_Found_{text}")
            raise NoSuchElementException(f"Option '{text}' not found in {element_desc}")

    def select_radio_by_value(self, name, value, description=None):
        desc = description or f"Radio '{name}' value '{value}'"
        xpath = (By.XPATH, f"//input[@name='{name}' and @value='{value}']")
        self.js_click(xpath, desc)

    def wait_for_title(self, title):
        self.log(f"Waiting for title to contain '{title}'")
        try:
            self.wait.until(EC.title_contains(title))
        except TimeoutException:
            self.take_screenshot("Title_Mismatch")
            raise TimeoutException(f"Title '{title}' did not appear. Current title: {self.driver.title}")

    def handle_alert_if_present(self):
        """
        Handles an alert if it appears.
        NOTE: We cannot take a screenshot here because the alert blocks the driver.
        """
        try:
            alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())
            text = alert.text
            # CHANGED: screenshot=False because taking a screenshot while alert is open crashes the driver
            self.log(f"Accepting alert with text: '{text}'", screenshot=False)
            alert.accept()
        except TimeoutException:
            pass

    def take_screenshot(self, name="screenshot"):
        """Safe screenshot wrapper."""
        try:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name=name,
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")