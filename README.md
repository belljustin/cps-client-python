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
  wallet-address-create       Create a new wallet address.
  wallet-addresses-get        Get a collection of wallet addresses.
  wallet-create               Create a new wallet.
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

## Development

Fork this repo and do the following to get setup:

```sh
# clone the repository and add upstream so you can fetch the latest changes
git clone git@github.com:<your-username>/cps-client-python.git
git remote add upstream git@github.com:belljustin/cps-client-python.git

# create a virtualenv
cd cps-client-python
virtualenv -p python3 venv
source venv/bin/activate

# install the project in editable mode
pip install -e .
```

Now, as long as you're using the virtualenv, you can use cps-client with all the edits you've made including running the cli tool.

To test, you'll need a CPS API key.
You can get this by signing up for the sandbox here: https://my-sandbox.circle.com/.
To run the cli and integration tests, this needs to exist as an environment variable named `$CPS_API_KEY`

You can then run all the integration tests via the make file:

```
make integration
```

or run individual tests with the python unittest command, e.g:

```sh
python -m unittest tests.integration.test_integration.TestBasic.test_get_wallet_addresses
```

To submit a contribution, open a pull request against the master branch on upstream.
