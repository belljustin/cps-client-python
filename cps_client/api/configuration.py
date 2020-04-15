class Configuration:
    def __init__(self, payments):
        self.payments = payments

    def from_json(json_):
        paymentsConfig = PaymentsConfiguration.from_json(json_['payments'])
        return Configuration(paymentsConfig)

class PaymentsConfiguration:
    def __init__(self, masterWalletId):
        self.masterWalletId = masterWalletId

    def from_json(json_):
        return PaymentsConfiguration(json_['masterWalletId'])
