import json


class CreateSubscriptionRequest:
    def __init__(self, endpoint):
        self.endpoint = endpoint

class Subscription:
    def __init__(self, id, endpoint, subscriptionDetails):
        self.id = id
        self.endpoint = endpoint
        self.subscriptionDetails = subscriptionDetails

    @staticmethod
    def from_json(json_):
        details = [SubscriptionDetails.from_json(d) for d in json_["subscriptionDetails"]]
        return Subscription(json_["id"], json_["endpoint"], details)

    def __str__(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def __repr__(self):
        return self.__str__()

class SubscriptionDetails:
    def __init__(self, url, status):
        self.url = url
        self.status = status

    @staticmethod
    def from_json(json_):
        return SubscriptionDetails(json_["url"], json_["status"])
