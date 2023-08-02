
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
            item.bind(on_press= self.chngSel)
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

class TradePage(Screen):
    # considerations:
    '''
    1. start with add to collection have locations set up
    2. need a way to promt for if foil/

    '''
    # test search suggestion:
    '''
    1. send a request for info every ~.5s
    2. make widget that gives suggestions like safran suggestion widget
    '''
    card_finder = scryfall.ScryFallAPI()
    pass

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



