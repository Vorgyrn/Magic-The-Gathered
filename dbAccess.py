import sqlite3
from sqlite3 import Error

import apsw
import apsw.bestpractice

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

COLLECTION_TABLE='''
CREATE TABLE collection (
    collection_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cmc INTEGER NOT NULL,
    power INTEGER,
    toughness INTEGER,
    set TEXT NOT NULL,
    num INTEGER NOT NULL,
    type TEXT NOT NULL,
    oracle TEXT,
    rarity TEXT NOT NULL,
    price REAL NOT NULL,
    location INTEGER DEFAULT 1,
    loc_details TEXT,
    FOREIGN KEY (location)
    REFERENCES locations (location_id)
       ON UPDATE SET DEFAULT
       ON DELETE SET DEFAULT
    image BLOB,
)
'''
DECKLIST_TABLE='''
CREATE TABLE REPLACE_ME (
    name TEXT NOT NULL,
    FOREIGN KEY (name)
    REFERENCES collection (name)
       ON UPDATE SET CASCADE
       ON DELETE SET RESTRICT
    cmc INTEGER NOT NULL,
    FOREIGN KEY (cmc)
    REFERENCES collection (cmc)
       ON UPDATE SET CASCADE
       ON DELETE SET RESTRICT
    power INTEGER,
    FOREIGN KEY (power)
    REFERENCES collection (power)
       ON UPDATE SET CASCADE
       ON DELETE SET RESTRICT
    toughness INTEGER,
    FOREIGN KEY (toughness)
    REFERENCES collection (toughness)
       ON UPDATE SET CASCADE
       ON DELETE SET RESTRICT
    set TEXT NOT NULL,
    FOREIGN KEY (set)
    REFERENCES collection (set)
       ON UPDATE SET CASCADE
       ON DELETE SET RESTRICT
    num INTEGER NOT NULL,
    FOREIGN KEY (num)
    REFERENCES collection (num)
       ON UPDATE SET CASCADE
       ON DELETE SET RESTRICT
    type TEXT NOT NOT,
    FOREIGN KEY (type)
    REFERENCES collection (type)
       ON UPDATE SET CASCADE
       ON DELETE SET RESTRICT
    oracle TEXT,
    FOREIGN KEY (oracle)
    REFERENCES collection (oracle)
       ON UPDATE SET CASCADE
       ON DELETE SET RESTRICT
    rarity TEXT NOT NULL,
    FOREIGN KEY (rarity)
    REFERENCES collection (rarity)
       ON UPDATE SET CASCADE
       ON DELETE SET RESTRICT
    price REAL NOT NULL,
    FOREIGN KEY (price)
    REFERENCES collection (price)
       ON UPDATE SET CASCADE
       ON DELETE SET RESTRICT
    location INTEGER DEFAULT 1,
    FOREIGN KEY (location)
    REFERENCES locations (location_id)
       ON UPDATE SET DEFAULT
       ON DELETE SET DEFAULT
    count INTEGER DEFAULT 1     -- primarily for lands
)
'''
DECKS_TABLE='''
CREATE TABLE decks (
    name TEXT NOT NULL PRIMARY KEY,
    commander TEXT NOT NULL,
    avg_cmc REAL,
    instants INTEGER,
    sorcerys INTEGER,
    creatures INTEGER,
    enchanmtents INTEGER,
    artifacts INTEGER,
    plainswakers INTEGER,
    lands INTEGER,
    count INTEGER,
    location INTEGER DEFAULT 1,
    loc_details TEXT,
    FOREIGN KEY (location)
    REFERENCES locations (location_id)
       ON UPDATE SET DEFAULT
       ON DELETE SET DEFAULT
)
'''
LOCATIONS_TABLE='''
CREATE TABLE locations (
    location_id INTEGER PRIMARY KEY,
    location TEXT
)
'''

def search_for_db(path:str):
    """Search a folder for all .db files and return the paths in a list

        Args:
            path (str): path to search
        """
    dbs = []
    for file in os.listdir(path):
        if file.endswith('.db'):
           dbs.append(file)

    return dbs

class database:
    connection = None

    def __init__(self, path):
        self.dbPath = path

        if not self.validateDb():
            self.createNewDB()

        raise Exception(f"Invalid Path: Path provided is neither a valid file or folder.\n {self.dbPath}")

    def createNewDB(self):
        '''Create a new database with the path that was provided.'''

        # check if the given path is a dir
        if os.path.isdir(self.dbPath):
            os.mkdir(self.dbPath+'\\db\\')
            self.dbPath += '\\db\\collection.db'

        self.connection = apsw.Connection(self.dbPath)
        cursor = self.connection.cursor()
        cursor.execute(LOCATIONS_TABLE)
        cursor.execute(COLLECTION_TABLE)
        cursor.execute(DECKS_TABLE)

    def validateDb(self):
        '''Validate the provided path a properly formatted .db file.
        :return: True if the file is a properly formatted .db file, otherwise false.
        '''
        # validate path
        if os.path.isfile(self.dbPath):
            # check if its a .db file
            if '.db' not in self.dbPath:
                raise Exception(f"Invalid File Type: File path provided is not a .db file.\n {self.dbPath}")
        else:
            return False

        # test if the db contains the correct tables
        self.connection = apsw.Connection(self.dbPath)
        c = self.connection.cursor()
        reqs = ['locations', 'collection', 'decks']
        for req in reqs:
            tabeQuery=f"SELECT name FROM sqlite_master WHERE type='table' AND name='{req}';"
            value = c.execute(tabeQuery).fetchone()
            if value == []:
                raise Exception(f"Invalid Data Base: The data base provided is not formatted correctly.\n {self.dbPath}")
        return True

    def addLocation(self, location):
        query = "INSERT INTO locations values(?)"
        c = self.connection.cursor()
        c.execute(query, location)

    def addDeck(self, name:str, commander:str, location=1, location_details=''):
        '''Add a deck to the decks table'''
        cols = 'name, commander, location'
        vals = (name, commander, location)
        if len(location_details) > 0:
            cols += ', location_details'
            vals = (name, commander, location, location_details)
        query = f"INSERT INTO decks ({cols}) values(?)"
        c = self.connection.cursor()
        c.execute(query, vals)

    def add_card(self, card):
        """Adds a new card card to the collection, if a deck is specified add
        the card to the deck as well.

        Args:
            name (str): The exact name (not case sensative).
            set (str): set the card is in (either set code or full set name).
            num (int): The cards number within the set.
            count (int): Amount of cards owned
            location (str): place(s) the card(s) is stored, seperated by commas. If the location is a deck
            name, the card will be added to the deck list.
            foilType (str): foil, nonfoil, etched or glossy. Default to nonfoil
        """
        pass

    def add_to_deck(self, card):

        pass

    def remove_card(self, name:str, set:str, num:int, count:int, location:str, foilType='nonfoil'):
        """Remove a number of cards from the collection, if the count hits 0 the
        entire entry will be deleted.

        Args:
            name (str): name of card.
            set (str): set of card.
            num (int): set numbver of the card.
            count (int): number to be removed.
            location (str): locations to remove card from, will remove card
            from deck lists if the location is a deck list.
            foilType (str, optional): foil, nonfoil, etched or glossy. Defaults to 'nonfoil'.
        """
        pass

    def update_card(self, name):
        # is this neccessary?
        pass
    def get_card(self):
        pass

    def card_to_entry(self, card):
        pass

    def entry_to_card(self, entry):
        pass

    def get_card_locations(self):
        """get_card_locations:\n
        :return: all the locations cards are stored at
        """
        pass
if __name__ == "__main__":
    # sql_query = """SELECT name FROM sqlite_master"""
    sql_query = """SELECT * FROM Krenko""" #
    conn = create_connection(magicInfo)
    c = conn.cursor()
    c.execute(sql_query)
    print(c.fetchall())
