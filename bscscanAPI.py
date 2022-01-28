from requests import get
import json, requests
import config
import dbms
import time


class BSCscanner:
	endpoint = "https://api.bscscan.com/api"
	
	def __init__(self, apiKey):
		self.apiKey = apiKey
		self.apiKeyEndpoint = "&apikey=" + self.apiKey
	
	def verify(self, address):
		action = "?module=contract&action=getabi"
		address = "&address=" + address
		url = self.endpoint + action + address + self.apiKeyEndpoint
		response = requests.get(url).json()
		return response["message"] == "OK"
	
	def getContractABI(self, address):
		action = "?module=contract&action=getabi"
		address = "&address=" + address
		url = self.endpoint + action + address + self.apiKeyEndpoint
		response = requests.get(url).json()["result"]
		return str(response)
	
	def getContractSourceCode(self, address):
		if self.verify(address):
			action = "?module=contract&action=getsourcecode"
			address = "&address=" + address
			url = self.endpoint + action + address + self.apiKeyEndpoint
			response = requests.get(url).json()["result"]
			return str(response[0]["SourceCode"])
		else:
			return None


class scanSCAMTokens(BSCscanner):
	
	def isNotPancakeRouterV1(self, sourceCode):
		return "0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F" in sourceCode
	
	def scamFuncs(self, sourceCode):
		return "newun" in sourceCode or "function transferFrom(address sender, address recipient, uint256 amount) public override returns (bool)" in sourceCode
	
	def audit(self, address):
		sourceCode = self.getContractSourceCode(address)
		if sourceCode != None:
			if not self.isNotPancakeRouterV1(sourceCode) and not self.scamFuncs(sourceCode):
				return True
			else:
				return False
		else:
			return False

if __name__ == "__main__":
	pass
