from web3 import Web3
import time, threading
import dbms
import config

web3 = Web3(Web3.HTTPProvider(config.BSCURL))
print("Blockchain node connection:", web3.isConnected())


def approveToken(walletAddress, privateKey, routerAddress, tokenAddress):
	tokenAddress = web3.toChecksumAddress(tokenAddress)
	tokenBalance = getBalance(tokenAddress, walletAddress)
	
	start = time.time()
	tokenContract = web3.eth.contract(tokenAddress, abi=dbms.BEP20ABI)
	approve = tokenContract.functions.approve(routerAddress, tokenBalance).buildTransaction(
			{
				'from': walletAddress,
				'gasPrice': web3.toWei('6', 'gwei'),
				'nonce': web3.eth.get_transaction_count(walletAddress),
				}
			)
	
	signed_txn = web3.eth.account.sign_transaction(approve, private_key=privateKey)
	tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
	approvingHex = web3.toHex(tx_token)

	return approvingHex


def pairAvailable(factoryAddress, factoryABI, tokenA_address, tokenB_address):
	factoryContract = web3.eth.contract(address=factoryAddress, abi=factoryABI)
	pairContract = factoryContract.functions.getPair(
			web3.toChecksumAddress(tokenA_address),
			web3.toChecksumAddress(tokenB_address)
			).call()
	return pairContract != "0x0000000000000000000000000000000000000000"


def getPrice(routerAddress, routerABI, tokenA_address, tokenB_address, amountIn):
	routerContract = web3.eth.contract(address=routerAddress, abi=routerABI)
	price = routerContract.functions.getAmountsOut(amountIn, [tokenA_address, tokenB_address]).call()
	normalizedPrice = web3.fromWei(price[1], 'Ether')
	return price[1]


def getEstimatedPrice(factoryAddress, factoryABI, pairABI, tokenA_address, tokenB_address, amountIn=1):
	factoryContract = web3.eth.contract(address=factoryAddress, abi=factoryABI)
	
	pairAddress = factoryContract.functions.getPair(
			web3.toChecksumAddress(tokenA_address),
			web3.toChecksumAddress(tokenB_address)
			).call()
	
	pairContract = web3.eth.contract(address=pairAddress, abi=pairABI)
	reserves = pairContract.functions.getReserves().call()
	
	if tokenA_address == pairContract.functions.token0().call():
		tokenA_index = 0
		tokenB_index = 1
	else:
		tokenA_index = 1
		tokenB_index = 0
	
	tokenA_reserve = float(reserves[tokenA_index])
	tokenA_reserve = web3.fromWei(tokenA_reserve, "ether")
	tokenB_reserve = float(reserves[tokenB_index])
	tokenB_reserve = web3.fromWei(tokenB_reserve, "ether")
	constantProduct = tokenA_reserve * tokenB_reserve
	newTokenB_reserve = constantProduct / (tokenA_reserve + amountIn)
	tokenB_out = tokenB_reserve - newTokenB_reserve
	return tokenB_out


def getBalance(tokenAddress, walletAddress):
	symbol = tokenSymbol(tokenAddress)
	
	if symbol == "WBNB":
		balance = web3.eth.get_balance(walletAddress)
	else:
		tokenContract = web3.eth.contract(address=tokenAddress, abi=dbms.BEP20ABI)
		balance = tokenContract.functions.balanceOf(walletAddress).call()
	
	return balance


def swapETHForToken(walletAddress, privateKey, routerAddress, routerABI, tokenToSell, tokenToBuy, amountIn, gasPrice):
	nonce = web3.eth.get_transaction_count(walletAddress)
	contract = web3.eth.contract(address=routerAddress, abi=routerABI)
	txn = contract.functions.swapExactETHForTokens(
			0,
			[tokenToSell, tokenToBuy],
			walletAddress,
			(int(time.time()) + 10000),
			).buildTransaction(
			{
				'from': walletAddress,
				'value': amountIn,
				'gas': 250000,
				'gasPrice': gasPrice,
				'nonce': nonce
				}
			)
	
	signedTxn = web3.eth.account.sign_transaction(txn, privateKey)
	txToken = web3.eth.send_raw_transaction(signedTxn.rawTransaction)
	return web3.toHex(txToken)


def swapTokenForToken(walletAddress, privateKey, routerAddress, routerABI, tokenToSell, tokenToBuy, amountIn, gasPrice):
	contract = web3.eth.contract(address=routerAddress, abi=routerABI)
	nonce = web3.eth.get_transaction_count(walletAddress)
	pancakeswap2_txn = contract.functions.swapExactTokensForTokens(
			amountIn,
			0,
			[tokenToSell, tokenToBuy],
			walletAddress,
			(int(time.time()) + 1000)
			).buildTransaction(
			{
				'from': walletAddress,
				'gasPrice': gasPrice,
				'nonce': nonce,
				}
			)
	
	signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=privateKey)
	tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
	return web3.toHex(tx_token)


def swapTokenForETH(walletAddress, privateKey, routerAddress, routerABI, tokenToSell, tokenToBuy, amountIn, gasPrice):
	contract = web3.eth.contract(address=routerAddress, abi=routerABI)
	nonce = web3.eth.get_transaction_count(walletAddress)
	pancakeswap2_txn = contract.functions.swapExactTokensForETH(
			amountIn,
			0,
			[tokenToSell, tokenToBuy],
			walletAddress,
			(int(time.time()) + 1000000)
			).buildTransaction(
			{
				'from': walletAddress,
				'gasPrice': gasPrice,
				'nonce': nonce,
				}
			)
	
	signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=privateKey)
	tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
	return web3.toHex(tx_token)


def tokenSymbol(tokenAddress):
	tokenContract = web3.eth.contract(address=tokenAddress, abi=dbms.BEP20ABI)
	symbol = tokenContract.functions.symbol().call()
	return symbol

def tokenDecimals(tokenAddress):
	contract = web3.eth.contract(address = tokenAddress, abi = dbms.BEP20ABI)
	decimals = contract.functions.decimals().call()
	return decimals

