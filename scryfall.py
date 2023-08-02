import requests
import card


#TO DO: abstract away the use of scryfall api json data format
#       and return the data in some form of object (card class etc)

class ScryFallAPI:
    search_url = "https://api.scryfall.com/cards/search?"
    named_url = "https://api.scryfall.com/cards/named?"
    autocomplete_url = "https://api.scryfall.com/cards/autocomplete?"
    collection_url = "https://api.scryfall.com/cards/collection" #max of 75 cards pre request

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
        self.response = requests.get(self.named_url + searchType + "=" + name)

        if self.validateResponse():
            return self.response.json()
        else:
            return None

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

        return False

if __name__ == "__main__":
    cardAccess = ScryFallAPI()
    option = input("Type 1 for card search or 2 for autofill: ")
    if option == "1":
        value = cardAccess.getNamedCard(input("Enter a card to search: "))
        if value != None:
            for item in value:
                print(item, value[item])
            new_card = card.Card(value)
            print(new_card.name, new_card.price)

        else:
            print('error occurred', cardAccess.response.status_code)
    elif option == "2":
        value = cardAccess.getAutoComplete(input("Enter a string to suggest cards: "))
        if value != None:
            for item in value:
                print(item, value[item])

        else:
            print('error occurred', cardAccess.response.status_code)
    else:
        print("invalid input", option)




