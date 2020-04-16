import json


class Location:
    def __init__(self, type):
        self.type = type

    @staticmethod
    def from_json(json_):
        if (json_["type"] == "blockchain"):
            return BlockchainLocation.from_json(json_)
        elif (json_["type"] == "wallet"):
            return WalletLocation.from_json(json_)

class WalletLocation(Location):
    def __init__(self, id):
        Location.__init__(self, "wallet")
        self.id = id

    @staticmethod
    def from_json(json_):
        return WalletLocation(json_["id"])

class BlockchainLocation(Location):
    def __init__(self, address, chain):
        Location.__init__(self, "blockchain")
        self.address = address
        self.chain = chain

    @staticmethod
    def from_json(json_):
        return BlockchainLocation(json_["address"], json_["chain"])

class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    @staticmethod
    def from_json(json_):
        return Money(json_["amount"], json_["currency"])

class Transfer:
    def __init__(self, id, source, destination, amount, status, transactionHash):
        self.id = id
        self.source = source
        self.destination = destination
        self.amount = amount
        self.status = status
        self.transactionHash = transactionHash

    @staticmethod
    def from_json(json_):
        return Transfer(
                json_["id"],
                Location.from_json(json_["source"]),
                Location.from_json(json_["destination"]),
                Money.from_json(json_["amount"]),
                json_["status"],
                json_.get("transactionHash"))

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def __repr__(self):
        return self.__str__()
