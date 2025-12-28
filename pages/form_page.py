from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class FormPage(BasePage):
    # Locators
    FULLNAME = (By.ID, "fullname")
    EMAIL = (By.ID, "email")
    DOB = (By.ID, "dob")
    GENDER = (By.ID, "gender")

    # Async Skills Locators
    LOAD_SKILLS_BTN = (By.ID, "loadSkillsBtn")
    SKILLS_CONTAINER = (By.ID, "skills-container")
    SKILL_INPUT = (By.ID, "skill_name")

    SUBSCRIBE = (By.ID, "subscribe")
    SUBMIT = (By.ID, "submitBtn")

    def wait_for_load(self):
        self.wait_for_title("Form Page")
        self.find(self.FULLNAME)

    # PLAN 1: Single Responsibility Principle
    # Instead of one giant 'fill_form' method, we have specific methods for specific sections.

    def enter_personal_details(self, fullname, email, dob, experience, gender):
        self.type(self.FULLNAME, fullname, "Full Name")
        self.type(self.EMAIL, email, "Email")
        self.type(self.DOB, dob, "Date of Birth")  # Using type as discussed

        self.select_radio_by_value("experience", experience)
        self.select_by_text(self.GENDER, gender, "Gender Dropdown")

    def add_skill(self, skill_name):
        """
        Handles the async nature of the skills section separately.
        If the container doesn't appear, 'find' will raise TimeoutException naturally.
        """
        self.js_click(self.LOAD_SKILLS_BTN, "Load Skills Button")

        self.log("Waiting for skills container to appear...")
        self.find(self.SKILLS_CONTAINER)

        self.type(self.SKILL_INPUT, skill_name, "Skill Input")

    def set_subscription(self, should_subscribe):
        checkbox = self.find(self.SUBSCRIBE)
        is_selected = checkbox.is_selected()

        if should_subscribe and not is_selected:
            self.js_click(self.SUBSCRIBE, "Subscribe Checkbox")
        elif not should_subscribe and is_selected:
            self.js_click(self.SUBSCRIBE, "Unsubscribe Checkbox")

    def submit_form(self):
        self.js_click(self.SUBMIT, "Submit Button")
        self.handle_alert()