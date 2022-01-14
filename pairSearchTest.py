from web3 import Web3
from time import sleep
import config
import json
import dbms
import sqlite3
web3 = Web3(Web3.HTTPProvider(config.BSCTestnetURL))
print("Blockchain node connection:", web3.isConnected())

with open("data/package.json", "r") as file:
	contractABI = json.load(file)
with open("data/1.json", "r") as file:
	contractABIToken = json.load(file)
with open("data/2.txt", "r") as file:
	index = file.read()
	print(index)
pairABI = dbms.getPairABI("PancakeSwap (v2)")


address = "0xB7926C0430Afb07AA7DEfDE6DA862aE0Bde767bc"
contract = web3.eth.contract(address=address, abi=contractABI)

allPairNum = contract.functions.allPairsLength().call()
print(allPairNum)

query = "INSERT INTO pairs(id, pair, symbol0, token0, symbol1, token1) VALUES(?, ?, ?, ?, ?, ?)"
conn = sqlite3.connect("data/pairsTest.db")
cur = conn.cursor()
for i in range(int(index), allPairNum):
	with open("data/2.txt", "w") as file:
		file.write(str(i))
		file.close()
	try:
		txn = contract.functions.allPairs(i).call()
	
		contractPair = web3.eth.contract(address=web3.toChecksumAddress(txn), abi=pairABI)
	
		token0 = contractPair.functions.token0().call()
		contractToken0 = web3.eth.contract(address=web3.toChecksumAddress(token0), abi=contractABIToken)
		token0Symbol = contractToken0.functions.symbol().call()
	
		token1 = contractPair.functions.token1().call()
		contractToken1 = web3.eth.contract(address=web3.toChecksumAddress(token1), abi=contractABIToken)
		token1Symbol = contractToken1.functions.symbol().call()
	
		temp = (i, txn, token0Symbol, token0, token1Symbol, token1)
		cur.execute(f"SELECT * FROM pairs WHERE id = {i}")
		if cur.fetchone() != []:
			cur.execute(query, temp)
			conn.commit()
			print(f"Done {i}/{allPairNum}")
	except:
		print("Error by web. Waiting 60s...")
		sleep(60)
		i -= 1
print("finish")
# txn = contract.functions.multiswap(
# 	web3.toWei(0.01, "ether"),
# 	[
# 		"0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd",
# 		"0x7728B1aB9ab8ec52a392FC3FEF5b8A396F2317d1",
# 		"0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd",
#
# 	]
# ).buildTransaction(
# 			{
# 				'from': config.wallet3,
# 				'value': 10000000000000000,
# 				'gasLimit': 50000000,
# 				'gasPrice': web3.toWei(10, "gwei"),
# 				'nonce': web3.eth.get_transaction_count(config.wallet3)
# 				}
# 			)
#
# signedTxn = web3.eth.account.sign_transaction(txn, config.key3)
# txToken = web3.eth.send_raw_transaction(signedTxn.rawTransaction)
# print(web3.toHex(txToken))
