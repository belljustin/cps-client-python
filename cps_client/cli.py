#!/usr/bin/env python3 

import os

import click

from . import api


@click.group()
def cli():
    pass

@click.command()
def wallet_create():
    """Create a new wallet."""

    c = getClient()
    wallet = c.create_wallet()

    print(wallet)

@click.command()
@click.argument('walletid')
def wallet_get(walletid):
    """Get a wallet.

    WALLETID identifier of the wallet with which the created address will be associated.
    """

    c = getClient()
    wallet = c.get_wallet(walletid)

    print(wallet)

@click.command()
@click.option('--from', 'from_', default=None, help='Items created since the specified date-time (inclusive). Must be ISO-8691 formatted')
@click.option('--to', default=None, help='Items created before the specified date-time (inclusive). Must be ISO-8601 formatted.')
@click.option('--pageSize', default=50, help='The number of items to fetch per page.')
def wallets_get(from_, to, pagesize):
    """Get a collection of wallets."""

    c = getClient()

    paginationParams = api.PaginationParams(pageSize=pagesize)
    datetimeParams = api.DateTimeParams(from_, to)

    paginate(lambda paginateParams: c.get_wallets(paginateParams, datetimeParams), paginationParams)

@click.command()
@click.argument('walletid')
@click.option('--currency', default='USD', help='the receivable currency of the generated address.')
@click.option('--chain', default='ETH', help='the blockchain on which the address will be generated.')
def wallet_address_create(walletid, currency, chain):
    """Create a new wallet address.

    WALLETID identifier of the wallet with which the created address will be associated.
    """

    c = getClient()
    address = c.create_wallet_address(walletid, currency, chain)

    print(address)

@click.command()
@click.argument('walletid')
@click.option('--from', 'from_', default=None, help='Items created since the specified date-time (inclusive). Must be ISO-8691 formatted')
@click.option('--to', default=None, help='Items created before the specified date-time (inclusive). Must be ISO-8601 formatted.')
@click.option('--pageSize', default=50, help='The number of items to fetch per page.')
def wallet_addresses_get(walletid, from_, to, pagesize):
    """Get a collection of wallet addresses.

    WALLETID identifier of the wallet to get associated addresses.
    """

    c = getClient()

    paginationParams = api.PaginationParams(pageSize=pagesize)
    datetimeParams = api.DateTimeParams(from_, to)

    paginate(lambda paginateParams: c.get_wallet_addresses(walletid, paginateParams, datetimeParams), paginationParams)

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
@click.argument('sourcewalletid')
@click.argument('destwalletid')
@click.argument('amount')
@click.option('--currency', default='USD', help='the amount currency to transfer. Defaults to USD.')
def transfer_create_wallet(sourcewalletid, destwalletid, amount, currency):
    """Create transfers from a wallet to another wallet.

    SOURCEWALLETID the source wallet id.\n
    DESTWALLETID the destination wallet id.\n
    AMOUNT the value to send.
    """

    source = api.WalletLocation(sourcewalletid)
    destination = api.WalletLocation(destwalletid)
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
    transferParams = api.TransferParams(sourcewalletid, destinationwalletid)

    paginate(lambda paginateParams: c.get_transfers(paginateParams, datetimeParams, transferParams), paginationParams)

@click.command()
def configuration_get():
    """Get global CPS configuration."""

    c = getClient()
    config = c.get_configuration()
    
    print(config)

@click.command()
@click.argument("endpoint")
def subscription_create(endpoint):
    """Create a subscription.

    ENDPOINT the endpoint that will receive subscription notifications.
    """

    c = getClient()
    subscription = c.create_subscription(endpoint)

    print(subscription)

@click.command()
def subscriptions_get():
    """Get a collection of subscriptions."""

    c = getClient()
    subscriptions = c.get_subscriptions()

    print(subscriptions)

@click.command()
@click.argument("id")
def subscription_delete(id):
    """Delete a subscription.

    ID of the subscription to be deleted.
    """

    c = getClient()
    subscriptions = c.delete_subscription(id)

    print("success")

def getClient():
    API_BASE_URL = os.environ.get('CPS_API_BASE_URL', 'https://api-sandbox.circle.com')
    API_KEY = os.environ['CPS_API_KEY']
    return api.Client(API_BASE_URL, API_KEY)

def paginate(supplier, paginationParams):
    results = supplier(paginationParams)
    while len(results) > 0:
        print(results)

        i = input('n(next) / q(quit): ')
        if (i == 'n' or i == 'next'):
            paginationParams.set_page_after(results[-1].page_after())
            results = supplier(paginationParams)
        else:
            return


def run():
    cli.add_command(wallet_create)
    cli.add_command(wallet_get)
    cli.add_command(wallets_get)
    cli.add_command(wallet_address_create)
    cli.add_command(wallet_addresses_get)
    cli.add_command(transfer_create_blockchain)
    cli.add_command(transfer_create_wallet)
    cli.add_command(transfer_get)
    cli.add_command(transfers_get)
    cli.add_command(configuration_get)
    cli.add_command(subscription_create)
    cli.add_command(subscriptions_get)
    cli.add_command(subscription_delete)

    cli()

if __name__ == '__main__':
    run()
