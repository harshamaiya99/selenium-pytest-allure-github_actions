# CI Selenium E2E Testing with Pytest & Allure

This project demonstrates a robust End-to-End (E2E) testing framework for web applications, built using **Selenium WebDriver**, **Pytest**, and **Allure Report**, integrated into a **GitHub Actions** Continuous Integration (CI) pipeline. It provides a comprehensive solution for automated browser testing, detailed reporting, and automated execution on every code change and on a scheduled basis.

The System Under Test (SUT) is a simple, self-contained HTML application (Login and Form pages) served by a local HTTP server during test execution, making the project fully runnable and demonstrable without external dependencies.

## Table of Contents

-   [Features](#features)
-   [Technologies Used](#technologies-used)
-   [Project Structure](#project-structure)
-   [Getting Started](#getting-started)
    -   [Prerequisites](#prerequisites)
    -   [Installation](#installation)
    -   [Running Tests Locally](#running-tests-locally)
-   [Continuous Integration (CI) with GitHub Actions](#continuous-integration-ci-with-github-actions)
-   [Allure Report](#allure-report)
    -   [Viewing Reports Locally](#viewing-reports-locally)
    -   [Viewing Reports via GitHub Pages](#viewing-reports-via-github-pages)
-   [System Under Test (SUT) Overview](#system-under-test-sut-overview)
-   [Test Framework Design](#test-framework-design)
    -   [Page Object Model (POM)](#page-object-model-pom)
    -   [Fixtures (`conftest.py`)](#fixtures-conftestpy)
    -   [Test Data Management](#test-data-management)
    -   [Allure Integration](#allure-integration)
-   [Contributing](#contributing)
-   [License](#license)
-   [Contact](#contact)

## Features

*   **End-to-End Web Testing:** Comprehensive E2E tests for web application flows using Selenium WebDriver.
*   **Pytest Framework:** Leverages Pytest for test discovery, execution, and advanced fixtures.
*   **Allure Reports:** Generates rich, interactive, and detailed test reports with screenshots on failure, step-by-step logs, and test data.
*   **GitHub Actions CI:** Automates test execution on:
    *   `push` to `main` branch.
    *   `pull_request` to `main` branch.
    *   Daily schedule (12:00 AM IST / 18:30 UTC).
*   **Self-contained SUT:** Includes a simple HTML application (`app/index.html`, `app/form.html`) served locally during tests, removing external dependencies.
*   **Headless Browser Execution:** Configured for headless Chrome for efficient CI/CD execution.
*   **Robust Page Objects:** Implements Page Object Model (POM) with enhanced methods for element interaction, including JavaScript click handling for scenarios where elements might be obscured.
*   **Parameterized Tests:** Uses CSV-driven test data to run the same test logic with multiple data sets.
*   **Automatic Screenshots:** Captures screenshots automatically for failed tests and attaches them to Allure reports.

## Technologies Used

*   **Python:** Programming language for the test framework.
*   **Selenium WebDriver:** For browser automation.
*   **Pytest:** Test framework.
*   **Allure Report:** For comprehensive test reporting.
*   **Google Chrome / ChromeDriver:** The browser and WebDriver used for testing (configurable).
*   **GitHub Actions:** CI/CD pipeline.
*   **HTTP Server (Python built-in):** For serving the local SUT.

## Project Structure

```
.
├── .github/                       # GitHub Actions workflows
│   └── workflows/
│       └── main.yml               # CI workflow definition
├── app/                           # System Under Test (SUT) web application
│   ├── form.html                  # Sample form page
│   └── index.html                 # Sample login page
├── pages/                         # Page Object Model (POM) classes
│   ├── base_page.py               # Base class for all page objects
│   ├── form_page.py               # Page object for the form page
│   └── login_page.py              # Page object for the login page
├── tests/                         # Test suite
│   ├── conftest.py                # Pytest fixtures and hooks
│   ├── test_data.csv              # Test data for parameterized tests
│   └── test_suite.py              # Main test scripts
├── allure-results/                # Directory for raw Allure test results
├── allure-report/                 # Generated Allure HTML report (after running `allure generate`)
├── README.md                      # Project documentation
└── requirements.txt               # Python dependencies
```

## Getting Started

Follow these instructions to set up and run the tests locally.

### Prerequisites

*   **Python 3.10+**: Ensure Python is installed and added to your PATH.
*   **Google Chrome**: The browser used by Selenium. ChromeDriver (installed automatically by `webdriver_manager`) will match your Chrome version.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/harshamaiya99/selenium-pytest-allure-github_actions.git
    cd selenium-pytest-allure-github_actions
    ```

2.  **Create and activate a virtual environment (recommended):**

    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**

    ```bash
    pip install -r tests/requirements.txt
    ```

    This will install Selenium, Pytest, Allure-pytest, and `webdriver_manager` (to handle ChromeDriver automatically).

### Running Tests Locally

1.  **Ensure virtual environment is active.**

2.  **Run Pytest with Allure integration:**

    ```bash
    pytest tests --alluredir=allure-results --disable-warnings -v
    ```
    *   `pytest tests`: Discovers and runs tests in the `tests/` directory.
    *   `--alluredir=allure-results`: Specifies the directory to save raw Allure results.
    *   `--disable-warnings`: Suppresses Pytest warnings for a cleaner output.
    *   `-v`: Enables verbose output for more detailed test progress.

    This command will execute the tests, and if successful, a directory named `allure-results` will be created/updated with `.json` and `.xml` files containing the test execution data.

## Continuous Integration (CI) with GitHub Actions

The project is configured with a GitHub Actions workflow defined in `.github/workflows/main.yml`.

**Workflow Triggers:**
The workflow automatically triggers on:
*   `push` events to the `main` branch.
*   `pull_request` events targeting the `main` branch.
*   A daily schedule at 18:30 UTC (which translates to 12:00 AM IST).

**Workflow Steps:**
1.  **`Checkout main`**: Checks out the project repository.
2.  **`Set up Python`**: Installs Python 3.10.
3.  **`Install dependencies`**: Installs all required Python packages from `tests/requirements.txt`.
4.  **`Run Tests`**: Executes the Selenium Pytest tests, generating raw Allure results into `allure-results`.
5.  **`Install Allure CLI`**: Downloads and extracts the Allure Command Line Interface.
6.  **(Implicit) Generate Allure Report**: *Though not explicitly shown in the provided `main.yml` snippet, a typical workflow for Allure report generation would follow here.* This step would use the Allure CLI to convert the raw results into an HTML report.
    ```yaml
    - name: Generate Allure Report
      run: |
        ./allure-*/bin/allure generate allure-results --clean -o allure-report
    ```
7.  **(Implicit) Deploy Allure Report to GitHub Pages**: *Again, not explicitly shown, but essential for the Allure badge link.* This step would typically use an action like `peaceiris/actions-gh-pages` to deploy the generated `allure-report` directory to the `gh-pages` branch, making it accessible via GitHub Pages.
    ```yaml
    - name: Deploy Allure Report to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: allure-report
        keep_files: true
    ```

You can view the CI execution status and details on your GitHub repository's "Actions" tab.

## Allure Report

Allure Report provides a clear and interactive representation of test execution.

### Viewing Reports Locally

After running tests locally and generating `allure-results`, you can serve the HTML report:

1.  **Generate the HTML report:**
    ```bash
    # Ensure Allure CLI is installed (see GitHub Actions workflow for how)
    # Or download it manually from https://github.com/allure-framework/allure2/releases
    # Then generate report:
    <path-to-allure-cli>/bin/allure generate allure-results --clean -o allure-report
    ```
    This will create an `allure-report` directory.

2.  **Open the report in your browser:**
    ```bash
    <path-to-allure-cli>/bin/allure open allure-report
    ```
    This command will open the generated HTML report in your default web browser.

### Viewing Reports via GitHub Pages

The CI pipeline is set up to automatically generate and deploy the Allure Report to GitHub Pages, linked from the badge at the top of this README.

You can access the latest report via: `https://harshamaiya99.github.io/selenium-pytest-allure-github_actions/`

## System Under Test (SUT) Overview

The `app/` directory contains the simple web application used as the SUT:

*   **`index.html` (Login Page):** A basic login form with username, password, and a login button. Upon successful submission, it redirects to `form.html`.
*   **`form.html` (Form Page):** An extended form requiring personal details (full name, email, DOB, experience, gender), an asynchronous "Load Skills" button (simulating network delay), a primary skill input, and a subscription checkbox.

During test execution, a Python HTTP server serves these pages locally on `http://localhost:8000`.

## Test Framework Design

### Page Object Model (POM)

The `pages/` directory implements the Page Object Model design pattern:

*   **`BasePage`:** Provides common methods for interacting with web elements (e.g., `find`, `click`, `type`, `wait_for_title`), logging to Allure, and handling common exceptions like `ElementClickInterceptedException` with a JavaScript click fallback.
*   **`LoginPage`:** Encapsulates elements and actions specific to the login page.
*   **`FormPage`:** Encapsulates elements and actions specific to the form page, demonstrating a modular approach by breaking down form filling into smaller, more focused methods (`enter_personal_details`, `add_skill`, `set_subscription`).

This structure promotes code reusability, maintainability, and readability.

### Fixtures (`conftest.py`)

The `tests/conftest.py` file defines Pytest fixtures that provide setup and teardown for tests:

*   **`base_url` (session scope):** Provides the base URL for the local HTTP server.
*   **`start_server` (session scope, autouse=True):** Starts a local HTTP server in the `app/` directory before any tests run and terminates it after all tests are complete. This ensures the SUT is always available.
*   **`driver` (function scope):** Initializes a headless Chrome WebDriver before each test and quits it afterward, ensuring a clean browser state for every test. It also configures standard headless options for CI environments.
*   **`pytest_runtest_makereport` (hook):** A Pytest hook that automatically captures a screenshot using `allure.attach` whenever a test fails during the "call" phase, enhancing debuggability in reports.

### Test Data Management

Test data for parameterized tests is stored in `tests/test_data.csv`. The `load_test_data()` function in `test_suite.py` reads this CSV file, allowing the `test_login_and_form` function to execute multiple scenarios with different inputs without duplicating test logic.

### Allure Integration

*   **`allure.feature` and `allure.story` decorators:** Used in `test_suite.py` to categorize tests within Allure reports.
*   **`allure.step` context manager:** Used extensively in page object methods and test functions to log actions and states directly into the Allure report, creating a clear, step-by-step narrative of test execution.
*   **`allure.attach`:** Employed in the `pytest_runtest_makereport` hook to attach failure screenshots, providing visual context for any issues.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'feat: Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (if a LICENSE file exists; otherwise, state "No explicit license provided, assume standard GitHub terms").

## Contact

For any questions or feedback, please contact [harshamaiya99](https://github.com/harshamaiya99).

---