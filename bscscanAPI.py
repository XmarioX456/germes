from requests import get
import json
import config
def getTransaction(hash):
    url = f"https://api.bscscan.com/api?module=account&action=txlistinternal&txhash={hash}&apikey={config.BSCAPIKey}"
    response = get(url)
    print(response.json())

    #print(j)
getTransaction("0x534ab2ad654f65201517f35136ac42578b3b497deed282722ee4b5708bf99adc")