import sqlite3
from sqlite3 import Error

conn = None

try: 
    #can pas :memory: to make the db be stored in ram
    conn = sqlite3.connect(r'db\decklists.db')
    print(sqlite3.version)
except Error as e:
    print(e)
finally:
    if conn:
        conn.close()

