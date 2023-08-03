
from cgitb import text
from unicodedata import name
import kivy
kivy.require('2.1.0')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.config import Config
from kivy.properties import ObjectProperty, StringProperty

import scryfall
import card
import dbAccess
import time

Config.set('graphics', 'resizable', True)

dbFile = "db\magicinfo.db"

class SrchBtn(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Search"

class HomePage(Screen):
    pass

class DeckPage(Screen):
    deck_names = ObjectProperty(None)
    selected_deck = StringProperty("None")

class ListAll(BoxLayout):
    sel_deck = StringProperty("None")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.fillWithDecks()

    def chngSel(self, instance):
        self.sel_deck = instance.text
        #print(f"{self.parent.parent.parent.selected_deck} called this and the value it {self.sel_deck}")

    def fillWithDecks(self):
        self.clear_widgets()
        conn = dbAccess.create_connection(dbFile)
        c = conn.cursor()
        decks = c.execute(''' SELECT name FROM decks ''')
        for deck in decks:
            item = Button(text=deck[0])
            item.bind(on_press=self.chngSel)
            self.add_widget(item)

    def fillWithCards(self):
        pass


class NewPage(Screen):

    def adddeck(self, instance):
        pass


class SearchPage(Screen):
    pass

class AdvSrchPage(Screen):
    pass

class ResultsPage(Screen):
    pass


# next steps: figure out how to serach for full art version of a card
# might be just need to add a flag
class TradePage(Screen):
    # considerations:
    '''
    1. add foil check box
    2. ditch single/buk entry
    3. have a button that promts for a path to a csv file that will handle bulk entry
    4.

    '''
    # test search suggestion:
    '''
    1. send a request for info every ~.5s
    2. make widget that gives suggestions like safran suggestion widget
    '''
    card_finder = scryfall.ScryFallAPI()
    keyPressTimer = 0

    ''' Sets the value of the text box with the selllected reccomendation
        1. instance: the button instance that was clicked
    '''
    def select_autofill(self, instance):
        self.ids.input.text = instance.text
        self.ids.recs.clear_widgets()

    '''Populates reccomendations in the suggestion box by accessing scryfall api'''
    def populate_suggestions(self):
        if len(self.ids.input.text) > 2 and \
            (time.time() - self.keyPressTimer) < 2:

            return

        sid = self.ids
        sid.recs.clear_widgets()
        jdata = self.card_finder.getAutoComplete(sid.input.text)

        for i in range(len(jdata["data"])):
            if i > 5:
                return
            btn = Button(text=jdata["data"][i])
            btn.bind(on_press=self.select_autofill)
            sid.recs.add_widget(btn)

    def add_to_collection(self):
        card_data = self.card_finder.search(self.ids.input.text)
        if card_data["total_cards"] < 1:
            pass
        # TODO: Figure out how to handle multiple cards being returned from search
        # look into: card ids, searching for frames, set
        # each card should have all the right foil price info so dont worry about searching that

        #new_card = card.Card()
        #print(new_card)
        # TO DO: add the card to the data base with concern to location(box/binder/deck)


class HomePage(Screen):
    pass

class DeckListPage(Screen):
    pass


class WindManager(ScreenManager):
    pass


class MagicTheGathered(App):
    prev_page = ObjectProperty(None)
    conn = dbAccess.create_connection(dbFile)
    c = conn.cursor()
    def on_pause(self):
        self.conn.commit()
        self.conn.close()

    def on_resume(self):
        self.conn = dbAccess.create_connection(dbFile)
        self.c = self.conn.cursor()
        return super().on_resume()

    def build(self):
        kv = Builder.load_file('magicthegathered.kv')
        return kv
        #build kv file with stuff I have

if __name__ == "__main__":
    # conn = dbAccess.create_connection(dbFile)
    # c = conn.cursor()
    # cn = 'Kaalia'
    # #c.execute(f'''CREATE TABLE {cn} (card_name text, univ_id integer, price real)''')
    # sql = f''' INSERT INTO {cn} (card_name, univ_id, price) VALUES (?, ?, ?)'''
    # vals = ('Avacyn, Angel of Hope, 0000, 40.99')
# c.execute(sql, vals)
    # vals = ('Aurelia, Warleader, 0000, 20.99')
    # c.execute(sql, vals)
    # card = Card.where(name="Avacyn").all()
    # for item in card:
    #     print(item.name, item.multiverse_id, item.image_url)


    # vals = ('Vito', 500.00, 4.7, 6, 4, 35, 27, 10, 7, 1, 1, 0, 1, 1, 0)
    # sql = ''' INSERT INTO decks (name,price,avg_cmc,instants,sorcerys,lands,creatures,artifacts,enchantments,plainswakers,white,blue,black,red,green)
    #         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    # c.execute(sql, vals)
    # conn.commit()
    # c.execute('''SELECT * FROM decks''')
    # rows = c.fetchall()
    # print(len(rows))
    # for i in rows:
    #     print(i)

    # conn.close()
    MagicTheGathered().run()



