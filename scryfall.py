import requests
from time import sleep

from urllib.parse import quote

import Card

EQ='%3D'
CL='%3A'
PL='%2B'

#TO DO: abstract away the use of scryfall api json data format
#       and return the data in some form of object (card class etc)

class ScryFallAPI:
    base_url = "https://api.scryfall.com"
    search_url = base_url + "/cards/search?q="
    named_url = base_url + "/cards/named?"
    autocomplete_url = base_url + "/cards/autocomplete?"
    collection_url = base_url + "/cards/collection" #max of 75 cards per request
    

    def __init__(self) -> None:
        self.response = None

    '''
    searches for a named card from the scryfall api
    PARAMETERS:
    #1 name: the name of the card to search for
    #2 searchType: the search type to use,
        fuzzy for non exact names,
        exact for the exact (capitalization, spelling, punctuation)
    '''
    def getNamedCard(self, name:str, searchType="fuzzy"):
        #print(self.named_url + searchType + "=" + name)
        self.response = requests.get(self.named_url + searchType + "=" +  name) #"++" +

        if self.validateResponse():
            return self.response.json()
        else:
            return None

    def search(self, searchStr=""):
        
        self.response = requests.get(self.search_url+searchStr) # quote( #  + "q=unique:" + unique + "+"

        if self.validateResponse():
            return self.response.json()['data']
        
        return []

    # add option to return a specified number of suggestions
    def getAutoComplete(self, partialName:str):
        self.response = requests.get(self.autocomplete_url + "q=" + partialName)

        if self.validateResponse():
            return self.response.json()
        else:
            return None

    def getCollection(self, collection:str):
        pass

    def validateResponse(self):

        if self.response.status_code == 200:
            return True
        
        # Too many requests too fast slow down a second
        if self.response.status_code == 429:
            sleep(0.1)

        return False

if __name__ == "__main__":
    cardAccess = ScryFallAPI()
    option = input("Type 1 for card search, 2 for autofill or 3 for general surch: ")
    if option == "1":
        value = cardAccess.getNamedCard(input("Enter a card to search: "))
        if value != None:
            ''' for item in value:
                print(item, value[item]) '''
            new_card = Card.Card(value)
            print(new_card)

        else:
            if cardAccess.response.status_code == 400:
                print(cardAccess.response.json())
            else:
                print('error occurred', cardAccess.response.status_code)
    elif option == "2":
        value = cardAccess.getAutoComplete(input("Enter a string to suggest cards: "))
        if value != None:
            for item in value:
                print(item, value[item])

        else:
            print('error occurred', cardAccess.response.status_code)
    elif option == "3":
        value = cardAccess.search(input("Enter search string: "))
        cards = []
        if value != None:
            for item in value["data"]:

                #print(item)
                new_card = Card.Card(item)
                #pdb.set_trace()
                #print(new_card.price)
                cards.append(new_card)

        else:
            print("no luck")

    else:
        print("invalid input", option)




