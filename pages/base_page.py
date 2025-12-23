import allure
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class BasePage:

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.find(locator).click()

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def select_by_text(self, locator, text):
        Select(self.find(locator)).select_by_visible_text(text)

    def wait_for_title(self, title):
        self.wait.until(EC.title_contains(title))

    def handle_alert_if_present(self):
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert.accept()
        except:
            pass

    def take_screenshot(self, name="screenshot"):
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )