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


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, table_name_info):
    try:
        c = conn.cursor()
        c.execute(table_name_info)
        c.close()
    except Error as e:
        print(e)
    
def add_deck_to_table(conn, vals):
    c = conn.cursor()
    sql = ''' INSERT INTO decks (name,price,avg_cmc,instants,sorcerys,lands,creatures,artifacts,enchantments,plainswakers,white,blue,black,red,green)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    c.execute(sql, vals)
    conn.commit()


def check_table(conn, table_name):
    c = conn.cursor()
    c.execute(f''' SELECT count(name) FROM sqlite_master WHERE 
        type='table' AND name= {table_name} ''')
    return c.fetchone()[0]

class database:
    def __init__(self):
        pass