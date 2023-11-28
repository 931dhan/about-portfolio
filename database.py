import sqlite3
import json

connection = sqlite3.connect('paper_trading.db')
# Connecting/Creating a paper trading database.
cursor = connection.cursor()
# A cursor is needed to execute code.

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        cash_balance TEXT,
        stocks TEXT,
        log TEXT
    )
''')



connection.commit()
# Commit saves the changes
connection.close()

