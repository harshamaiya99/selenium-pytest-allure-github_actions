import pytest  # pytest framework for fixtures and test running
import subprocess  # For starting a simple HTTP server as a subprocess
import time  # For sleeping to allow the server to start
import os  # OS utilities for path handling
import allure  # Allure reporting for attachments
from selenium import webdriver  # Selenium WebDriver API
from selenium.webdriver.chrome.options import Options  # Chrome options for headless mode

# Plan 2: Centralized Configuration
@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8000"  # Base URL used by tests to reach the local server


@pytest.fixture(scope="session", autouse=True)
def start_server():
    process = subprocess.Popen(
        ["python", "-m", "http.server", "8000"],  # Start a simple HTTP server on port 8000
        cwd=os.path.join(os.getcwd(), "app"),  # Serve files from the app directory
        stdout = subprocess.DEVNULL,  # Suppress server stdout
        stderr = subprocess.DEVNULL  # Suppress server stderr
    )
    time.sleep(2) # Kept original logic as requested (wait briefly for server to start)
    yield
    process.terminate()  # Terminate server after the test session ends


@pytest.fixture
def driver():
    options = Options()  # Create Chrome options
    options.add_argument("--headless")  # Run Chrome in headless mode for CI
    options.add_argument("--no-sandbox")  # Disable sandbox for containerized environments
    options.add_argument("--disable-dev-shm-usage")  # Workaround for limited /dev/shm in containers
    options.add_argument("--disable-gpu")  # Disable GPU usage
    options.add_argument("--window-size=1920,1080")  # Set a consistent window size

    driver = webdriver.Chrome(options=options)  # Instantiate Chrome WebDriver with options
    driver.maximize_window()  # Maximize browser window for consistent behavior
    yield driver
    driver.quit()  # Quit the browser after the test


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()  # Get the test report

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")  # Retrieve driver fixture from the test if present
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),  # Attach a screenshot of the browser on failure
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )