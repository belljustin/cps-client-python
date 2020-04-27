import unittest
import time
import os

from cps_client import api

class TestBasic(unittest.TestCase):
    def setUp(self):
        API_BASE_URL = os.environ.get('CPS_API_BASE_URL', 'https://api-sandbox.circle.com')
        API_KEY = os.environ['CPS_API_KEY']
        self.client = api.Client(API_BASE_URL, API_KEY)

    def test_get_configuration(self):
        config = self.client.get_configuration()
        self.assertIsNotNone(config.payments.masterWalletId)

    def test_create_and_get_blockchain_transfer(self):

        # it's assumed the master wallet is pre-funded with amounts sufficient to run these tests
        config = self.client.get_configuration()
        self.assertIsNotNone(config.payments.masterWalletId)


        source = api.WalletLocation(config.payments.masterWalletId)
        destination = api.BlockchainLocation("0x71715Da6ADa699e3a1a5C2664A55fF3D179c86EE", "ETH")
        amount = api.Money("0.01", "USD")

        transfer = self.client.create_transfer(source, destination, amount)

        self.assertIsNotNone(transfer.id)
        self.assertEqual(transfer.source.id, source.id)
        self.assertEqual(transfer.destination.address, destination.address)
        self.assertEqual(transfer.destination.chain, destination.chain)
        self.assertEqual(transfer.amount.amount, amount.amount)
        self.assertEqual(transfer.amount.currency, amount.currency)
        self.assertIsNotNone(transfer.status)

        retrievedTransfer = self.client.get_transfer(transfer.id)
        self.assertEqual(retrievedTransfer.id, transfer.id)
        self.assertEqual(retrievedTransfer.destination.address, destination.address)
        self.assertEqual(retrievedTransfer.destination.chain, destination.chain)
        self.assertEqual(retrievedTransfer.amount.amount, amount.amount)
        self.assertEqual(retrievedTransfer.amount.currency, amount.currency)
        self.assertIsNotNone(transfer.status)

    def test_create_wallet_transfer(self):

        # it's assumed the master wallet is pre-funded with amounts sufficient to run these tests
        config = self.client.get_configuration()
        self.assertIsNotNone(config.payments.masterWalletId)

        dest_wallet = self.client.create_wallet()
        self.assertIsNotNone(dest_wallet.walletId)

        source = api.WalletLocation(config.payments.masterWalletId)
        destination = api.WalletLocation(dest_wallet.walletId)
        amount = api.Money("0.01", "USD")

        transfer = self.client.create_transfer(source, destination, amount)

        self.assertIsNotNone(transfer.id)
        self.assertEqual(transfer.source.id, source.id)
        self.assertEqual(transfer.destination.id, destination.id)
        self.assertEqual(transfer.amount.amount, amount.amount)
        self.assertEqual(transfer.amount.currency, amount.currency)
        self.assertIsNotNone(transfer.status)


    def test_get_transfers(self):

        # it's assumed that some transfers exist
        transfers = self.client.get_transfers()

        self.assertIsNotNone(transfers)

        paginationParams = api.PaginationParams(pageSize=1)
        transfers = self.client.get_transfers(paginationParams)

        self.assertIsNotNone(transfers)
        self.assertEqual(len(transfers), 1)

        paginationParams.set_page_after(transfers[-1].page_after())
        nextTransfers = self.client.get_transfers(paginationParams)

        self.assertIsNotNone(nextTransfers)
        self.assertEqual(len(nextTransfers), 1)
        self.assertNotEqual(nextTransfers, transfers)

    def test_create_wallet(self):

        wallet = self.client.create_wallet()

        self.assertIsNotNone(wallet.walletId)

        wallet = self.client.get_wallet(wallet.walletId)
        self.assertIsNotNone(wallet.walletId)

    def test_get_wallets(self):
        # create another wallet so there's at least two
        wallet = self.client.create_wallet()
        self.assertIsNotNone(wallet)

        paginationParams = api.PaginationParams(pageSize=1)
        wallets = self.client.get_wallets(paginationParams)

        self.assertIsNotNone(wallets)
        self.assertEqual(len(wallets), 1)

        paginationParams.set_page_after(wallets[-1].page_after())
        nextWallets = self.client.get_wallets(paginationParams)

        self.assertIsNotNone(nextWallets)
        self.assertEqual(len(nextWallets), 1)
        self.assertNotEqual(nextWallets, wallets)

    def test_create_address(self):

        wallet = self.client.create_wallet()
        self.assertIsNotNone(wallet.walletId)

        address = self.client.create_wallet_address(wallet.walletId, "USD", "ETH")
        self.assertIsNotNone(address.address)
        self.assertEqual(address.currency, "USD")
        self.assertEqual(address.chain, "ETH")

    def test_get_wallet_addresses(self):

        wallet = self.client.create_wallet()
        self.assertIsNotNone(wallet.walletId)

        n = 2
        addresses = [self.client.create_wallet_address(wallet.walletId, "USD", "ETH") for _ in range(n)]
        addresses.reverse() # reverse because retrieve list will be in reverse chronological order
        retreivedAddresses = self.client.get_wallet_addresses(wallet.walletId)

        for i in range(n):
            self.assertEqual(addresses[i].address, retreivedAddresses[i].address)
