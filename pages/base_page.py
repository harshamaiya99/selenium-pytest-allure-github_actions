import allure  # Allure reporting utilities for steps and attachments
from selenium.webdriver.support.ui import WebDriverWait, Select  # Wait helpers and Select element wrapper
from selenium.webdriver.support import expected_conditions as EC  # Expected conditions for waits
from selenium.webdriver.common.by import By  # Locator strategies (By.ID, By.XPATH, etc.)
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException  # Common Selenium exceptions


class BasePage:

    def __init__(self, driver, timeout=10):
        self.driver = driver  # Selenium WebDriver instance used for interactions
        self.timeout = timeout  # Default timeout for waits
        self.wait = WebDriverWait(driver, timeout)  # WebDriverWait instance bound to the driver and timeout

    def log(self, message):
        """Logs a message to Allure."""
        with allure.step(message):
            pass  # Use an Allure step to record the message in the report

    # Simplified 'find' to strictly handle waiting and returning.
    # We removed the manual try/catch/screenshot here. If this fails, it raises a standard TimeoutException which the test runner will catch and report.
    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))  # Wait until the element is visible and return it

    def click(self, locator, description=None):
        desc = description or str(locator)  # Human-friendly description for logging
        self.log(f"Clicking on {desc}")  # Log the click action to Allure
        try:
            # Explicitly waiting for element to be clickable is safer than just visible
            element = self.wait.until(EC.element_to_be_clickable(locator))  # Wait until clickable
            element.click()  # Perform the click via Selenium
        except ElementClickInterceptedException:
            self.log(f"Intercepted! Forcing JS click on {desc}")  # Log interception and fallback
            self.js_click(locator, description)  # Use JS click as a fallback to avoid interception issues

    def js_click(self, locator, description=None):
        desc = description or str(locator)  # Description used for logging
        element = self.find(locator)  # Reuse find to get the element (ensures visibility)
        self.driver.execute_script("arguments[0].click();", element)  # Execute a JS click on the element

    def type(self, locator, text, description=None):
        desc = description or str(locator)  # Description for logging context
        # masking password in logs for security
        display_text = "*****" if "password" in desc.lower() else text  # Mask password-like inputs in logs

        self.log(f"Typing '{display_text}' into {desc}")  # Log what is being typed (masked if needed)
        element = self.find(locator)  # Find the input element
        element.clear()  # Clear existing text in the input
        element.send_keys(text)  # Send the provided text to the input

    def select_by_text(self, locator, text, description=None):
        desc = description or str(locator)  # Logging description
        self.log(f"Selecting '{text}' from {desc}")  # Log the selection action
        select = Select(self.find(locator))  # Wrap the element in a Select helper
        select.select_by_visible_text(text)  # Select option by visible text

    def select_radio_by_value(self, name, value):
        self.log(f"Selecting Radio: name='{name}' value='{value}'")  # Log radio selection
        xpath = (By.XPATH, f"//input[@name='{name}' and @value='{value}']")  # Build an XPath locator for the radio
        self.js_click(xpath, description=f"Radio {value}")  # Click the radio via JS to avoid interception issues

    def wait_for_title(self, title_fragment):
        self.log(f"Waiting for title to contain '{title_fragment}'")  # Log title wait
        self.wait.until(EC.title_contains(title_fragment))  # Wait until the page title contains the fragment

    def handle_alert(self):
        try:
            alert = WebDriverWait(self.driver, 3).until(EC.alert_is_present())  # Wait briefly for an alert to appear
            self.log(f"Accepting alert: {alert.text}")  # Log alert text for debugging
            alert.accept()  # Accept the alert (click OK)
        except TimeoutException:
            pass  # If no alert appears within timeout, do nothing