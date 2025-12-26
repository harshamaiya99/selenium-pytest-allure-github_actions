from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class FormPage(BasePage):
    FULLNAME = (By.ID, "fullname")
    EMAIL = (By.ID, "email")
    DOB = (By.ID, "dob")  # New
    GENDER = (By.ID, "gender")
    LOAD_SKILLS_BTN = (By.ID, "loadSkillsBtn")  # New
    SKILL_INPUT = (By.ID, "skill_name")  # New (Dynamic)
    SUBSCRIBE = (By.ID, "subscribe")
    SUBMIT = (By.ID, "submitBtn")

    def wait_for_page(self):
        self.find(self.FULLNAME)

    def fill_form(self, fullname, email, dob, experience, gender, subscribe=False):
        self.wait_for_page()

        self.type(self.FULLNAME, fullname)
        self.type(self.EMAIL, email)
        self.type(self.DOB, dob)

        # Helper method from BasePage handles the XPath construction
        self.select_radio_by_value("experience", experience)

        self.select_by_text(self.GENDER, gender)

        # --- Dynamic Element Handling ---
        self.click(self.LOAD_SKILLS_BTN)
        try:
            # We reuse 'type' because BasePage.find() inside it
            # already implements an Explicit Wait for visibility
            self.type(self.SKILL_INPUT, "Python Selenium")
        except TimeoutException:
            raise TimeoutException(
                "Skills input did not appear after clicking 'Load Skills'. Check network delay or JS.")

        if subscribe:
            checkbox = self.find(self.SUBSCRIBE)
            if not checkbox.is_selected():
                checkbox.click()

    def submit(self):
        self.click(self.SUBMIT)
        self.handle_alert_if_present()