# Simple Banking Web Application with Automated Testing

## Overview

This project is a demonstration of testing skills for the ITRP - Junior Tester position at Česká spořitelna. It includes a simple banking web application built with Flask and automated UI tests using Selenium and Pytest.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/armesha/demo-bank-tests.git
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

```bash
python init_db.py
```

### 5. Run the Flask Application

```bash
python app.py
```

Access the application at `http://127.0.0.1:5000/`.

### 6. Automated Testing

Ensure the Flask application is running.

#### a. Run Tests with Pytest

```bash
pytest --html=reports/pytest_html_report.html --self-contained-html
```

View the test report at `reports/pytest_html_report.html`.

## Usage

### Sample Users

- **Username:** `armen_davtian` **Password:** `password123`

- **Username:** `peter_pavel` **Password:** `asdf12345`

### Features

- **Login:** Authenticate with username and password.
- **Dashboard:** View current balance and navigate to other features.
- **Transfer Funds:** Transfer money to another user.
- **Transaction History:** View past transactions.

## Technologies Used

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Automated Testing:** Selenium, Pytest, pytest-html