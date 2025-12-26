import csv
import pytest
import allure
from pages.login_page import LoginPage
from pages.form_page import FormPage

def load_test_data():
    with open("tests/test_data.csv") as f:
        return list(csv.DictReader(f))

@allure.feature("E2E Web Testing")
@allure.story("Login and Form Submission")
@pytest.mark.parametrize("data", load_test_data())
def test_login_and_form(driver, base_url, data):

    login_page = LoginPage(driver)
    form_page = FormPage(driver)

    with allure.step(f"Open login page at {base_url}"):
        login_page.open(base_url)

    with allure.step(f"Login as {data['username']}"):
        login_page.login(data["username"], data["password"])

    with allure.step("Wait for form page"):
        form_page.wait_for_page()
        assert "Form" in driver.title

    with allure.step("Fill extended form"):
        form_page.fill_form(
            fullname=data["fullname"],
            email=data["email"],
            dob=data["dob"],
            experience=data["experience"],
            gender=data["gender"],
            subscribe=data["subscribe"].lower() == "true"
        )

    with allure.step("Submit form"):
        form_page.submit()