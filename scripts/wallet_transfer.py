import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from ape import accounts
from dotenv import load_dotenv

class TransferWidget(tk.Tk):
    def __init__(self):
        super().__init__()
        load_dotenv()

        self.title("Transfer ETH")
        self.geometry("300x180")
        self.resizable(False, False)

        self.username = os.environ["WALLET_USERNAME"]
        self.password = os.environ["WALLET_PASSWORD"]

        # Amount field with ETH label
        amount_frame = tk.Frame(self)
        amount_frame.pack(pady=5)

        self.amount_field = tk.Entry(amount_frame, width=20)
        self.amount_field.pack(side=tk.LEFT, padx=5)

        eth_label = tk.Label(amount_frame, text="ETH")
        eth_label.pack(side=tk.LEFT)

        # Address field
        self.address_field = tk.Entry(self, width=30)
        self.address_field.insert(0, "Address")
        self.address_field.pack(pady=5)

        # Transfer button
        transfer_button = ttk.Button(self, text="Transfer", command=self.transfer_button_on_clicked)
        transfer_button.pack(pady=10)

    def transfer_button_on_clicked(self):
        address = self.address_field.get().strip()
        amount = self.amount_field.get().strip()

        if not address or address == "Address" or not amount:
            messagebox.showerror("Error", "Please enter a valid address and amount.")
            return

        try:
            # Append wei conversion
            amount_wei = amount + "000000000000000000"

            wallet_account = accounts.load(self.username)
            wallet_account.set_autosign(True, passphrase=self.password)
            wallet_account.transfer(address, amount_wei)

            messagebox.showinfo("Success", f"Transferred {amount} ETH to {address}")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Transfer failed: {str(e)}")


def main():
    app = TransferWidget()
    app.mainloop()

