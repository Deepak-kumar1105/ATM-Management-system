import tkinter as tk
from tkinter import messagebox, ttk
import datetime

initial_deposit = 5000
accounts = { "12345": {     "pin": "1234","balance": initial_deposit,"transactions": [f"Initial deposit: +₹{initial_deposit:.2f} on {datetime.datetime.now()}"]}}

class ATM:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x300")
        self.root.title("ATM Management")
        self.main_window()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_window(self):
        self.clear()
        tk.Label(self.root, text="ATM management").pack(pady=30)
        tk.Label(self.root, text="12345(pin:134)", font="Arial").pack()
        tk.Button(self.root, text="Login", command=self.login, bg="lightblue").pack(pady=20)
        tk.Button(self.root, text="Exit", command=self.root.quit, bg="lightblue").pack(pady=20)

    def login(self):
        self.clear()
        tk.Label(self.root, text="Login", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Account Number:").pack()
        acc_entry = tk.Entry(self.root)
        acc_entry.pack(pady=5)
        tk.Label(self.root, text="PIN:").pack()
        pin_entry = tk.Entry(self.root, show="*")
        pin_entry.pack(pady=5)

        def submit():
            account_number = acc_entry.get()
            pin = pin_entry.get()
            if account_number in accounts and accounts[account_number]["pin"] == pin:
                self.current_account = account_number
                messagebox.showinfo("Success", "Login successful!")
                self.atm_menu()
            else:
                messagebox.showerror("Error", "Invalid account number or PIN!")

        tk.Button(self.root, text="Submit", command=submit, width=15).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_window, width=15).pack(pady=5)

    def atm_menu(self):
        self.clear()
        tk.Label(self.root, text="ATM Menu", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="Check Balance", command=self.check_balance, width=20).pack(pady=10)
        tk.Button(self.root, text="Deposit", command=self.deposit_window, width=20).pack(pady=10)
        tk.Button(self.root, text="Withdraw", command=self.withdraw_window, width=20).pack(pady=10)
        tk.Button(self.root, text="Transaction History", command=self.transaction_history_window, width=20).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout, width=20).pack(pady=10)

    def check_balance(self):
        balance = accounts[self.current_account]["balance"]
        messagebox.showinfo("Balance", f"Current balance: ₹{balance:.2f}")

    def deposit_window(self):
        self.clear()
        tk.Label(self.root, text="Deposit", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Amount:").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack(pady=5)

        def submit():
            try:
                amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number!")
                return
            if amount <= 0:
                messagebox.showerror("Error", "Deposit amount must be positive!")
                return

            accounts[self.current_account]["balance"] += amount
            accounts[self.current_account]["transactions"].append(
                f"Deposit: +₹{amount:.2f} on {datetime.datetime.now()}"
            )
            messagebox.showinfo("Success", f"Deposited ₹{amount:.2f} successfully!")
            self.atm_menu()

        tk.Button(self.root, text="Submit", command=submit, width=15).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.atm_menu, width=15).pack(pady=5)

    def withdraw_window(self):
        self.clear()
        tk.Label(self.root, text="Withdraw", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Amount:").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack(pady=5)

        def submit():
            try:
                amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Amount must be a number!")
                return
            if amount <= 0:
                messagebox.showerror("Error", "Withdrawal amount must be positive!")
                return
            if amount > accounts[self.current_account]["balance"]:
                messagebox.showerror("Error", "Insufficient funds!")
                return

            accounts[self.current_account]["balance"] -= amount
            accounts[self.current_account]["transactions"].append(
                f"Withdrawal: -₹{amount:.2f} on {datetime.datetime.now()}"
            )
            messagebox.showinfo("Success", f"Withdrawn ₹{amount:.2f} successfully!")
            self.atm_menu()

        tk.Button(self.root, text="Submit", command=submit, width=15).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.atm_menu, width=15).pack(pady=5)

    def transaction_history_window(self):
        self.clear()
        tk.Label(self.root, text="Transaction History", font=("Arial", 14)).pack(pady=10)
        text_area = tk.Text(self.root, height=10, width=50)
        text_area.pack(pady=5)
        transactions = accounts[self.current_account]["transactions"]
        if not transactions:
            text_area.insert(tk.END, "No transactions found.")
        else:
            for transaction in transactions:
                text_area.insert(tk.END, transaction + "\n")
        text_area.config(state="disabled")
        tk.Button(self.root, text="Back", command=self.atm_menu, width=15).pack(pady=10)

    def logout(self):
        self.current_account = None
        messagebox.showinfo("Success", "Logged out successfully!")
        self.main_window()
root = tk.Tk()
app = ATM(root)
root.mainloop()
