# Allure Report Workflow

This document explains the standard commands for running pytest and generating Allure reports.

## 1. `pytest tests --alluredir=allure-results`

**The Execution Phase**

This command actually runs your test code and collects the raw data needed for the report.

* **`pytest`**: The Python test runner.
* **`tests`**: The target directory (or file) where your test scripts are located.
* **`--alluredir=allure-results`**: This is a specific flag provided by the `allure-pytest` plugin. It tells pytest: *"Don't just print the results to the console; also save the raw test data (JSON and XML files) into a folder named `allure-results`."*

> **Note:** If the folder `allure-results` does not exist, this command will create it.

---

## 2. `allure serve allure-results`

**The Instant Preview (Local Development)**

This command is used when you are working locally and want to see the report immediately without saving permanent files.

* **`serve`**: This spins up a temporary local Java web server.
* **`allure-results`**: The source folder containing the raw data generated in Step 1.

**What happens:**

1.  Allure reads the raw data.
2.  It creates a temporary report in your system's temp folder.
3.  It **automatically opens your default web browser** to display the report.

**Use case:** Quick debugging on your local machine. The report disappears when you stop the server (`Ctrl+C`).

---

## 3. `allure generate allure-results --clean -o allure-report`

**The Static Report (CI/CD & Sharing)**

This command creates a permanent folder containing the HTML, CSS, and JS files of the report. This is what you would use in a CI/CD pipeline (like Jenkins or GitHub Actions) or if you want to zip the report and email it.

* **`generate`**: Tells Allure to compile the raw data into a static HTML website.
* **`allure-results`**: The source of the raw data.
* **`--clean`**: A crucial flag. It deletes the existing output directory (`allure-report`) before generating the new one. This prevents old test history from messing up the new report.
* **`-o allure-report`**: Specifies the **Output** directory. The final HTML `index.html` will be placed inside a folder named `allure-report`.

**Use case:** Creating a shareable artifact that does not require a running server to view (though you may need a web server to view it properly due to browser security settings on local files).

## 4. `allure generate allure-results --clean --single-file -o allure-report`

**Allure Single-File Report Generation**

This workflow generates a standalone HTML report file directly using the Allure CLI. This file contains all necessary CSS, JS, and data inline, making it easy to share via email or archive without needing a local web server.

* **`--clean`**: Deletes the output directory before generating a new report to prevent data overlap.

* **`--single-file`**: Key Flag. Tells Allure to embed all assets (CSS/JS/Images) into one index.html file.

* **`-o allure-report`**: Specifies the output directory.