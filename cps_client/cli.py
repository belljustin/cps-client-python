#!/usr/bin/env python3 

import os

import click

from . import api


@click.group()
def cli():
    pass

@click.command()
@click.argument('walletid')
@click.argument('address')
@click.argument('amount')
@click.option('--chain', default='ETH', help='The destination chain. Defaults to ETH.')
@click.option('--currency', default='USD', help='The amount currency to transfer. Defaults to USD.')
def create_blockchain_transfer(walletid, address, amount, currency, chain):
    """Create transfers from a wallet to blockchain address.

    WALLETID the source wallet id.\n
    ADDRESS the blockchain destination address.\n
    AMOUNT the value to send.
    """

    source = api.WalletLocation(walletid)
    destination = api.BlockchainLocation(address, chain)
    amount = api.Money(amount, currency)

    c = getClient()
    transfer = c.createTransfer(source, destination, amount)

    print(transfer)

@click.command()
@click.argument('id')
def get_transfer(id):
    """Get info about transfers.

    ID the unique identifier of the transfer.
    """
    c = getClient()
    transfer = c.getTransfer(id)
    
    print(transfer)


def getClient():
    API_KEY = os.environ['CPS_API_KEY']
    return api.Client("https://api-sandbox.circle.com", API_KEY)


def run():
    cli.add_command(create_blockchain_transfer)
    cli.add_command(get_transfer)

    cli()

if __name__ == '__main__':
    run()
