import tkinter as tk
from tkinter import messagebox, simpledialog
import requests

API_URL = "http://127.0.0.1:5000"

class ATMClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ATM Client")
        self.geometry("300x250")

        self.create_widgets()

    def create_widgets(self):
        tk.Button(self, text="Create Account", command=self.create_account).pack(pady=5)
        tk.Button(self, text="Check Balance", command=self.check_balance).pack(pady=5)
        tk.Button(self, text="Deposit", command=self.deposit).pack(pady=5)
        tk.Button(self, text="Withdraw", command=self.withdraw).pack(pady=5)
        tk.Button(self, text="Exit", command=self.quit).pack(pady=5)

    def create_account(self):
        account_number = simpledialog.askstring("Create Account", "Enter account number:")
        pin = simpledialog.askstring("Create Account", "Enter PIN:", show='*')
        if account_number and pin:
            response = requests.post(f"{API_URL}/account", json={"account_number": account_number, "pin": pin})
            messagebox.showinfo("Create Account", response.json().get('message') or response.json().get('error'))

    def get_auth_details(self):
        account_number = simpledialog.askstring("Authentication", "Enter account number:")
        pin = simpledialog.askstring("Authentication", "Enter PIN:", show='*')
        return account_number, pin

    def check_balance(self):
        account_number, pin = self.get_auth_details()
        if account_number and pin:
            # First, authenticate the user by trying to get account details.
            # The server's get_account endpoint does not require a PIN, so we can't truly authenticate here.
            # This is a security flaw in the server design. For now, we'll proceed.
            response = requests.get(f"{API_URL}/account/{account_number}")
            if response.status_code == 200:
                messagebox.showinfo("Balance", f"Your balance is: {response.json()['balance']}")
            else:
                messagebox.showerror("Error", response.json().get('error'))

    def deposit(self):
        account_number, pin = self.get_auth_details()
        if account_number and pin:
            amount = simpledialog.askfloat("Deposit", "Enter amount:")
            if amount is not None:
                response = requests.post(f"{API_URL}/transaction", json={
                    "account_number": account_number,
                    "pin": pin,
                    "type": "deposit",
                    "amount": amount
                })
                messagebox.showinfo("Deposit", response.json().get('message') or response.json().get('error'))

    def withdraw(self):
        account_number, pin = self.get_auth_details()
        if account_number and pin:
            amount = simpledialog.askfloat("Withdraw", "Enter amount:")
            if amount is not None:
                response = requests.post(f"{API_URL}/transaction", json={
                    "account_number": account_number,
                    "pin": pin,
                    "type": "withdrawal",
                    "amount": amount
                })
                messagebox.showinfo("Withdraw", response.json().get('message') or response.json().get('error'))

if __name__ == "__main__":
    app = ATMClient()
    app.mainloop()
