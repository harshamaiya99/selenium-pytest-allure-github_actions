import csv  # CSV helper to load test data from file
import pytest  # pytest testing framework
import allure  # Allure reporting for features/stories and steps
from pages.login_page import LoginPage  # Page object for login interactions
from pages.form_page import FormPage  # Page object for form interactions


def load_test_data():
    with open("tests/test_data.csv") as f:  # Open the CSV file containing test rows
        return list(csv.DictReader(f))  # Return a list of dictionaries (one per row)


@allure.feature("E2E Web Testing")  # High-level feature label for Allure
@allure.story("Login and Form Submission")  # Story label within the feature
@pytest.mark.parametrize("data", load_test_data())  # Parameterize the test over rows from CSV
def test_login_and_form(driver, base_url, data):
    login_page = LoginPage(driver)  # Instantiate the login page object
    form_page = FormPage(driver)  # Instantiate the form page object

    with allure.step(f"Open login page at {base_url}"):
        login_page.open(base_url)  # Open the login page

    with allure.step(f"Login as {data['username']}"):
        login_page.login(data["username"], data["password"])  # Perform login with credentials from CSV

    with allure.step("Wait for form page"):
        form_page.wait_for_load()  # Wait until the form page has loaded

    # PLAN 1 in action: The test now orchestrates the steps, making it easier to read/debug

    with allure.step("Fill Personal Details"):
        form_page.enter_personal_details(
            fullname=data["fullname"],  # Full name from CSV
            email=data["email"],  # Email from CSV
            dob=data["dob"],  # DOB from CSV
            experience=data["experience"],  # Experience value from CSV
            gender=data["gender"]  # Gender text from CSV
        )

    with allure.step("Add Skill (Async)"):
        # We can pass specific skills here or from data
        form_page.add_skill("Python Selenium")  # Add a skill via the async section

    with allure.step("Set Subscription"):
        # Convert string 'true'/'false' from CSV to boolean
        should_subscribe = data["subscribe"].lower() == "true"  # Parse subscription flag from CSV
        form_page.set_subscription(should_subscribe)  # Set checkbox accordingly

    with allure.step("Submit form"):
        form_page.submit_form()  # Submit the form and handle alert