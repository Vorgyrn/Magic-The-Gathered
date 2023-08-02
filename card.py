

class Card:

    price = 0.0
    art_treatment = "Normal"
    # options: normal, showcase, extended

    finish = "none"
    # options none, foil, foil etch, other (step and conplete, surge, etc)

    def __init__(self, cardData, foil="none", art="normal"):
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
        if art == "normal":
            if foil == "foil":
                self.price = cardData["prices"]["usd_foil"]
            elif foil == "none":
                self.price = cardData["prices"]['usd_etched']
            else:
                self.price = cardData["prices"]['usd']

    def __repr__(self) -> str:
        return f"{self.name}: {self.type_line}, price: {self.price}"
