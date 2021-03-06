import json
import uuid
import re

import requests

from .wallet import Wallet, Address, CreateWalletRequest, CreateAddressRequest
from .transfer import Transfer
from .configuration import Configuration
from .subscription import Subscription, CreateSubscriptionRequest

class HttpException(Exception):
    def __init__(self, status_code):
        self.status_code = status_code

class ClientException(HttpException):
    pass

class ServerException(HttpException):
    pass

class CreateTransferRequest:
    def __init__(self, source, destination, amount):
        self.idempotencyKey = str(uuid.uuid4())
        self.source = source
        self.destination = destination
        self.amount = amount

class PaginationParams:
    def __init__(self, pageSize=50, pageBefore=None, pageAfter=None):
        if pageBefore is not None and pageAfter is not None:
            raise ValueError("cannot specify both pageBefore and pageAfter for PaginationParams")

        self.params = {
            "pageSize": pageSize,
            "pageBefore": pageBefore,
            "pageAfter": pageAfter
        }

    def set_page_after(self, pageAfter):
        self.params["pageBefore"] = None
        self.params["pageAfter"] = pageAfter

    def set_page_before(self, pageBefore):
        self.params["pageAfter"] = None
        self.params["pageBefore"] = pageBefore

    def get_params(self):
        return self.params

class DateTimeParams:
    regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex).match

    def __init__(self, from_=None, to=None):
        if from_ is not None:
            DateTimeParams.match_iso8601(from_)

        if to is not None:
            DateTimeParams.match_iso8601(to)

        self.params = {
            "from": from_,
            "to": to,
        }

    def get_params(self):
        return self.params

class TransferParams:
    def __init__(self, sourceWalletId, destinationWalletId):
        self.params = {
            "sourceWalletId": sourceWalletId,
            "destinationWalletId": destinationWalletId
        }

    def get_params(self):
        return self.params

class Client:
    def __init__(self, host, creds, version="v1"):
        self.host = host
        self.creds = creds
        self.version = version

    def _default_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.creds
        }

    @staticmethod
    def __check_status_code(res):
        if (res.status_code >= requests.codes.internal_server_error):
            raise ServerException(res.status_code)
        elif (res.status_code >= requests.codes.bad_request):
            raise ClientException(res.status_code)

    """ wallets """

    def create_wallet(self):
        req = CreateWalletRequest()
        resource = "/".join([self.host, self.version, "wallets"])

        res = requests.post(
                resource,
                data = json.dumps(req, default=lambda o: o.__dict__),
                headers = self._default_headers())
        Client.__check_status_code(res)

        return Wallet.from_json(res.json()["data"])

    def get_wallet(self, walletId):
        resource = "/".join([self.host, self.version, "wallets", walletId])

        res = requests.get(
                resource,
                headers = self._default_headers())
        Client.__check_status_code(res)

        return Wallet.from_json(res.json()["data"])

    def get_wallets(self, *params):
        resource = "/".join([self.host, self.version, "wallets"])

        qparams = dict()
        for p in params:
            qparams = { **qparams, **p.get_params() }

        res = requests.get(
                resource,
                headers = self._default_headers(),
                params = qparams)
        Client.__check_status_code(res)

        return [Wallet.from_json(w) for w in res.json()["data"]]

    """ addresses """

    def create_wallet_address(self, walletId, currency, chain):
        req = CreateAddressRequest(currency, chain)
        resource = "/".join([self.host, self.version, "wallets", walletId, "addresses"])

        res = requests.post(
                resource,
                data = json.dumps(req, default=lambda o: o.__dict__),
                headers = self._default_headers())
        Client.__check_status_code(res)

        return Address.from_json(res.json()["data"])

    def get_wallet_addresses(self, walletId, *params):
        resource = "/".join([self.host, self.version, "wallets", walletId, "addresses"])

        qparams = dict()
        for p in params:
            qparams = { **qparams, **p.get_params() }

        res = requests.get(
                resource,
                headers = self._default_headers(),
                params = qparams)
        Client.__check_status_code(res)

        return [Address.from_json(a) for a in res.json()["data"]]

    """ transfers """

    def create_transfer(self, source, destination, amount):
        req = CreateTransferRequest(source, destination, amount)
        resource = "/".join([self.host, self.version, "transfers"])

        res = requests.post(
                resource,
                data = json.dumps(req, default=lambda o: o.__dict__),
                headers = self._default_headers())
        Client.__check_status_code(res)

        return Transfer.from_json(res.json()["data"])

    def get_transfer(self, id):
        resource = "/".join([self.host, self.version, "transfers", id])

        res = requests.get(
                resource,
                headers = self._default_headers())
        Client.__check_status_code(res)

        return Transfer.from_json(res.json()["data"])

    def get_transfers(self, *params):
        resource = "/".join([self.host, self.version, "transfers"])

        qparams = dict()
        for p in params:
            qparams = { **qparams, **p.get_params() }

        res = requests.get(
                resource,
                headers = self._default_headers(),
                params = qparams)
        Client.__check_status_code(res)

        return [Transfer.from_json(t) for t in res.json()["data"]]

    """ configuration """

    def get_configuration(self):
        resource = "/".join([self.host, self.version, "configuration"])

        res = requests.get(
                resource,
                headers = self._default_headers())
        Client.__check_status_code(res)

        return Configuration.from_json(res.json()["data"])

    """ subscriptions """

    def create_subscription(self, endpoint):
        req = CreateSubscriptionRequest(endpoint)
        resource = "/".join([self.host, self.version, "notifications/subscriptions"])

        res = requests.post(
                resource,
                data = json.dumps(req, default=lambda o: o.__dict__),
                headers = self._default_headers())
        Client.__check_status_code(res)

        return Subscription.from_json(res.json()["data"])

    def get_subscriptions(self):
        resource = "/".join([self.host, self.version, "notifications/subscriptions"])

        res = requests.get(
                resource,
                headers = self._default_headers())
        Client.__check_status_code(res)

        return [Subscription.from_json(s) for s in res.json()["data"]]

    def delete_subscription(self, id):
        resource = "/".join([self.host, self.version, "notifications/subscriptions", id])

        res = requests.delete(
                resource,
                headers = self._default_headers())
        Client.__check_status_code(res)
