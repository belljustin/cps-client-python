import json
import uuid
import re

import requests

from .transfer import Transfer
from .configuration import Configuration

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
    def __init__(self, sourceWalletId, destinationWalletId, *moreParams):
        self.params = {
            "sourceWalletId": sourceWalletId,
            "destinationWalletId": destinationWalletId
        }
        for p in moreParams:
            self.params = { **self.params, **p.get_params() }

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

    def get_transfers(self, params=None):
        resource = "/".join([self.host, self.version, "transfers"])

        res = requests.get(
                resource,
                headers = self._default_headers(),
                params = params)
        Client.__check_status_code(res)

        return [Transfer.from_json(t) for t in res.json()["data"]]

    def get_configuration(self):
        resource = "/".join([self.host, self.version, "configuration"])

        res = requests.get(
                resource,
                headers = self._default_headers())
        Client.__check_status_code(res)

        return Configuration.from_json(res.json()["data"])
