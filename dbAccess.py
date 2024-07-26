from Card import Card
from MassEntry import MassEntryFile

import apsw
import apsw.bestpractice

apsw.bestpractice.apply(apsw.bestpractice.recommended)

TYPES = ['Creature', "Planeswalker", "Artifact", "Land", "Battle", "Instant", 'Sorcery']
import os
from pdb import set_trace

def check_table(conn, table_name):
    c = conn.cursor()
    c.execute(f''' SELECT count(name) FROM sqlite_master WHERE
        type='table' AND name= {table_name} ''')
    return c.fetchone()[0]

COLLECTION_TABLE='''
CREATE TABLE collection (
    collection_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cmc INTEGER NOT NULL,
    mana_cost TEXT,
    set_name TEXT NOT NULL,
    set_num INTEGER NOT NULL,
    type TEXT NOT NULL,
    rarity TEXT NOT NULL,
    price REAL NOT NULL,
    power INTEGER,
    toughness INTEGER,
    oracle TEXT,
    location INTEGER DEFAULT 1,
    loc_details TEXT,
    foil INTEGER DEFAULT 0,
    etched INTEGER DEFAULT 0,
    FOREIGN KEY (location)
    REFERENCES locations(location_id)
       ON UPDATE SET DEFAULT
       ON DELETE SET DEFAULT
)
'''
DECKLIST_TABLE='''
CREATE TABLE REPLACE_ME_list (
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
    set_name TEXT NOT NULL,
    FOREIGN KEY (set_name)
    REFERENCES collection (set_name)
       ON UPDATE SET CASCADE
       ON DELETE SET RESTRICT
    set_num INTEGER NOT NULL,
    FOREIGN KEY (set_num)
    REFERENCES collection (set_num)
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
    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

def cardToEntry(card:Card, location=1):
        pnt = []
        if card.isCreature():
            pnt = [card.power, card.toughness]
        ret = (card.name, card.cmc, card.mana_cost, card.set_name, card.set_num,
               card.type_line, card.rarity, card.price, *pnt, card.oracle_text,
               location, card.loc_dets, int(card.foil), int(card.etched))
        return ret

class database:
    connection = None

    def __init__(self, path=''):
        self.dbPath = path

        if not self.validateDb():
            self.createNewDB()

    def createNewDB(self):
        '''Create a new database with the path that was provided.'''
        # check if the given path is a dir
        if not os.path.isdir(self.dbPath):
            folder='db\\'
            if not os.path.exists(folder):
                os.mkdir(folder)
            self.dbPath = folder +'collection.db'
        else:
            self.dbPath = 'collection.db'

        self.connection = apsw.Connection(self.dbPath)
        self.connection.pragma("foreign_keys", True)
        cursor = self.connection.cursor()
        cursor.execute(LOCATIONS_TABLE)
        self.addLocation('unknown')
        cursor.execute(COLLECTION_TABLE)
        cursor.execute(DECKS_TABLE)

        print("Created new database at:", self.dbPath)

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


        self.connection = apsw.Connection(self.dbPath)
        check = self.connection.pragma("integrity_check")
        if check != "ok":
            raise Exception("Database Integrity Error:", check)

        # test if the db contains the correct tables
        c = self.connection.cursor()
        reqs = ['locations', 'collection', 'decks']
        for req in reqs:
            tabeQuery=f"SELECT name FROM sqlite_master WHERE type='table' AND name='{req}';"
            value = c.execute(tabeQuery).fetchone()
            if value == []:
                raise Exception(f"Invalid DataBase: The database provided is not formatted correctly.\n {self.dbPath}")

        print("Database at: ", self.dbPath, "VALIDATED")
        return True

    def getLocationID(self, location):
        query = f"SELECT location_id FROM locations WHERE location = '{location}';"
        c = self.connection.cursor()
        res, = c.execute(query).fetchone()
        return res

    def addLocation(self, location):
        query = "INSERT INTO locations (location) VALUES (?);"
        c = self.connection.cursor()
        c.execute(query, (location,))

    def getLocations(self):
        """getLocations:\n
        :return: all the locations cards are stored at
        """
        query = 'SELECT * FROM locations;'
        c = self.connection.cursor()
        results = c.execute(query).fetchall()
        return results

    def addDeck(self, name:str, commander:str, location=1, location_details=''):
        '''Add a deck to the decks table'''
        
        if name in self.getDeckNames():
            print(f"A deck with name {name} already exists.")
            return
        
        cols = 'name, commander, location'
        vals = (name, commander, location)
        qs = '?,?,?'
        if len(location_details) > 0:
            cols += ', location_details'
            vals = (name, commander, location, location_details)
            qs += ',?'
        query = f"INSERT INTO decks ({cols}) values ({qs})"
        c = self.connection.cursor()
        c.execute(query, vals)
        c.execute(DECKLIST_TABLE.replace('REPLACE_ME', name))        

    def getDeckList(self, deckName):
        query = f'''SELECT * FROM {deckName}_list'''
        c = self.connection.cursor()
        res = c.execute(query)
        return res

    def addCard(self, card:Card):
        """Adds a new card card to the collection, if a deck is specified add
        the card to the deck as well.

        Args:
            card: the card to add to the collection
        """
        # check if new location is needed
        locs = [loc[1] for loc in self.getLocations()]
        if card.location not in locs:
            self.addLocation(card.location)

        loc_id = self.getLocationID(card.location)
        pnt = ""
        if card.isCreature():
            pnt = 'power, toughness,'

        info = cardToEntry(card, loc_id)
        qs = ','.join(['?' for i in range(len(info))])
        query = f"""INSERT INTO collection
                        (name, cmc, mana_cost, set_name, set_num, type,
                        rarity, price, {pnt}oracle, location, loc_details,
                        foil, etched)
                        VALUES
                        ({qs})"""
        c = self.connection.cursor()
        c.execute(query, card.toDBFormat(loc_id))

    def addToDeck(self, card:Card):
        # make a trigger or a call back to do averages of cmc and stuff
        pass

    def bulkAdd(self, path):
        # accept a csv file
        # read over csv file and add each card to collection and deck
        [self.addCard(card) for card in MassEntryFile(path).getCards()]

    def remove_card(self, card:Card):
        """Remove a number of cards from the collection, if the count hits 0 the
        entire entry will be deleted.

        Args:
            card (Card): card object
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
    
    def getDeckNames(self):
        c = self.connection.cursor()
        query = f'''SELECT name FROM decks'''
        res = c.execute(query).fetchall()
        return [r[0] for r in res]
    
    def getDeckInfo(self, deckName):
        
        # this currently looks at info from the view. I will be moving on from
        #  views and instead implimenting the deck_list table the way I already
        #  designed it. THis time it will have 
        c = self.connection.cursor()
        query = f'''SELECT * FROM {deckName}'''
        res = c.execute(query).fetchall()
        for r in res:
            print(r)
            
    # temporary testing funcS
    def seeViews(self):
        #query = '''SELECT name FROM sqlite_master WHERE type = "view" ''' #and sql LIKE "%_tablename_%"
        query = '''PRAGMA table_list'''
        c = self.connection.cursor()
        res = c.execute(query).fetchall()
        for r in res:
            print(r)
        
    def seeTables(self):
        query = """SELECT name FROM sqlite_master WHERE type = 'table'""" #and sql LIKE "%_tablename_%"
        c = self.connection.cursor()
        res = c.execute(query).fetchall()
        for r in res:
            print(r)
            
    def tableContents(self, tableName):
        # locations collection decks
        query = f"""SELECT * FROM {tableName}""" #and sql LIKE "%_tablename_%"
        c = self.connection.cursor()
        res = c.execute(query).fetchall()
        for r in res:
            print(r)

    def seeCollection(self):
        query = "SELECT * from collection;"
        c = self.connection.cursor()
        res = c.execute(query).fetchall()
        for r in res:
            print(r)

if __name__ == "__main__":
    a = 'rb1'
    '''data={'name':'Kaalia', 'cmc':4, 'mana_cost':'1{b}{w}{r}', 'set_name':'c14',
          'collector_number':1, 'type_line':'Lengendary Creature - Human Cleric',
          'rarity':'mythic', 'power':2, 'toughness':2, 'oracle_text':"Flying\n When this creature attacks put a demon, dragon, or angel onto the battlefield tapped and attacking.",
          'colors':'WBR', 'prices':{'usd_foil':40.00, 'usd_etched':50.90, 'usd':20.69},
          'image_uris':'none'} 
    data={'name':'Avacyn', 'cmc':8, 'mana_cost':'5{w}{w}{w}', 'set_name':'AVC',
          'collector_number':1, 'type_line':'Lengendary Creature - Angel',
          'rarity':'mythic', 'power':8, 'toughness':8, 'oracle_text':"Flying\nIndestructible\nOther permanents yoc control have indestructible",
          'colors':'W', 'prices':{'usd_foil':40.00, 'usd_etched':50.90, 'usd':30.00},
          'image_uris':'none'} '''
    #kaalia = Card(data, 'foil', a)
    #kaalia.fromJson(data, location=a)
    db = database('db\\collection.db')
    print(db.getDeckNames())
    #print(db.getLocations())
    #db.addCard(kaalia)
    deck = ['WHite', 'Avacyn']
    db.addDeck(*deck)
    db.seeTables()
    # db.tableContents('decks')
    #db.tableContents('locations')
    db.seeCollection()
    #db.getDeckInfo('DDA')
    #lit = db.getDeckList('DDA')
    #for l in lit: print(l)
    #db.seeCollection()


