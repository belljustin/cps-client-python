import json
import uuid

from .transfer import Money


class Wallet:
    def __init__(self, walletId, balances):
        self.walletId = walletId
        self.balances = balances

    def page_after(self):
        self.walletId

    @staticmethod
    def from_json(json_):
        balances = [Money.from_json(m) for m in json_["balances"]]
        return Wallet(json_["walletId"], balances)

    def page_after(self):
        return self.walletId

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def __repr__(self):
        return self.__str__()

class CreateWalletRequest:
    def __init__(self):
        self.idempotencyKey = str(uuid.uuid4())

class Address:
    def __init__(self, address, currency, chain):
        self.address = address
        self.currency = currency
        self.chain = chain

    def page_after(self):
        return self.address

    @staticmethod
    def from_json(json_):
        return Address(json_["address"], json_["currency"], json_["chain"])

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def __repr__(self):
        return self.__str__()

class CreateAddressRequest:
    def __init__(self, currency, chain):
        self.idempotencyKey = str(uuid.uuid4())
        self.currency = currency
        self.chain = chain
