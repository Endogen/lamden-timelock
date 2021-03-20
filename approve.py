import json
import time
import requests

from lamden.crypto.transaction import build_transaction
from lamden.crypto.wallet import Wallet

# Maternode URL (testnet)
url = "https://testnet-master-1.lamden.io"
wallet = Wallet("<some privkey>")

# Get nonce for our address
nonce = requests.get(f"{url}/nonce/{wallet.verifying_key}")
nonce = json.loads(nonce.text)

# Build transaction to approve contract to spend TAU
tx = build_transaction(
    wallet=wallet,
    processor=nonce["processor"],
    stamps=100,
    nonce=nonce["nonce"],
    contract="currency",
    function="approve",
    kwargs={"amount": 100000, "to": "con_lock_test15"}
)

# Send transaction
approve = requests.post(url, data=tx)
print("approve", approve.text)

# Wait to make sure that transaction is already processed
time.sleep(2)

# Get amount of TAU that is approved to be spent by the smart contract
key = f"{wallet.verifying_key}:con_lock_test15"
verify = requests.get(f"{url}/contracts/currency/balances?key={key}")
print("verify", verify.text)
