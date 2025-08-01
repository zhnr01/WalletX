import os
import sys
import json
import tkinter as tk
from tkinter import ttk, messagebox


class AddAddressToDbWidget(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Add Address to Wallet DB")
        self.geometry("300x180")
        self.resizable(False, False)

        self.wallet_db_path = "wallet_db.json"

        # Address field
        tk.Label(self, text="Address:").pack(anchor="w", padx=10, pady=(10, 0))
        self.address_field = tk.Entry(self, width=40)
        self.address_field.pack(padx=10, pady=5)

        # Label field
        tk.Label(self, text="Label:").pack(anchor="w", padx=10)
        self.label_field = tk.Entry(self, width=40)
        self.label_field.pack(padx=10, pady=5)

        # Save button
        save_button = ttk.Button(self, text="Save", command=self.save_button_on_clicked)
        save_button.pack(pady=10)

    def save_button_on_clicked(self):
        address = self.address_field.get().strip()
        label = self.label_field.get().strip()

        if not address or not label:
            messagebox.showerror("Error", "Please enter both an address and a label.")
            return

        try:
            if not os.path.exists(self.wallet_db_path):
                data = {}
            else:
                with open(self.wallet_db_path, "r") as f:
                    data = json.load(f)

            data[label] = address

            with open(self.wallet_db_path, "w") as f:
                json.dump(data, f, indent=4)

            messagebox.showinfo("Success", f"Address saved under label '{label}'.")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Could not save address: {e}")


def main():
    app = AddAddressToDbWidget()
    app.mainloop()

