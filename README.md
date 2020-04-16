# Circle Platform Services - Python Client

[![PyPI version](https://badge.fury.io/py/cps-client.svg)](https://badge.fury.io/py/cps-client)

## WARNING: work in progress and subject to change

A python client and CLI for working with Circle Platform Services.

## Installation

```sh
pip install cps-client
```

## Usage

cps-client uses an enviroment variable to fetch your API key.

```sh
export CPS_API_KEY="<api-key>"
```

### CLI

Installation provides a command line interface for interacting with CPS.

```sh
Usage: cps [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  configuration-get           Get global CPS configuration
  transfer-create-blockchain  Create transfers from a wallet to blockchain...
  transfer-get                Get info about transfers.
  transfers-get               Get collection of transfers.
```

### Library

You can also use cps-client as a library.

```python
from cps_client import api

# you can get your own at https://my-sandbox.circle.com/
API_KEY="my-circle-sanbox-api-key" 

source = api.WalletLocation(walletid)
destination = api.BlockchainLocation(address, chain)
amount = api.Money(amount, currency)

cpsAPI = api.Client("https://api-sandbox.circle.com", API_KEY)
transfer = cpsAPI.create_transfer(source, destination, amount)

print(transfer)

"""
Output:

{
    "id": "b08478d5-a110-4b0e-9136-4b9d94601c65",
    "source": {
        "type": "wallet",
        "id": "1000004286"
    },
    "destination": {
        "type": "blockchain",
        "address": "0x71715Da6ADa699e3a1a5C2664A55fF3D179c86EE",
        "chain": "ETH"
    },
    "amount": {
        "amount": "0.05",
        "currency": "USD"
    },
    "status": "complete",
    "transactionHash": "0x52176702740c8720d77ade3f20014396a4a2eb13d09dd1e6bffcc6f209a45326"
}
"""
```
