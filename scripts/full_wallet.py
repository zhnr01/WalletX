import os
import sys
import json
import time
import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread
from ape import accounts
from dotenv import load_dotenv


class WalletApp(tk.Tk):
    def __init__(self):
        super().__init__()

        load_dotenv()

        self.title("Cryptocurrency Wallet")
        self.geometry("350x250")
        self.resizable(False, False)

        self.username = os.environ["WALLET_USERNAME"]
        self.password = os.environ["WALLET_PASSWORD"]
        self.wallet_db_path = os.path.join(os.getcwd(), "wallet_db.json")

        # --- Balance display ---
        balance_frame = tk.Frame(self)
        balance_frame.pack(pady=10)

        tk.Label(balance_frame, text="My Balance:").pack(side=tk.LEFT, padx=5)
        self.balance_field = tk.Label(balance_frame, text="Loading...")
        self.balance_field.pack(side=tk.LEFT)

        # --- Amount input ---
        amount_frame = tk.Frame(self)
        amount_frame.pack(pady=10)

        self.amount_field = tk.Entry(amount_frame, width=15)
        self.amount_field.pack(side=tk.LEFT, padx=5)

        eth_label = tk.Label(amount_frame, text="ETH")
        eth_label.pack(side=tk.LEFT)

        # --- Address dropdown ---
        self.address_combobox = ttk.Combobox(self, state="readonly", width=45)
        self.address_combobox.pack(pady=10)

        addresses = self.load_addresses()
        options = ["---"] + [f"{label} - {addr}" for label, addr in addresses.items()]
        self.address_combobox["values"] = options
        self.address_combobox.current(0)

        # --- Transfer button ---
        transfer_button = ttk.Button(self, text="Transfer", command=self.transfer_button_on_clicked)
        transfer_button.pack(pady=10)

        # --- Start balance updater thread ---
        self.running = True
        Thread(target=self.update_balance_loop, daemon=True).start()

    def load_addresses(self):
        """Load wallet addresses from JSON file."""
        if not os.path.exists(self.wallet_db_path):
            return {}
        try:
            with open(self.wallet_db_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid wallet database format.")
            return {}

    def update_balance_loop(self):
        """Continuously fetch balance and update label."""
        while self.running:
            try:
                wallet_account = accounts.load(self.username)
                balance_wei = int(wallet_account.balance)
                balance_eth = balance_wei / 10**18
                self.balance_field.config(text=f"{balance_eth:.6f} ETH")
            except Exception:
                self.balance_field.config(text="Error")
            time.sleep(1)

    def transfer_button_on_clicked(self):
        """Handle ETH transfer when button is clicked."""
        label_address = self.address_combobox.get()
        if label_address == "---":
            messagebox.showerror("Error", "Please select an address.")
            return

        try:
            label, address = label_address.split(" - ")
        except ValueError:
            messagebox.showerror("Error", "Invalid address entry.")
            return

        amount = self.amount_field.get().strip()
        if not amount:
            messagebox.showerror("Error", "Please enter an amount.")
            return

        amount_wei = amount + "000000000000000000"  # ETH to Wei

        try:
            wallet_account = accounts.load(self.username)
            wallet_account.set_autosign(True, passphrase=self.password)
            wallet_account.transfer(address, amount_wei)
            messagebox.showinfo("Success", f"Transferred {amount} ETH to {label}")

            self.address_combobox.current(0)
            self.amount_field.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Transfer failed: {e}")

    def on_close(self):
        """Cleanly stop background thread and close app."""
        self.running = False
        self.destroy()


def main():
    app = WalletApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()



