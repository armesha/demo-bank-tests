import pytest
from selenium.webdriver.common.by import By
import sqlite3

BASE_URL = "http://127.0.0.1:5000/"

def get_balance_from_db(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE username = ?', (username,))
    balance = cursor.fetchone()[0]
    conn.close()
    return balance

def login(driver, username, password):
    driver.get(BASE_URL + "login")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()

def test_balance(driver):
    username = "armen_davtian"
    password = "password123"
    login(driver, username, password)
    
    # Get balance from UI
    balance_text = driver.find_element(By.XPATH, "//p[contains(text(), 'Current Balance')]").text
    balance_ui = float(balance_text.split('$')[-1])
    
    # Get balance from DB
    balance_db = get_balance_from_db(username)
    
    assert balance_ui == balance_db, "Balance mismatch between UI and Database."
