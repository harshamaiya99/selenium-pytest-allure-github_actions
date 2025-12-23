from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class FormPage(BasePage):

    FULLNAME = (By.ID, "fullname")
    EMAIL = (By.ID, "email")
    GENDER = (By.ID, "gender")
    SUBSCRIBE = (By.ID, "subscribe")
    SUBMIT = (By.ID, "submitBtn")

    def wait_for_page(self):
        self.find(self.FULLNAME)

    def fill_form(self, fullname, email, gender, subscribe=False):
        self.wait_for_page()

        self.type(self.FULLNAME, fullname)
        self.type(self.EMAIL, email)
        self.select_by_text(self.GENDER, gender)

        if subscribe:
            self.click(self.SUBSCRIBE)

    def submit(self):
        self.click(self.SUBMIT)
        self.handle_alert_if_present()
