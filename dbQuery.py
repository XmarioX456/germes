from main import exchange
import sqlite3
with sqlite3.connect('base.db')as db:
    cursor = db.cursor()
    query = """ INSERT INTO exchange(name, blockchain) VALUES(?, ?) """
    for i in range(len(exchange)-1):
        cursor.execute(query, exchange[i])
    db.commit()