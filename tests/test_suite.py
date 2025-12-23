import csv
import pytest
import allure
from pages.login_page import LoginPage
from pages.form_page import FormPage

BASE_URL = "http://localhost:8000"


def load_test_data():
    with open("tests/test_data.csv") as f:
        return list(csv.DictReader(f))


@allure.feature("E2E Web Testing")
@allure.story("Login and Form Submission")
@pytest.mark.parametrize("data", load_test_data())
def test_login_and_form(driver, data):

    login_page = LoginPage(driver)
    form_page = FormPage(driver)

    with allure.step("Open login page"):
        login_page.open(BASE_URL)

    with allure.step("Login"):
        login_page.login(data["username"], data["password"])

    with allure.step("Wait for form page"):
        form_page.wait_for_page()
        assert "Form" in driver.title

    with allure.step("Fill form"):
        form_page.fill_form(
            fullname=data["fullname"],
            email=data["email"],
            gender=data["gender"],
            subscribe=data["subscribe"].lower() == "true"
        )

    with allure.step("Submit form"):
        form_page.submit()
