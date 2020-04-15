# Circle Platform Services - Python Client

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
```
