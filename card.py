

class Card:

    foil = False
    art_treatment = "nomral"
    price = 0.0

    def __init__(self, cardData):
        self.name = cardData["name"]
        self.image_urls = cardData["image_uris"]
        self.mana_cost = cardData["mana_cost"]
        self.cmc = cardData["cmc"]
        self.type_line = cardData["type_line"]
        self.oracle_text = cardData["oracle_text"]
        self.power = cardData["power"]
        self.toughness = cardData["toughness"]
        self.colors = cardData["colors"]
        self.keywords = cardData["keywords"]
        self.set_name = cardData["set_name"]
        self.price = cardData["prices"]['usd']
