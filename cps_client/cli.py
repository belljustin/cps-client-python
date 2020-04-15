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
def transfer_create_blockchain(walletid, address, amount, currency, chain):
    """Create transfers from a wallet to blockchain address.

    WALLETID the source wallet id.\n
    ADDRESS the blockchain destination address.\n
    AMOUNT the value to send.
    """

    source = api.WalletLocation(walletid)
    destination = api.BlockchainLocation(address, chain)
    amount = api.Money(amount, currency)

    c = getClient()
    transfer = c.create_transfer(source, destination, amount)

    print(transfer)

@click.command()
@click.argument('id')
def transfer_get(id):
    """Get info about transfers.

    ID the unique identifier of the transfer.
    """
    c = getClient()
    transfer = c.get_transfer(id)
    
    print(transfer)

@click.command()
def configuration_get():
    """Get global CPS configuration"""
    c = getClient()
    config = c.get_configuration(id)
    
    print(config)


def getClient():
    API_KEY = os.environ['CPS_API_KEY']
    return api.Client("https://api-sandbox.circle.com", API_KEY)


def run():
    cli.add_command(transfer_create_blockchain)
    cli.add_command(transfer_get)
    cli.add_command(configuration_get)

    cli()

if __name__ == '__main__':
    run()
