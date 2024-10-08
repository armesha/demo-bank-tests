from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key in production

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash("Logged in successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.", "danger")
            return render_template('login.html')
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('dashboard.html', user=user)

@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    if request.method == 'POST':
        target_username = request.form['target_username']
        amount = float(request.form['amount'])

        conn = get_db_connection()
        sender = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        receiver = conn.execute('SELECT * FROM users WHERE username = ?', (target_username,)).fetchone()

        if not receiver:
            flash("Target user does not exist.", "danger")
            conn.close()
            return render_template('transfer.html')

        if sender['balance'] < amount:
            flash("Insufficient funds.", "danger")
            conn.close()
            return render_template('transfer.html')

        # Update balances
        new_sender_balance = sender['balance'] - amount
        new_receiver_balance = receiver['balance'] + amount

        conn.execute('UPDATE users SET balance = ? WHERE id = ?', (new_sender_balance, sender['id']))
        conn.execute('UPDATE users SET balance = ? WHERE id = ?', (new_receiver_balance, receiver['id']))

        # Record transactions
        conn.execute('INSERT INTO transactions (user_id, amount, type) VALUES (?, ?, ?)', (sender['id'], amount, 'debit'))
        conn.execute('INSERT INTO transactions (user_id, amount, type) VALUES (?, ?, ?)', (receiver['id'], amount, 'credit'))
        conn.commit()
        conn.close()

        flash(f"Transferred {amount} to {target_username}.", "success")
        return redirect(url_for('dashboard'))

    return render_template('transfer.html')

@app.route('/transactions')
@login_required
def transactions():
    conn = get_db_connection()
    transactions = conn.execute('SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC', (session['user_id'],)).fetchall()
    conn.close()
    return render_template('transactions.html', transactions=transactions)

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
