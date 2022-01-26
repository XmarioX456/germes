import sqlite3
connPair = sqlite3.connect("data/pairs.db")
connTokens = sqlite3.connect("data/tokens.db")
curPair = connPair.cursor()
curTokens = connTokens.cursor()


def cheakAndAdd(newToken, tokenList):
	logic = False
	for j in tokenList:
		if j[0] == newToken[1]:
			logic = True
	if not logic:
		curTokens.execute("INSERT INTO tokens(symbol, address) VALUES(?,?)", newToken)
		connTokens.commit()
		print("Added")
	else:
		print("Is already in db")
		
		
for i in range(1, 86553):
	curPair.execute(f"SELECT symbol0, token0 FROM pairs WHERE id ={i}")
	temp = curPair.fetchone()
	print(temp)
	if temp == None:
		continue
		
	
	curTokens.execute("SELECT address FROM tokens")
	tempTokens = curTokens.fetchall()
	
	cheakAndAdd(temp, tempTokens)
	
	curPair.execute(f"SELECT symbol1, token1 FROM pairs WHERE id ={i}")
	temp = curPair.fetchone()

	curTokens.execute("SELECT address FROM tokens")
	tempTokens = curTokens.fetchall()
	cheakAndAdd(temp, tempTokens)