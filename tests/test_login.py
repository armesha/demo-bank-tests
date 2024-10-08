import pytest
from selenium.webdriver.common.by import By

BASE_URL = "http://127.0.0.1:5000/"

@pytest.mark.parametrize("username,password,should_pass", [
    ("armen_davtian", "password123", True),
    ("petr_pavel", "asdf12345", True),
    ("invalid_user", "password", False),
    ("john_doe", "wrongpassword", False),
])
def test_login(driver, username, password, should_pass):
    driver.get(BASE_URL + "login")
    
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()

    if should_pass:
        assert "Dashboard" in driver.title or "Welcome" in driver.page_source
    else:
        assert "Invalid username or password." in driver.page_source
