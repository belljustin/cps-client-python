import json

class Configuration:
    def __init__(self, payments):
        self.payments = payments

    def from_json(json_):
        paymentsConfig = PaymentsConfiguration.from_json(json_['payments'])
        return Configuration(paymentsConfig)

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def __repr__(self):
        return self.__str__()

class PaymentsConfiguration:
    def __init__(self, masterWalletId):
        self.masterWalletId = masterWalletId

    def from_json(json_):
        return PaymentsConfiguration(json_['masterWalletId'])
