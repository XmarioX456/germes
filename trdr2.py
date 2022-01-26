import config
import dbms
from time import time

class ViewerEth:

    def __init__(self, provider):
        from web3 import Web3
        self.w3 = Web3(Web3.HTTPProvider(provider))

    def txnStatus(self, hash):
        receipt = self.w3.eth.get_transaction_receipt(hash)
        return bool(receipt["status"])

    def balance(self, address):
        return self.w3.fromWei(self.w3.eth.get_balance(address), "ether")

    def balanceOf(self, address, contractAddress):
        contract = self.w3.eth.contract(address=contractAddress, abi=dbms.BEP20ABI)
        balance = self.w3.fromWei(contract.functions.balanceOf(address).call(), "ether")
        return balance

class Trdr2(ViewerEth):

    def __init__(self, provider, WETH, wallet, key):
        from web3 import Web3
        self.w3 = Web3(Web3.HTTPProvider(provider))
        self.WETH = WETH
        self.wallet = wallet
        self.key = key

    def pending(self):
        return self.w3.eth.get_transaction_count(self.wallet, "pending") - self.w3.eth.get_transaction_count(self.wallet) == 1

    def waitForTxnExecution(self):
        start = time()
        while True:
            if not self.pending():
                finish = time()
                break
        return finish - start

    def thisBalance(self): #ETH balance
        return self.balance(self.wallet)

    def thisBalanceOf(self, contractAddress): #balance of some token
        return self.balanceOf(self.wallet, contractAddress)

    def signAndSend(self, txn):
        signedTxn = self.w3.eth.account.sign_transaction(txn, private_key=self.key)
        txToken = self.w3.eth.send_raw_transaction(signedTxn.rawTransaction)
        hash = self.w3.toHex(txToken)
        return hash

    def deposit(self, amount): #WETH => ETH
        amount = self.w3.toWei(amount, "ether")
        contract = self.w3.eth.contract(address=self.WETH, abi=dbms.WETHABI)
        txn = contract.functions.deposit().buildTransaction(
            {
                "gas" : 3000000,
                "gasPrice": self.w3.toWei(10, "gwei"),
                "value": amount,
                "nonce": self.w3.eth.get_transaction_count(self.wallet)
            }
        )
        return self.signAndSend(txn)

    def withdraw(self, amount): #ETH => WETH
        amount = self.w3.toWei(amount, "ether")
        contract = self.w3.eth.contract(address=self.WETH, abi=dbms.WETHABI)
        txn = contract.functions.withdraw(
            amount
        ).buildTransaction(
            {
                "gas" : 300000,
                "gasPrice": self.w3.toWei(10, "gwei"),
                "nonce": self.w3.eth.get_transaction_count(self.wallet)
            }
        )
        return self.signAndSend(txn)

    def approve(self, address, spender, amount):
        amount = self.w3.toWei(amount, "ether")
        contract = self.w3.eth.contract(address=address, abi=dbms.BEP20ABI)
        txn = contract.functions.approve(
            spender,
            amount
        ).buildTransaction(
            {
                "gas" : 300000,
                "gasPrice": self.w3.toWei(10, "gwei"),
                "nonce": self.w3.eth.get_transaction_count(self.wallet)
            }
        )
        return self.signAndSend(txn)

    def amountsOut(self, amountIn, path, pairPath):
        fees = [2 for i in range(len(pairPath))]
        amountIn = self.w3.toWei(amountIn, "ether")
        contract = self.w3.eth.contract(address=config.contractAddress, abi=dbms.contractABI)
        amountsOut = contract.functions.getAmountsOut(
            amountIn,
            path,
            pairPath,
            fees
        ).call()
        return amountsOut

    def vSwap(self, amountIn, amountOutMin, path, pairPath):
        fees = [2 for i in range(len(pairPath))]
        amountIn = self.w3.toWei(amountIn, "ether")
        amountOutMin = self.w3.toWei(amountOutMin, "ether")
        contract = self.w3.eth.contract(address=config.contractAddress, abi=dbms.contractABI)
        txn = contract.functions.vSwap(
            amountIn,
            amountOutMin,
            path,
            pairPath,
            fees,
            self.wallet,
	        (int(time()) + 1000)
        ).buildTransaction(
            {
                "gas" : 10000000,
                "gasPrice": self.w3.toWei(10, "gwei"),
                "nonce": self.w3.eth.get_transaction_count(self.wallet)
                #"value": amountIn
            }
        )
        return self.signAndSend(txn)

if __name__ == "__main__":
    trd = Trdr2(config.BSCTestnetURL, "0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd", config.wallet2, config.key2)
    circle = dbms.circles[1]
    hash = trd.approve(trd.WETH, config.contractAddress, trd.thisBalanceOf(trd.WETH))
    print(hash)
    trd.waitForTxnExecution()
    print(trd.txnStatus(hash))
    hash = trd.vSwap(0.000100001, 0.00000000000001, circle.path, circle.pairPaths)
    print(hash)
    trd.waitForTxnExecution()
    print(trd.txnStatus(hash))
