from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class FormPage(BasePage):
    # ... (Locators remain the same) ...
    FULLNAME = (By.ID, "fullname")
    EMAIL = (By.ID, "email")
    DOB = (By.ID, "dob")
    GENDER = (By.ID, "gender")
    LOAD_SKILLS_BTN = (By.ID, "loadSkillsBtn")
    SKILL_INPUT = (By.ID, "skill_name")
    SUBSCRIBE = (By.ID, "subscribe")
    SUBMIT = (By.ID, "submitBtn")

    def wait_for_page(self):
        self.log("Waiting for Form Page to load")
        self.find(self.FULLNAME)

    def fill_form(self, fullname, email, dob, experience, gender, subscribe=False):
        self.wait_for_page()

        self.type(self.FULLNAME, fullname, "Full Name Input")
        self.type(self.EMAIL, email, "Email Input")
        self.type(self.DOB, dob, "Date of Birth Picker")

        self.select_radio_by_value("experience", experience, f"Experience {experience} Years")
        self.select_by_text(self.GENDER, gender, "Gender Dropdown")

        # The Click call below now uses the robust Scroll+Click from BasePage
        self.click(self.LOAD_SKILLS_BTN, "Load Skills Button")

        self.log("Waiting for Skills input to appear (Async)...")
        try:
            self.type(self.SKILL_INPUT, "Python Selenium", "Skills Input")
        except TimeoutException:
            # If this raises, it means the click definitely didn't trigger the JS
            # even after our robust retry, or the network/JS is truly broken.
            raise TimeoutException(
                "Skills input did not appear after clicking 'Load Skills'. Check network delay or JS.")

        if subscribe:
            checkbox = self.find(self.SUBSCRIBE)
            if not checkbox.is_selected():
                self.click(self.SUBSCRIBE, "Subscribe Checkbox")

    def submit(self):
        self.click(self.SUBMIT, "Submit Button")
        self.handle_alert_if_present()