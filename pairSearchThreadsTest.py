import config, dbms
import sqlite3
from threading import Thread

from requests.exceptions import HTTPError
from web3 import Web3


w3 = Web3(Web3.HTTPProvider(config.BSCTestnetURL))

exchangeName = "PancakeSwap"

factoryAddress = "0xB7926C0430Afb07AA7DEfDE6DA862aE0Bde767bc"
factoryABI = dbms.getFactoryABI(exchangeName)

factoryContract = w3.eth.contract(address = factoryAddress, abi = factoryABI)
max = factoryContract.functions.allPairsLength().call()

conn = sqlite3.connect("data/pairsThreadsTestNet.db", check_same_thread=False)
cur = conn.cursor()

cur.execute(f"SELECT id FROM 'pairs{exchangeName}' ORDER BY id DESC")
startIndex = 0
print(startIndex)

pairABI = dbms.getPairABI(exchangeName)
tokenABI = dbms.BEP20ABI

def getPairRecord(index, w3):
	pairAddress = factoryContract.functions.allPairs(index).call()
	pairContract = w3.eth.contract(address = pairAddress, abi = pairABI)

	token0Address = pairContract.functions.token0().call()
	token0Contract = w3.eth.contract(address = token0Address, abi = tokenABI)
	# symbol0 = token0Contract.functions.symbol().call()

	token1Address = pairContract.functions.token1().call()
	token1Contract = w3.eth.contract(address = token1Address, abi = tokenABI)
	# symbol1 = token1Contract.functions.symbol().call()

	args = (index, pairAddress, None, token0Address, None, token1Address, )
	return args


def sort(data):
	for j in range(len(data)-1):
		for i in range(len(data)-j-1):
			if data[i][0]>data[i+1][0]:
				data[i], data[i+1] = data[i+1], data[i]
	return data

data = []
def insertIntoDB(index):
	args = getPairRecord(index, w3)
	data.append(args)

indexList = [[]]
for i in range(1, 50001):
	indexList[len(indexList)-1].append(i)
	if len(indexList[len(indexList)-1])>=50:
		indexList.append([])

for i in indexList:
	print(i)

for indexes in indexList:
	threads = []
	for index in indexes:
		threads.append(Thread(target = insertIntoDB, args = (index, )))

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	data = sort(data)
	for i in data:
		print(*i)
	c=0
	for i in data:
		try:
			cur.execute(f"INSERT INTO 'pairs{exchangeName}' VALUES (?, ?, ?, ?, ?, ?)", i)
			c+=1
		except:
			print("COMMIT EXCEPTION")
	conn.commit()
	print(f"COMMITED {c}/50 "*10)
	data=[]


