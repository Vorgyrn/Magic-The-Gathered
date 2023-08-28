import sqlite3
from sqlite3 import Error

import os


deckFile = r'db\decklists.db'
magicInfo = r'db\magicinfo.db'

conn = None

try:
    #can pas :memory: to make the db be stored in ram
    conn = sqlite3.connect(deckFile)
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
    try:
        return sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return None

def create_table(conn, name, table_params):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE {0}({1}) '''.format(name, table_params))
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
    dbName = 'collection.db'

    def __init__(self):
        if not self.search_for_db():
            self. conn = self.create_new_db()
        else:
            self.conn = create_connection(f'db\\{self.dbName}')

    def search_for_db(self):
        if 'db' not in os.listdir(os.getcwd()):
            os.mkdir(os.getcwd()+'\\db')

        for file in os.listdir(os.getcwd()):
            if file.endswith('.db'):
                # not great idea to set to first file but oh well for now
                self.dbName = file.split(sep='\\')[-1]
                return True

        return False

    def create_new_db(self):
        '''
        a. if not then create collection.db
            I. create the following tables
                - collection
                - decklists '''
        # create the database file
        conn = create_connection(f'db\\{self.dbName}')

        # create table for all storage locations
        locations = 'Card Name, Universe ID, Foil, Alt Art, Price, Location'
        create_table(conn, 'Collection', locations)

        # create the table for decklists
        deck_params = 'Name, avg_cmc,instants,sorcerys,lands,creatures,artifacts,enchantments,plainswakers Card Count, Value, Archived'
        create_table(conn, 'Deck Lists', deck_params)

        return conn

    def new_deck(self, name):
        create_table(self.conn, name, 'Card Name, Universe ID')

    def add_card(self, card_info, location):
        pass

    def get_card(self):
        pass




if __name__ == "__main__":
    sql_query = """SELECT name FROM sqlite_master"""
    conn = create_connection(magicInfo)
    c = conn.cursor()
    c.execute(sql_query)
    print(c.fetchall())
