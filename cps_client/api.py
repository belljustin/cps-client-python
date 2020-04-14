import requests
import jsonpickle
import uuid


class Location:
    def __init__(self, type):
        self.type = type

    def fromJSON(json_):
        if (json_["type"] == "blockchain"):
            return BlockchainLocation.fromJSON(json_)
        elif (json_["type"] == "wallet"):
            return WalletLocation.fromJSON(json_)

class WalletLocation(Location):
    def __init__(self, id):
        Location.__init__(self, "wallet")
        self.id = id

    def fromJSON(json_):
        return WalletLocation(json_["id"])

class BlockchainLocation(Location):
    def __init__(self, address, chain):
        Location.__init__(self, "blockchain")
        self.address = address
        self.chain = chain

    def fromJSON(json_):
        return BlockchainLocation(json_["address"], json_["chain"])

class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def fromJSON(json_):
        return Money(json_["amount"], json_["currency"])

class Transfer:
    def __init__(self, id, source, destination, amount, status, transactionHash):
        self.id = id
        self.source = source
        self.destination = destination
        self.amount = amount
        self.status = status
        self.transactionHash = transactionHash

    def fromJSON(json_):
        return Transfer(
                json_["id"],
                Location.fromJSON(json_["source"]),
                Location.fromJSON(json_["destination"]),
                Money.fromJSON(json_["amount"]),
                json_["status"],
                json_["transactionHash"])

    def __str__(self):
        return jsonpickle.encode(self, unpicklable=False)

class CreateTransferRequest:
    def __init__(self, source, destination, amount):
        self.idempotencyKey = str(uuid.uuid4())
        self.source = source
        self.destination = destination
        self.amount = amount

class HttpException(Exception):
    def __init__(self, status_code):
        self.status_code = status_code

class ClientException(HttpException):
    pass

class ServerException(HttpException):
    pass

class Client:
    def __init__(self, host, creds, version="v1"):
        self.host = host
        self.creds = creds
        self.version = version

    def default_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.creds
        }

    def createTransfer(self, source, destination, amount):
        req = CreateTransferRequest(source, destination, amount)
        resource = "/".join([self.host, self.version, "transfers"])

        res = requests.post(
                resource,
                data = jsonpickle.encode(req),
                headers = self.default_headers())

        if (res.status_code >= requests.codes.internal_server_error):
            raise ServerException(res.status_code)
        elif (res.status_code >= requests.codes.bad_request):
            raise ClientException(res.status_code)
        
        return Transfer.fromJSON(res.json()["data"])

    def getTransfer(self, id):
        resource = "/".join([self.host, self.version, "transfers", id])

        res = requests.get(
                resource,
                headers = self.default_headers())

        if (res.status_code >= requests.codes.internal_server_error):
            raise ServerException(res.status_code)
        elif (res.status_code >= requests.codes.bad_request):
            raise ClientException(res.status_code)
        
        return Transfer.fromJSON(res.json()["data"])
