import pytest
import subprocess
import time
import os
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Plan 2: Centralized Configuration
@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8000"

@pytest.fixture(scope="session", autouse=True)
def start_server():
    process = subprocess.Popen(
        ["python", "-m", "http.server", "8000"],
        cwd=os.path.join(os.getcwd(), "app"),
        stdout = subprocess.DEVNULL,
        stderr = subprocess.DEVNULL
    )
    time.sleep(2) # Kept original logic as requested
    yield
    process.terminate()

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )