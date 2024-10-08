import pytest
from selenium.webdriver.common.by import By
import sqlite3

BASE_URL = "http://127.0.0.1:5000/"

def login(driver, username, password):
    driver.get(BASE_URL + "login")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[text()='Login']").click()

def test_transaction_history(driver):
    username = "armen_davtian"
    password = "password123"

    login(driver, username, password)
    driver.find_element(By.LINK_TEXT, "View Transaction History").click()

    # Fetch transactions from UI
    table_rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
    ui_transactions = []
    for row in table_rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        txn = {
            "id": cols[0].text,
            "amount": float(cols[1].text),
            "type": cols[2].text,
            "timestamp": cols[3].text
        }
        ui_transactions.append(txn)

    # Fetch transactions from DB
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, amount, type, timestamp FROM transactions WHERE user_id = (SELECT id FROM users WHERE username = ?) ORDER BY timestamp DESC', (username,))
    db_transactions = cursor.fetchall()
    conn.close()

    db_transactions = [{
        "id": str(txn[0]),
        "amount": txn[1],
        "type": txn[2],
        "timestamp": txn[3]
    } for txn in db_transactions]

    assert len(ui_transactions) == len(db_transactions), "Number of transactions mismatch."

    for ui_txn, db_txn in zip(ui_transactions, db_transactions):
        assert ui_txn == db_txn, f"Transaction mismatch: UI {ui_txn} != DB {db_txn}"
