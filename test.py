from web3 import Web3
import config
import json
web3 = Web3(Web3.HTTPProvider(config.BSCTestnetURL))
print("Blockchain node connection:", web3.isConnected())

with open("data/customABI.json", "r") as file:
	contractABI = json.load(file)
address = "0xf0CE3cE63c336e89774c34c7e2c5197a7a27b980"
contract = web3.eth.contract(address = address, abi = contractABI)

txn = contract.functions.multiswap(
	web3.toWei(0.01, "ether"),
	[
		"0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd",
		"0x7728B1aB9ab8ec52a392FC3FEF5b8A396F2317d1",
		"0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd",

	]
).buildTransaction(
			{
				'from': config.wallet3,
				'value': 10000000000000000,
				'gasLimit': 50000000,
				'gasPrice': web3.toWei(10, "gwei"),
				'nonce': web3.eth.get_transaction_count(config.wallet3)
				}
			)

signedTxn = web3.eth.account.sign_transaction(txn, config.key3)
txToken = web3.eth.send_raw_transaction(signedTxn.rawTransaction)
print(web3.toHex(txToken))
