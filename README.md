# CI Selenium E2E Testing with Pytest & Allure

## Features
- Simple HTML SUT (Login + Form)
- Selenium WebDriver (Headless Chrome)
- Pytest with CSV-driven tests
- Local HTTP server (self-contained)
- Allure HTML reporting
- GitHub Actions CI
- Allure report uploaded as artifact

## Run Locally
```bash
pip install -r tests/requirements.txt
pytest tests --alluredir=allure-results
allure serve allure-results
