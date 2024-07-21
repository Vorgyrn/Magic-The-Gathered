from dataclasses import dataclass
import os
from csv import reader
import Card
import dbAccess
import scryfall

@dataclass
class CardInfo:
   name: str
   setName: str
   setNum: int
   location: str 
   finish: str

class MassEntryFile:
    """This class handles the mass entry of cards to the database
    """    
    cards = []
    SFAPI = scryfall.ScryFallAPI()
    def __init__(self, path):
        self.setNewFile(path)
    
    def setNewFile(self, path):
        if not os.path.isfile(path):
            raise FileNotFoundError
        self.cards = []
        self.filename = path
        
    def respToCard(self, resp, info):
        # convert the card data gotten from the api
        # into a card data object
        card = Card.Card(resp, info.finish, info.location)
        return card
    
    def findCard(self, info:CardInfo):
        '''
        Use the card info given to request info on a card from ScryFallAPI.
        If data is returned add make card object and add return it. Otherwise,
        add let user know the card data was invalid/card doesnt exist
        '''
        srchStr = f"{info.name}+s:{info.setName}+cn:{info.setNum}"
        resp = self.SFAPI.search(srchStr)
        if len(resp) > 1:
            # think about what to do if multiple cards are returned
            print(f"{len(resp)} cards returned for {info.name}")
        if not resp:
            print("No card found for data", info)
        
        return Card.Card(resp[0],info.finish, info.location)
        
    def parseFile(self):
        ''' Pasre the file stored and query scryfallapi for card data. 
            Add the found cards to a list.                
        '''
        with open(self.filename, 'r') as infile:
            read = reader(infile)
            for line in read:
                self.cards.append(self.findCard(CardInfo(*line)))

if __name__ == "__main__":
    file = 'test.csv'
    mass = MassEntryFile(file)
    mass.parseFile()
    print(mass.cards)
