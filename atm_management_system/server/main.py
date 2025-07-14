from flask import Flask, jsonify, request
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import connect_db

app = Flask(__name__)

@app.route('/account', methods=['POST'])
def create_account():
    """Creates a new account."""
    data = request.get_json()
    account_number = data.get('account_number')
    pin = data.get('pin')
    balance = data.get('balance', 0)

    if not account_number or not pin:
        return jsonify({'error': 'Account number and PIN are required'}), 400

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO accounts (account_number, pin, balance) VALUES (?, ?, ?)",
            (account_number, pin, balance)
        )
        conn.commit()
        return jsonify({'message': 'Account created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/account/<account_number>', methods=['GET'])
def get_account(account_number):
    """Retrieves account information."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,))
    account = cursor.fetchone()
    conn.close()

    if account:
        return jsonify({
            'id': account[0],
            'account_number': account[1],
            'balance': account[3]
        })
    else:
        return jsonify({'error': 'Account not found'}), 404

@app.route('/transaction', methods=['POST'])
def create_transaction():
    """Creates a new transaction."""
    data = request.get_json()
    account_number = data.get('account_number')
    pin = data.get('pin')
    transaction_type = data.get('type')
    amount = data.get('amount')

    if not all([account_number, pin, transaction_type, amount]):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE account_number = ? AND pin = ?", (account_number, pin))
    account = cursor.fetchone()

    if not account:
        conn.close()
        return jsonify({'error': 'Invalid account number or PIN'}), 401

    account_id = account[0]
    balance = account[3]

    if transaction_type == 'withdrawal':
        if balance < amount:
            conn.close()
            return jsonify({'error': 'Insufficient funds'}), 400
        new_balance = balance - amount
    elif transaction_type == 'deposit':
        new_balance = balance + amount
    else:
        conn.close()
        return jsonify({'error': 'Invalid transaction type'}), 400

    try:
        cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_balance, account_id))
        cursor.execute(
            "INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)",
            (account_id, transaction_type, amount)
        )
        conn.commit()
        return jsonify({'message': 'Transaction successful'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
