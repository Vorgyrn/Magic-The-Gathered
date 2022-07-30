
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


class HomePage(Screen):
    '''def __init__(self,**kwargs):
        super(HomePage, self).__init__()
        self.name = kwargs['name']
        homeGrid = GridLayout(cols=1, rows=3)

        logo = BoxLayout()

        btns = BoxLayout(spacing=15, orientation='horizontal')
        space = BoxLayout()
        decklists = Button(text='Deck Lists')
        newdecks = Button(text='New Deck')
        btns.add_widget(decklists)
        btns.add_widget(space)
        btns.add_widget(newdecks)

        moreBtns = BoxLayout(spacing=15, orientation='horizontal')
        allCards = Button(text="Full Collection")
        trade = Button(text="Enter Trade")
        updatedDB = Button(text="Update Card Data")
        moreBtns.add_widget(allCards)
        moreBtns.add_widget(trade)
        moreBtns.add_widget(updatedDB)

        homeGrid.add_widget(logo)
        homeGrid.add_widget(btns)
        homeGrid.add_widget(moreBtns)
        self.add_widget(homeGrid)'''
    pass


class DeckPage(Screen):
    '''def __init__(self,**kwargs):
        super(DeckPage, self).__init__()
        self.name = kwargs['name']
        base = GridLayout(rows=3, cols=3)
        usedSpaces = 0
        spaces = [BoxLayout() for i in range(10)]
        backBtn = Button(text='Back to home')
        #backBtn.bind(on_press=self.go_home)
        spaces[0].add_widget(backBtn)'''
    pass

class NewPage(Screen):
    pass

class CollectionPage(Screen):
    pass

class TradePage(Screen):
    pass

class HomePage(Screen):
    pass



class WindManager(ScreenManager):
    pass

kv = Builder.load_file('magicthegathered.kv')

class MagicTheGathered(App):
    def build(self):
        #sm = ScreenManager()
        #sm.add_widget(HomePage(name='Home'))
        #return sm
        return kv
        #build kv file with stuff I have

if __name__ == "__main__":
    MagicTheGathered().run()