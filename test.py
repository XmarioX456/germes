import web3, config, time

import dbms

web3 = web3.Web3(web3.Web3.HTTPProvider(config.BSCTestnetURL))
print("Blockchain node connection:", web3.isConnected())

contract = web3.eth.contract(address = config.contractAddress, abi = dbms.contractABI)

txn = contract.functions.vSwap(
    web3.toWei(0.02, "ether"),
    web3.toWei(0.001, "ether"),
    ['0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd', '0xF9f93cF501BFaDB6494589Cb4b4C15dE49E85D0e', '0x7ef95a0FEE0Dd31b22626fA2e10Ee6A223F8a684', '0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7', '0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd'],
    ['0xDD4bDb1e31c6A5Edb0E96E61A05E2664bCDe578A', '0xbaE76CBa3eEB8a976683f4599041d83eBCbb96ca', '0x5126C1B8b4368c6F07292932451230Ba53a6eB7A', '0xe0e92035077c39594793e61802a350347c320cf2'],
    [25, 25, 25],
    config.wallet2,
	(int(time.time()) + 1000)
).buildTransaction(
    {
        "from" : config.wallet2,
        "gas" : 10000000,
        "gasPrice" : web3.toWei(10, "gwei"),
        "nonce" : web3.eth.get_transaction_count(config.wallet2)
    }
)
signed_txn = web3.eth.account.sign_transaction(txn, private_key=config.key2)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
txnHash = web3.toHex(tx_token)
print(txnHash)

