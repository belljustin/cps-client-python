class Configuration:
    def __init__(self, payments):
        self.payments = payments

    def from_json(json_):
        return Configuration(PaymentsConfiguration(json_['payments']))

class PaymentsConfiguration:
    def __init__(self, masterWalletId):
        self.masterWalletId = masterWalletId

    def from_json(json_):
        return PaymentsConfiguration(json_['masterWalletId'])
