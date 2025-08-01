import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox
from ape import accounts
from dotenv import load_dotenv

class TransferWidget(tk.Tk):
    def __init__(self):
        super().__init__()

        load_dotenv()
        self.title("Cryptocurrency Wallet - Transfer")
        self.geometry("350x200")
        self.resizable(False, False)

        self.username = os.environ["WALLET_USERNAME"]
        self.password = os.environ["WALLET_PASSWORD"]
        self.wallet_db_path = os.path.join(os.getcwd(), "wallet_db.json")


        # Amount field
        amount_frame = tk.Frame(self)
        amount_frame.pack(pady=10)

        self.amount_field = tk.Entry(amount_frame, width=15)
        self.amount_field.pack(side=tk.LEFT, padx=5)

        eth_label = tk.Label(amount_frame, text="ETH")
        eth_label.pack(side=tk.LEFT)

        # Address dropdown
        self.address_combobox = ttk.Combobox(self, state="readonly", width=45)
        self.address_combobox.pack(pady=10)

        addresses = self.load_addresses()
        options = ["---"] + [f"{label} - {addr}" for label, addr in addresses.items()]
        self.address_combobox["values"] = options
        self.address_combobox.current(0)

        # Transfer button
        transfer_button = ttk.Button(self, text="Transfer", command=self.transfer_button_on_clicked)
        transfer_button.pack(pady=10)

    def load_addresses(self):
        if not os.path.exists(self.wallet_db_path):
            return {}
        try:
            with open(self.wallet_db_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid wallet database format.")
            return {}

    def transfer_button_on_clicked(self):
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

        amount_wei = amount + "000000000000000000"  # Convert ETH to wei

        try:
            wallet_account = accounts.load(self.username)
            wallet_account.set_autosign(True, passphrase=self.password)
            wallet_account.transfer(address, amount_wei)
            messagebox.showinfo("Success", f"Transferred {amount} ETH to {label}")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Transfer failed: {e}")


def main():
    app = TransferWidget()
    app.mainloop()


