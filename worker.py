import manBlockchainFuncs, dbms, config
import time
from web3 import Web3


class Worker:
	def __init__(self, walletAddress, privateKey, blockchain="BSC"):
		self.walletAddress = walletAddress
		self.privateKey = privateKey
		self.blockchain = blockchain
		
	def balance(self, ticker):
		tokenAddress = dbms.getTokenAddress(ticker)
		tokenAddress = Web3.toChecksumAddress(tokenAddress)
		balance = manBlockchainFuncs.getBalance(tokenAddress, self.walletAddress)
		humanReadable = Web3.fromWei(balance, "Ether")
		return float(humanReadable)

	def customBalance(self, tokenAddress):
		tokenAddress = Web3.toChecksumAddress(tokenAddress)
		balance = manBlockchainFuncs.getBalance(tokenAddress, self.walletAddress)
		humanReadable = Web3.fromWei(balance, "ether")
		return humanReadable
	
	def pending(self):
		return manBlockchainFuncs.web3.eth.get_transaction_count(self.walletAddress, "pending") - manBlockchainFuncs.web3.eth.get_transaction_count(self.walletAddress) == 1

	def waitForTxnExecution(self):
		start = time.time()
		while True:
			if not self.pending():
				finish = time.time()
				break
		return finish - start

	def pairAvailable(self, tickerPair, exchange):
		symbol1, symbol2 = tickerPair.split("/")
		factoryAddress = dbms.getFactoryAddress(exchange)
		factoryABI = dbms.getFactoryABI(exchange)
		address1 = Web3.toChecksumAddress(dbms.getTokenAddress(symbol1))
		address2 = Web3.toChecksumAddress(dbms.getTokenAddress(symbol2))
		return manBlockchainFuncs.pairAvailable(factoryAddress, factoryABI, address1, address2)
	
	def price(self, tickerPair, exchange, amountIn = 1):
		router = dbms.getRouterAddress(exchange)
		abi = dbms.getRouterABI(exchange)
		symbol1, symbol2 = tickerPair.split("/")
		address1 = Web3.toChecksumAddress(dbms.getTokenAddress(symbol1))
		address2 = Web3.toChecksumAddress(dbms.getTokenAddress(symbol2))
		price = manBlockchainFuncs.getPrice(router, abi, address1, address2, amountIn)
		humanReadable = Web3.fromWei(price, "Ether")
		return float(humanReadable)

	def customPrice(self, address1, address2, exchange, amountIn = 1):
		router = dbms.getRouterAddress(exchange)
		abi = dbms.getRouterABI(exchange)
		address1 = Web3.toChecksumAddress(address1)
		address2 = Web3.toChecksumAddress(address2)
		amountIn = Web3.toWei(amountIn, "ether")
		price = manBlockchainFuncs.getPrice(router, abi, address1, address2, amountIn)
		humanReadable = Web3.fromWei(price, "Ether")
		return float(humanReadable)

	def estimatedPrice(self, tickerPair, amountIn = 1, exchange ="PancakeSwap (v2)"):
		factoryAddress = dbms.getFactoryAddress(exchange)
		factoryABI = dbms.getFactoryABI(exchange)
		pairABI = dbms.getPairABI(exchange)
		symbol1, symbol2 = tickerPair.split("/")
		address1 = Web3.toChecksumAddress(dbms.getTokenAddress(symbol1))
		address2 = Web3.toChecksumAddress(dbms.getTokenAddress(symbol2))
		price = manBlockchainFuncs.getEstimatedPrice(factoryAddress, factoryABI, pairABI, address1, address2, amountIn)
		humanReadable = price
		return float(humanReadable)
		
	def priceImpact(self, tickerPair, amountIn = 1, exchange ="PancakeSwap (v2)"):
		ePrice = self.price(tickerPair, 1, exchange) * amountIn
		rPrice = self.price(tickerPair, amountIn, exchange)
		priceImpact = round((ePrice - rPrice)/rPrice, 5)
		return priceImpact

	def approve(self, exchange, tokenAddress):
		router = dbms.getRouterAddress(exchange)
		tokenAddress = Web3.toChecksumAddress(tokenAddress)
		hash = manBlockchainFuncs.approveToken(self.walletAddress, self.privateKey, router, tokenAddress)
		return hash

	def swap(self, ticker, exchange, amountIn, gasPrice = 5):
		router = dbms.getRouterAddress(exchange)
		abi = dbms.getRouterABI(exchange)
		symbol1 , symbol2 = ticker.split("/")
		address1 = Web3.toChecksumAddress(dbms.getTokenAddress(symbol1))
		address2 = Web3.toChecksumAddress(dbms.getTokenAddress(symbol2))

		if amountIn == "max" and symbol1 != "WBNB":
			amountIn = self.balance(symbol1)
		else:
			amountIn = Web3.toWei(amountIn, "ether")
	
		if symbol1 == "WBNB":
			hash = manBlockchainFuncs.swapETHForToken(
				self.walletAddress,
				self.privateKey,
				router,
				abi,
				address1,
				address2,
				amountIn,
				gasPrice)
		elif symbol2 == "WBNB":
			hash = manBlockchainFuncs.swapTokenForETH(
				self.walletAddress,
				self.privateKey,
				router,
				abi,
				address1,
				address2,
				amountIn,
				gasPrice)
		else:
			hash = manBlockchainFuncs.swapTokenForToken(
				self.walletAddress,
				self.privateKey,
				router,
				abi,
				address1,
				address2,
				amountIn,
				gasPrice)
		return hash

	def customSwap(self, address1, address2, exchange, amountIn, gasPrice = 5):
		router = dbms.getRouterAddress(exchange)
		abi = dbms.getRouterABI(exchange)
		address1 = Web3.toChecksumAddress(address1)
		address2 = Web3.toChecksumAddress(address2)
		amountIn = Web3.toWei(amountIn, "ether")
		gasPrice = Web3.toWei(gasPrice, "gwei")
		WBNBAddress = Web3.toChecksumAddress(dbms.getTokenAddress("WBNB"))
		if address1 == WBNBAddress:
			hash = manBlockchainFuncs.swapETHForToken(
				self.walletAddress,
				self.privateKey,
				router,
				abi,
				address1,
				address2,
				amountIn,
				gasPrice)
		elif address2 == WBNBAddress:
			hash = manBlockchainFuncs.swapTokenForETH(
				self.walletAddress,
				self.privateKey,
				router,
				abi,
				address1,
				address2,
				amountIn,
				gasPrice)
		else:
			hash = manBlockchainFuncs.swapTokenForToken(
				self.walletAddress,
				self.privateKey,
				router,
				abi,
				address1,
				address2,
				amountIn,
				gasPrice)

		return hash
		
	def supportedExchanges(self):
		return dbms.getExchangeNames()
	
	def supportedTokens(self):
		return dbms.getTickers()
	
	def customTokenInfo(self, tokenAddress):
		tokenAddress = Web3.toChecksumAddress(tokenAddress)
		return manBlockchainFuncs.tokenSymbol(tokenAddress)
	
	def getTransactionStatus(self, hash):
		receipt = manBlockchainFuncs.web3.eth.get_transaction_receipt(hash)
		if receipt["status"] == 1:
			return True
		elif receipt["status"] == 0:
			return False
		
		
if __name__ == "__main__":	
	w = Worker(config.wallet, config.key)
	print(w.pending())