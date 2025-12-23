import pytest
import subprocess
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="session", autouse=True)
def start_server():
    process = subprocess.Popen(
        ["python", "-m", "http.server", "8000"],
        cwd=os.path.join(os.getcwd(), "app")
    )
    time.sleep(2)
    yield
    process.terminate()

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
