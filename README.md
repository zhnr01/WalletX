# WalletX
A simple Web3 wallet.


````markdown
# Cryptocurrency Wallet (Tkinter + Ape Framework)

A simple cryptocurrency wallet built with **Tkinter** for the GUI and **Ape Framework** for blockchain interactions.  
This wallet allows you to:
- View your real-time ETH balance
- Send ETH to saved addresses
- Manage saved addresses in a local JSON database

The project uses the **Ape Framework** for Ethereum account management and a **Geth local blockchain environment** for development.

---

## Features

- **Real-time ETH balance updates**
- **Send ETH** to stored addresses
- **Address book** stored in `wallet_db.json`
- **Tkinter GUI** for easy use
- **Ape Framework** account handling

---

## Prerequisites

Before you begin, make sure you have:

1. **Python 3.10+** installed
2. **Geth** installed and running for local Ethereum development  
   [Install Geth](https://geth.ethereum.org/docs/getting-started/installing-geth)
3. **Ape Framework** installed  
   ```bash
   pip install eth-ape'[recommended-plugins]'
````

4. **Node provider access** (Infura, Alchemy, or local Geth)

---

## Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/zhnr01/WalletX
cd WalletX
```

### 2️⃣ Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate  # On macOS/Linux
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

The wallet uses environment variables stored in a `.env` file.
Create a `.env` file in the project root:

```env
WALLET_USERNAME=your_wallet_account_name
WALLET_PASSWORD=your_wallet_password
```

---

## Generating Ape Accounts

To generate accounts with Ape Framework:

```bash
ape accounts generate your_wallet_account_name
```

You will be prompted to create a password — use the same one in your `.env` file.

---

## Running a Local Ethereum Node with Geth

Start a local Geth development node:

```bash
geth --dev --http --http.addr 127.0.0.1 --http.port 8545 --http.api eth,web3,net,personal
```

You can also use Sepolia or any Ethereum testnet via Infura/Alchemy by configuring Ape.

---

## Running the Wallet

Run the Tkinter wallet:

```bash
ape run full_wallet --network ethereum:local:node
```

---

## Database File

The wallet stores saved addresses in `wallet_db.json` in the project root.
