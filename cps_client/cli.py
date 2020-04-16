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
@click.option('--sourceWalletId', default=None, help='The source wallet id of a transfer.')
@click.option('--destinationWalletId', default=None, help='The destination wallet id of a transfer.')
@click.option('--from', 'from_', default=None, help='Items created since the specified date-time (inclusive). Must be ISO-8691 formatted')
@click.option('--to', default=None, help='Items created before the specified date-time (inclusive). Must be ISO-8601 formatted.')
@click.option('--pageSize', default=50, help='The number of items to fetch per page.')
def transfers_get(sourcewalletid, destinationwalletid, from_, to, pagesize):
    """Get collection of transfers."""

    c = getClient()

    paginationParams = api.PaginationParams(pageSize=pagesize)
    datetimeParams = api.DateTimeParams(from_, to)
    params = api.TransferParams(sourcewalletid, destinationwalletid, datetimeParams)
    transfers = c.get_transfers(params.get_params())

    while len(transfers) > 0:
        print(transfers)

        i = input("n(ext) / q(uit): ")
        if (i == "n" or i == "next"):
            params = api.PaginationParams(pageSize=pagesize, pageAfter=transfers[-1].id)
            transfers = c.get_transfers(params.get_params())
        else:
            return

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
    cli.add_command(transfers_get)
    cli.add_command(configuration_get)

    cli()

if __name__ == '__main__':
    run()
