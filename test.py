import config, dbms, time, manBlockchainFuncs
from worker import Worker
from web3 import Web3
from colorama import init
init()
from colorama import Fore, Back, Style

'''
def viewPrices():
	for symbol in w.supportedTokens():
		for exchange in w.supportedExchanges():
			try:
				ticker = symbol+"/WBNB"
				if w.pairAvailable(ticker, exchange):
					print(Fore.GREEN+ exchange, ticker, w.price(ticker, 1, exchange))
				else:
					print(Fore.YELLOW+f"{ticker} pair is unavailable on {exchange}")
			except:
				print(Fore.RED+ "FATAL ERROR")
'''

#print(f'{w.priceImpact("Cake/WBNB", 1.01, "BabySwap")*100}%')
'''
def figurePriceImpact():
	import matplotlib.pyplot as plt
	import numpy as np

	#x = np.linspace(1, 1000, 1000)
	#y = w.priceImpact("WBNB/BUSD", x, "PancakeSwap (v2)")

	x = [i for i in range(1, 500)]
	y = []
	for amountIn in x:
		y.append(w.priceImpact("WINGS/BUSD", amountIn, "Jetswap")*100)
	fig, ax = plt.subplots()
	ax.plot(x, y)
	plt.show()
figurePriceImpact()

for exchangeName in dbms.getExchangeNames():
	router = dbms.getRouterAddress(exchangeName)
	ABI = dbms.getRouterABI(exchangeName)
	pancakeContract = manBlockchainFuncs.web3.eth.contract(address = router, abi = ABI)

	factoryAddress = pancakeContract.functions.factory().call()
	factoryABI = dbms.getFactoryABI(exchangeName)
	factoryContract = manBlockchainFuncs.web3.eth.contract(address = factoryAddress, abi = factoryABI)

	pairAddress = factoryContract.functions.getPair(
		manBlockchainFuncs.web3.toChecksumAddress(dbms.getTokenAddress("WBNB")),
		manBlockchainFuncs.web3.toChecksumAddress(dbms.getTokenAddress("BUSD"))).call()
	print(f"{exchangeName}: \n\tpair address: {pairAddress} \n\tURL for contract pair ABI: https://bscscan.com/address/{pairAddress}#code")
	
'''

from worker import Worker
	
trader = Worker(config.wallet, config.key)

print(trader.customBalance("0x64fcEBf1bb8F43FB19A971f687F83A1d9C1C1f11")*(10**15))

