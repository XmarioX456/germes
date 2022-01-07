import sqlite3, json

with open("data/BEP20ABI.json", "r") as file:
	BEP20ABI = json.load(file)

with open("data/ERC20ABI.json", "r") as file:
	ERC20ABI = json.load(file)

conn = sqlite3.connect("data/base.db", check_same_thread=False)
cur = conn.cursor()


def getTokenAddress(ticker, tokenFormat="BEP20"):
	"""
	Gets *token address*:
	
	**Args:**
	`ticker` :ticker of token
	`tokenFormat` :format of token(default = "BEP20")

	**Returns:**
	`tokenAddress :str`
	"""
	if tokenFormat == "BEP20":
		cur.execute("SELECT address FROM coins_bep20 WHERE ticker = ?", (ticker,))
		return cur.fetchone()[0]
	elif tokenFormat == "ERC20":
		cur.execute("SELECT address from coins_erc20 WHERE ticker = ?", (ticker,))
		return cur.fetchone()[0]
	else:
		raise Exception("Unsupported token format")


def getTickers(tokenFormat="BEP20"):
	"""
	Gets *token tickers*:

	**Args:**

	`tokenFormat` :format of token(default = "BEP20")

	**Returns:**

	`tokenTickers :list`
	"""
	if tokenFormat == "ERC20":
		cur.execute("SELECT ticker from coins_erc20")
		return [i[0] for i in cur.fetchall()]
	elif tokenFormat == "BEP20":
		cur.execute("SELECT ticker from coins_bep20")
		return [i[0] for i in cur.fetchall()]
	else:
		raise Exception("Unsupported token format")


def getRouterAddressList():
	"""
	Gets *router addresses*:

	**Returns:**

	`routerAddresses :list`
	"""
	cur.execute(f"SELECT routerAddress from exchange")
	return [i[0] for i in cur.fetchall()]


def getExchangeNames():
	"""
	Gets *names of exchanges*:

	**Returns:**

	`exchangesNames :list`
	"""
	cur.execute("SELECT name FROM exchange")
	return [i[0] for i in cur.fetchall()]


def getRouterAddress(name):
	"""
	Gets *router address* of exchange:

	**Args:**
	
	`name` : name of exchange

	**Returns:**

	`routerAddress :str`
	"""
	cur.execute(f"SELECT routerAddress FROM exchange WHERE name = '{name}'")
	return cur.fetchone()[0]


def getRouterABI(name):
	"""
	Gets *router ABI* of exchange:

	**Args:**
	
	`name` : name of exchange

	**Returns:**

	`routerABI :str`
	"""
	cur.execute(f"SELECT routerABI from exchange WHERE name = '{name}'")
	return cur.fetchone()[0]


def getFactoryABI(name):
	"""
	Gets *factory ABI* of exchange:

	**Args:**

	`name` : name of exchange

	**Returns:**

	`factoryABI :str`
	"""
	cur.execute(f"SELECT factoryABI FROM exchange WHERE name = '{name}'")
	return cur.fetchone()[0]


def getFactoryAddress(name):
	"""
	Gets *factory address* of exchange:

	**Args:**

	`name` : name of exchange

	**Returns:**

	`factoryAddress :str`
	"""
	cur.execute(f"SELECT factoryAddress FROM exchange WHERE name = '{name}'")
	return cur.fetchone()[0]


def getPairABI(name):
	"""
	Gets *pair ABI* of exchange:

	**Args:**

	`name` : name of exchange

	**Returns:**

	`pairABI :str`
	"""
	cur.execute(f"SELECT pairABI FROM exchange WHERE name = '{name}'")
	return cur.fetchone()[0]


if __name__ == "__main__":
	eval(input("> "))
