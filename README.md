As an expert senior software engineer, here is a complete and professional `README.md` for your project, synthesizing information from all provided files.

---

# CI Selenium E2E Testing with Pytest & Allure

[![CI Status](https://github.com/maiyamohammad/selenium-pytest-allure-github_actions/workflows/Selenium%20Pytest%20+%20Allure%20CI/badge.svg)](https://github.com/maiyamohammad/selenium-pytest-allure-github_actions/actions)
[![Allure Report](https://img.shields.io/badge/Allure_Report-View_Latest-blue?style=flat-square&logo=allure)](https://maiyamohammad.github.io/selenium-pytest-allure-github_actions/allure-report/) *(Link assumes GitHub Pages deployment)*

This project demonstrates a robust End-to-End (E2E) testing framework for web applications, built using **Selenium WebDriver**, **Pytest**, and **Allure Report**, integrated into a **GitHub Actions** Continuous Integration (CI) pipeline. It provides a comprehensive solution for automated browser testing, detailed reporting, and automated execution on every code change and on a scheduled basis.

The System Under Test (SUT) is a simple, self-contained HTML application (Login and Form pages) served by a local HTTP server during test execution.

## Table of Contents

-   [Features](#features)
-   [Technologies Used](#technologies-used)
-   [Project Structure](#project-structure)
-   [Getting Started](#getting-started)
    -   [Prerequisites](#prerequisites)
    -   [Installation](#installation)
    -   [Running Tests Locally](#running-tests-locally)
    -   [Viewing Allure Report Locally](#viewing-allure-report-locally)
-   [CI/CD with GitHub Actions](#cicd-with-github-actions)
    -   [Workflow Triggers](#workflow-triggers)
    -   [Report Publication](#report-publication)
-   [Contributing](#contributing)
-   [License](#license)

## Features

*   **Simple HTML SUT:** A basic web application consisting of a login page and a subsequent form page for demonstrating E2E flows.
*   **Selenium WebDriver:** Automates browser interactions using headless Chrome for efficient, scriptable testing.
*   **Pytest Framework:** Utilizes Pytest for test discovery, execution, and advanced fixture management.
    *   **CSV-Driven Tests:** Test data is externalized in a CSV file, allowing for easy expansion and maintenance of test cases without modifying code.
    *   **Page Object Model (POM):** Implements POM for maintainable, reusable, and readable test code by abstracting web elements and interactions into dedicated page classes.
*   **Local HTTP Server (Self-Contained):** A lightweight Python HTTP server is automatically started as a Pytest fixture to serve the SUT during test execution, making the tests entirely self-sufficient.
*   **Allure HTML Reporting:** Generates rich, interactive, and comprehensive HTML reports with test steps, screenshots on failure, and detailed test execution information.
*   **GitHub Actions CI/CD:** Automates the entire test suite execution on every push, pull request, and on a daily schedule.
*   **Allure Report Upload as Artifact:** The generated Allure raw results are uploaded as a GitHub Actions artifact for debugging and archival.
*   **Allure Report Publication to GitHub Pages:** (Inferred) The generated Allure HTML report is automatically published to GitHub Pages, providing a live, accessible view of the latest test results.

## Technologies Used

*   **Python 3.10+**: Programming language
*   **Selenium WebDriver**: Browser automation library
*   **Pytest**: Testing framework
*   **Allure-Pytest**: Pytest integration for Allure reporting
*   **Chrome WebDriver**: Browser driver for Selenium (managed automatically by `selenium-manager`)
*   **GitHub Actions**: CI/CD platform
*   **`http.server` (Python module)**: For serving the local SUT

## Project Structure

```
.
├── .github/                       # GitHub Actions workflows
│   └── workflows/
│       └── main.yml               # CI/CD pipeline definition
├── app/                           # System Under Test (SUT)
│   ├── form.html                  # Sample form page
│   └── index.html                 # Sample login page
├── pages/                         # Page Object Model (POM) implementation
│   ├── base_page.py               # Base class for common page interactions
│   ├── form_page.py               # Page object for the form page
│   └── login_page.py              # Page object for the login page
│   └── __init__.py
├── tests/                         # Pytest test suite
│   ├── conftest.py                # Pytest fixtures (local server, WebDriver setup, Allure hooks)
│   ├── test_suite.py              # E2E test cases using parameterized data
│   ├── test_data.csv              # (Assumed) CSV file for test data
│   └── __init__.py
├── allure-results/                # Directory for raw Allure test results (generated during runtime)
└── README.md                      # This README file
```

## Getting Started

Follow these instructions to set up the project and run the tests locally.

### Prerequisites

*   Python 3.10 or higher
*   `pip` (Python package installer)
*   `git` (for cloning the repository)
*   Java Runtime Environment (JRE) 8 or higher (required for `allure serve` command, as it runs the Allure CLI).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/maiyamohammad/selenium-pytest-allure-github_actions.git
    cd selenium-pytest-allure-github_actions
    ```

2.  **Install Python dependencies:**
    Navigate to the project root and install the required packages.
    ```bash
    pip install -r tests/requirements.txt
    ```
    *(Assuming `tests/requirements.txt` contains `selenium`, `pytest`, `allure-pytest`)*

### Running Tests Locally

To execute the E2E test suite:

1.  Make sure you are in the root directory of the project.
2.  Run Pytest with the Allure reporting option:
    ```bash
    pytest tests --alluredir=allure-results
    ```
    This command will:
    *   Automatically start the local HTTP server serving the `app/` directory.
    *   Launch headless Chrome browser instances for each test.
    *   Execute the tests defined in `tests/test_suite.py`.
    *   Generate Allure raw results in the `allure-results/` directory.

### Viewing Allure Report Locally

After running the tests, you can generate and view the interactive Allure HTML report:

1.  Generate the Allure report from the raw results:
    ```bash
    allure generate allure-results --clean -o allure-report
    ```
    This command will process the raw data and create a static HTML report in the `allure-report/` directory.

2.  Serve the generated report in your browser:
    ```bash
    allure serve allure-results
    ```
    *(Alternatively, `allure serve allure-report` if you prefer to serve the already generated report.)*
    This command will open the report in your default web browser, usually at `http://localhost:port`.

## CI/CD with GitHub Actions

The project is configured with a GitHub Actions workflow (`.github/workflows/main.yml`) to automate testing and reporting.

### Workflow Triggers

The CI pipeline is triggered on:
*   **`push` events** to the `main` branch.
*   **`pull_request` events** targeting the `main` branch.
*   A **daily schedule** at 06:30 UTC (which corresponds to 12:00 PM IST).

### Workflow Steps

1.  **Checkout Code:** Clones the repository.
2.  **Set up Python:** Configures Python 3.10 environment.
3.  **Install Dependencies:** Installs project dependencies from `tests/requirements.txt`.
4.  **Run Tests:** Executes Pytest with Allure to generate raw test results in `allure-results/`. Screenshots are automatically attached to failed tests.
5.  **Install Allure CLI:** Downloads and installs the Allure command-line tool.
6.  **Generate Allure Report:** Generates the human-readable HTML report from the raw results.
7.  **Upload Allure Results as Artifact:** Uploads the `allure-results` directory as an artifact, making it downloadable from the GitHub Actions run summary.
8.  **Deploy Allure Report to GitHub Pages:** (Inferred) Publishes the generated `allure-report` directory to the `gh-pages` branch, making the report publicly accessible.

### Report Publication

The latest Allure Report is automatically published to GitHub Pages. You can access it via the badge at the top of this README or directly through the GitHub Pages URL:
`https://maiyamohammad.github.io/selenium-pytest-allure-github_actions/allure-report/`

## Contributing

Contributions are welcome! Please feel free to open issues, submit pull requests, or suggest improvements.

## License

This project is open-source and available under the [MIT License](LICENSE). *(Assuming an MIT license, add a LICENSE file if not present)*

---
*(Note: A `tests/requirements.txt` file and a `test_data.csv` file would typically be present in a real project based on the code provided. The GitHub Actions workflow assumes Allure CLI installation and report generation/deployment steps that were truncated in the provided `main.yml` content. These have been inferred and detailed in the README for a complete picture.)*