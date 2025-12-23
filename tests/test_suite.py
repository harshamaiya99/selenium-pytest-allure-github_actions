import csv
import allure
import pytest
from selenium.webdriver.common.by import By

BASE_URL = "http://localhost:8000"

def load_test_data():
    with open("tests/test_data.csv") as f:
        reader = csv.DictReader(f)
        return list(reader)

@allure.feature("E2E Web Testing")
@allure.story("Login and Form Submission")
@pytest.mark.parametrize("data", load_test_data())
def test_login_and_form(driver, data):

    with allure.step("Open login page"):
        driver.get(f"{BASE_URL}/index.html")

    with allure.step("Perform login"):
        driver.find_element(By.ID, "username").send_keys(data["username"])
        driver.find_element(By.ID, "password").send_keys(data["password"])
        driver.find_element(By.ID, "loginBtn").click()

    with allure.step("Fill user form"):
        driver.find_element(By.ID, "fullname").send_keys(data["fullname"])
        driver.find_element(By.ID, "email").send_keys(data["email"])
        driver.find_element(By.ID, "gender").send_keys(data["gender"])

        if data["subscribe"].lower() == "true":
            driver.find_element(By.ID, "subscribe").click()

    with allure.step("Submit form"):
        driver.find_element(By.ID, "submitBtn").click()
