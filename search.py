import sqlite3, web3
import dbms, config

web3 = web3.Web3(web3.Web3.HTTPProvider(config.BSCTestnetURL))
print("Blockchain node connection:", web3.isConnected())

def searchPaths(maxLen: int, startToken: str, data: list):
    paths = []
    processedTokens = []
    path = [startToken]
    def go(path: list):
        for pair in data:
            end = path[len(path)-1]
            if end in pair and len(path)<maxLen-1:
                if end == pair[0] and pair[1] not in path:
                    processedTokens.append(pair[1])
                    paths.append(path + [pair[1]])
                    go(path + [pair[1]])
                elif pair[0] not in path:
                    processedTokens.append(pair[0])
                    paths.append(path + [pair[0]])
                    go(path + [pair[0]])
    newPaths = []
    go(path)
    for path in paths:
        if (path[len(path)-1], startToken) in data or (startToken, path[len(path)-1]) in data:
            newPaths.append(path+[startToken])
    return newPaths

print("DB uploading")
conn = sqlite3.connect("data\pairsTest.db")
cur = conn.cursor()
cur.execute("SELECT token0, token1 FROM 'pairs'")
data = cur.fetchall()[:500]

print("CIRCLE SEARCHING")
paths = searchPaths(15, "0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7", data)

print("PRICE CHECKING")
amountIn = 0.1
amountIn = web3.toWei(amountIn, "ether")
contract = web3.eth.contract(address = config.contractAddress, abi = dbms.contractABI)
for path in paths:
    pairPath = []
    for i in range(len(path)-1):
        token0 = path[i]
        token1 = path[i+1]
        cur.execute("SELECT pair FROM 'pairs' WHERE token0 IN (?, ?) AND token1 IN (?, ?)", (token0, token1, token0, token1))
        pairPath.append(cur.fetchone()[0])
    try:
        amountsOut = contract.functions.getAmountsOut(
                amountIn,
                path,
                pairPath,
                [25 for i in range(len(pairPath))]
            ).call()
    except:
        continue
    profit = amountsOut[len(amountsOut)-1]-amountIn
    print(f"{round(profit/amountIn, 4)*100}%", amountsOut[len(amountsOut)-1], path, pairPath)
