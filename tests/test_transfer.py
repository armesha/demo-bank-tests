import pytest
from selenium.webdriver.common.by import By
import sqlite3

BASE_URL = "http://127.0.0.1:5000/"

def get_balance(username):
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

def test_fund_transfer_success(driver):
    sender = "armen_davtian"
    sender_pass = "password123"
    receiver = "petr_pavel"
    transfer_amount = 100.0

    # Get initial balances
    sender_initial = get_balance(sender)
    receiver_initial = get_balance(receiver)

    login(driver, sender, sender_pass)
    driver.find_element(By.LINK_TEXT, "Transfer Funds").click()
    driver.find_element(By.NAME, "target_username").send_keys(receiver)
    driver.find_element(By.NAME, "amount").send_keys(str(transfer_amount))
    driver.find_element(By.XPATH, "//button[text()='Transfer']").click()

    # Verify success message
    assert f"Transferred {transfer_amount}" in driver.page_source

    # Get updated balances
    sender_updated = get_balance(sender)
    receiver_updated = get_balance(receiver)

    assert sender_updated == sender_initial - transfer_amount
    assert receiver_updated == receiver_initial + transfer_amount

def test_fund_transfer_insufficient_funds(driver):
    sender = "armen_davtian"
    sender_pass = "password123"
    receiver = "petr_pavel"
    transfer_amount = 100000.0  # Assuming this exceeds the sender's balance

    login(driver, sender, sender_pass)
    driver.find_element(By.LINK_TEXT, "Transfer Funds").click()
    driver.find_element(By.NAME, "target_username").send_keys(receiver)
    driver.find_element(By.NAME, "amount").send_keys(str(transfer_amount))
    driver.find_element(By.XPATH, "//button[text()='Transfer']").click()

    # Verify error message
    assert "Insufficient funds." in driver.page_source
