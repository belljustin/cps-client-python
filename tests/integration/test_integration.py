import unittest
import time
import os

from cps_client import api

class TestBasic(unittest.TestCase):
    def setUp(self):
        API_KEY = os.environ['CPS_API_KEY']
        self.client = api.Client("https://api-sandbox.circle.com", API_KEY)

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

    def test_get_transfers(self):

        # it's assumed that some transfers exist
        transfers = self.client.get_transfers()

        self.assertIsNotNone(transfers)

        transferParams = api.PaginationParams(pageSize=1)
        transfers = self.client.get_transfers(transferParams.get_params())

        self.assertIsNotNone(transfers)
        self.assertEqual(len(transfers), 1)

        lastTransfer = transfers[-1]
        transferParams = api.PaginationParams(pageSize=1, pageAfter=lastTransfer.id)
        transfers = self.client.get_transfers(transferParams.get_params())

        self.assertIsNotNone(transfers)
        self.assertEqual(len(transfers), 1)
        self.assertNotEqual(transfers[0].id, lastTransfer.id)

    def test_create_wallet(self):

        wallet = self.client.create_wallet()

        self.assertIsNotNone(wallet.walletId)
