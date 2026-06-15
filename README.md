# TDD-ReCap

A robust Python Flask web application designed with a strict Test-Driven Development (TDD) approach. The application manages "Duties" using the Peewee ORM backed by a PostgreSQL database and features an automated CI/CD pipeline deploying straight to AWS ECS.

## Tech Stack

* **Backend Framework:** Flask
* **Database ORM:** Peewee
* **Database Engine:** PostgreSQL
* **Testing Suite:** Pytest (Unit & Integration)
* **Browser Automation (E2E):** Playwright
* **Deployment & Infrastructure:** GitHub Actions, Docker, AWS ECR, AWS ECS

---

## Local Development Setup

### 1. Prerequisites
Ensure you have Python 3.12+ and PostgreSQL installed on your local machine.

### 2. Installation
Clone the repository, set up a virtual environment, and install the project dependencies:

```bash
# Clone the repository
git clone [https://github.com/liam-blackburn/TDD-ReCap.git](https://github.com/liam-blackburn/TDD-ReCap.git)
cd TDD-ReCap

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install Playwright headless browsers for E2E tests
playwright install --with-deps
```

### 2. Local Environment Configuration

Create a `.env` file in the root directory of the project folder to map your local database parameters:

```bash
DATABASE='your_database_name'
DATABASE_USER='your_database_username'
DATABASE_PASSWORD='your_database_password'
DATABASE_HOST='your_database_host_url'
```
## Database Schema Architecture

To prevent database table collisions across environments, the database utilises a dynamic schema-splitting design mapped out via the model configurations:

| Environment | PostgreSQL Schema | Target Table Name |
| :--- | :--- | :--- |
| **Production** | `coins` | `tdd_safari_duties` |
| **Testing** | `coins_test` | `tdd_safari_test_duties` |

## Running the Test Suite

The test suite features **18 automated tests** spanning unit, integration and E2E testing.

Given there are 4 unit tests, 9 integration tests and 5 E2E tests, we can calculate the percentage of those tests:

| Test Type | Count | Percentage  |
| :--- | :--- |:------------|
| **Integration Tests** | 9 | 50%         |
| **End-to-End (E2E) Tests** | 5 | ~28%        |
| **Unit Tests** | 4 | ~22%        |
| **Total** | **18** | **100.00%** |

This highlights that due to the apps heavy reliance on database interactions, integration tests surpass both E2E and unit tests.
### Running Backend Unit & Integration Tests
For standard backend tests, you do not need to boot a background server. The `tests/conftest.py` setup automatically flags the environment and isolates everything cleanly inside the `coins_test` schema:

```bash
pytest
```

### Running End-to-End (E2E) Playwright Tests

Because E2E browser automated tests require a live system interface to interact with, you must execute them across **two separate terminal windows** to keep test data clear of your production records:

* **Terminal 1 (Start Local Test Server):**
    ```bash
    TESTING=True flask run
    ```
* **Terminal 2 (Execute the Test Suite):**
    ```bash
    pytest
    ```
### Coverage Reporting

To get a full coverage report, you must use the `TESTING=True` prefix so E2E tests are captured. Therefore:

* **Terminal 1 (Start Local Test Server):**
    ```bash
    TESTING=True flask run
    ```
* **Terminal 2 (Execute coverage capture and coverage report):**
    ```bash
    coverage run -m pytest -s tests
    coverage report
    ```
**Currently, coverage is sitting at a very healthy 94%**