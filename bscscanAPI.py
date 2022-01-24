from requests import get
import json, requests
import config
import dbms


class BSCscaner:

    endpoint = "https://api.bscscan.com/api"

    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.apiKeyEndpoint = "&apikey="+self.apiKey

    def verify(self, address):
        action = "?module=contract&action=getabi"
        address = "&address=" + address
        url = self.endpoint+action+address+self.apiKeyEndpoint
        response = requests.get(url).json()
        return response["message"] == "OK"

    def getContractABI(self, address):
        action = "?module=contract&action=getabi"
        address = "&address=" + address
        url = self.endpoint+action+address+self.apiKeyEndpoint
        response = requests.get(url).json()["result"]
        return response

    def getContractSourceCode(self, address):
        pass

if __name__ == "__main__":
    scaner = BSCscaner(config.BSCAPIKey)
    print(scaner.verify())