from web3 import Web3
import config
import json
web3 = Web3(Web3.HTTPProvider(config.BSCURL))
print("Blockchain node connection:", web3.isConnected())

with open("data/customABI.json", "r") as file:
	contractABI = json.load(file)
address = "0xfA403A78aC03084b89473ddD57c952CDdBc69C72"
contract = web3.eth.contract(address = address, abi = contractABI)

txn = contract.functions.swapBNBForToken(web3.toChecksumAddress("0xc98d826bc611ec1c54ec1674ed4bfce1aa9a5ddf")).buildTransaction(
			{
				'from': config.wallet3,
				'value': 1000000,
				'gasLimit': 50000000,
				'gasPrice': web3.toWei(10, "gwei"),
				'nonce': web3.eth.get_transaction_count(config.wallet3)
				}
			)

signedTxn = web3.eth.account.sign_transaction(txn, config.key3)
txToken = web3.eth.send_raw_transaction(signedTxn.rawTransaction)
print(web3.toHex(txToken))