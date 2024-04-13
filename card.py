

class Card:

    price = 0.0
    foil = 0
    etched = 0
    # options none, foil, foil etch, other (step and conplete, surge, etc)

    def __init__(self, cardData, finish='', location='', loc_dets=''):
        '''
        Args:
            cardData: the json retreived from scryfall for a card
            finish: foil or etched
            location: the name of the location the card is located at
            loc_dets: any more specifics of the location e.g. page 3 row 2 of red binder
        '''
        self.name = cardData["name"]
        self.cmc = cardData["cmc"]
        self.mana_cost = cardData["mana_cost"]
        self.set_name = cardData["set_name"]
        self.set_num = cardData["collector_number"]
        self.type_line = cardData["type_line"]
        self.rarity = cardData["rarity"]
        if "Creature" in self.type_line:
            self.power = cardData["power"]
            self.toughness = cardData["toughness"]
        self.oracle_text = cardData["oracle_text"]
        self.colors = cardData["colors"]
        self.location = location
        self.loc_dets = loc_dets

        if finish == "foil":
            self.foil = 1
            self.price = cardData["prices"]["usd_foil"]
        elif finish == "etched":
            self.etched = 1
            self.price = cardData["prices"]['usd_etched']
        else:
            self.price = cardData["prices"]['usd']

        self.image_urls = cardData["image_uris"]

    def __repr__(self) -> str:
        return f"{self.name}: {self.type_line}, price: {self.price}"
