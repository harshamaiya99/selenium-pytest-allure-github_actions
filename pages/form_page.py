from selenium.webdriver.common.by import By  # Locator strategies
from pages.base_page import BasePage  # BasePage with common helpers


class FormPage(BasePage):
    # Locators
    FULLNAME = (By.ID, "fullname")  # Input for full name
    EMAIL = (By.ID, "email")  # Input for email
    DOB = (By.ID, "dob")  # Input for date of birth
    GENDER = (By.ID, "gender")  # Dropdown for gender

    # Async Skills Locators
    LOAD_SKILLS_BTN = (By.ID, "loadSkillsBtn")  # Button that triggers async load of skills
    SKILLS_CONTAINER = (By.ID, "skills-container")  # Container that appears after loading skills
    SKILL_INPUT = (By.ID, "skill_name")  # Input for the skill name

    SUBSCRIBE = (By.ID, "subscribe")  # Subscribe checkbox
    SUBMIT = (By.ID, "submitBtn")  # Submit button

    def wait_for_load(self):
        self.wait_for_title("Form Page")  # Wait until the title indicates the form page
        self.find(self.FULLNAME)  # Ensure the fullname input is visible

    # PLAN 1: Single Responsibility Principle
    # Instead of one giant 'fill_form' method, we have specific methods for specific sections.

    def enter_personal_details(self, fullname, email, dob, experience, gender):
        self.type(self.FULLNAME, fullname, "Full Name")  # Type fullname into fullname input
        self.type(self.EMAIL, email, "Email")  # Type email into email input
        self.type(self.DOB, dob, "Date of Birth")  # Type DOB into dob input

        self.select_radio_by_value("experience", experience)  # Select the experience radio by value
        self.select_by_text(self.GENDER, gender, "Gender Dropdown")  # Select the gender option by text

    def add_skill(self, skill_name):
        """
        Handles the async nature of the skills section separately.
        If the container doesn't appear, 'find' will raise TimeoutException naturally.
        """
        self.js_click(self.LOAD_SKILLS_BTN, "Load Skills Button")  # Click the button that loads skills asynchronously

        self.log("Waiting for skills container to appear...")  # Log waiting for skills area
        self.find(self.SKILLS_CONTAINER)  # Wait for the skills container to become visible

        self.type(self.SKILL_INPUT, skill_name, "Skill Input")  # Type the skill into the skill input

    def set_subscription(self, should_subscribe):
        checkbox = self.find(self.SUBSCRIBE)  # Find the subscribe checkbox
        is_selected = checkbox.is_selected()  # Check current selection state

        if should_subscribe and not is_selected:
            self.js_click(self.SUBSCRIBE, "Subscribe Checkbox")  # Click to subscribe if not already
        elif not should_subscribe and is_selected:
            self.js_click(self.SUBSCRIBE, "Unsubscribe Checkbox")  # Click to unsubscribe if currently selected

    def submit_form(self):
        self.js_click(self.SUBMIT, "Submit Button")  # Click submit via JS to avoid interception
        self.handle_alert()  # Handle the confirmation alert that appears after submit