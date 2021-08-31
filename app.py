from tkinter import Button, Label, Listbox, Spinbox
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.lang import Builder
from kivy.config import Config

Config.set('graphics', 'width', '605')
Config.set('graphics', 'height', '750')

class app(App):
    def build(self):
        return pannel()

class pannel(TabbedPanel):
    def __init__(self, **kwargs):
        super(pannel, self).__init__(**kwargs)
        tp = TabbedPanel()
        tp.default_tab_text = "Search" #this is the default tab but we changed it to search
        tp.default_tab_content = Label(text="Search Parameters:")
        #tp.default_tab_content = Spinbox(text="Name", values=("Card Type", "Subtype", "Color", "Set", "Rarity"))
        #tp.default_tab_content = Button(text="Search")
        dl = TabbedPanelHeader(text='Deck Lists')
        self.add_widget(dl)
        ac = TabbedPanelHeader(text='Add Card')
        self.add_widget(ac)
        rc = TabbedPanelHeader(text='Remove Card')
        self.add_widget(rc)
        nd = TabbedPanelHeader(text='New Deck')
        self.add_widget(nd)

        



if __name__ == '__main__':
    app().run()


'''Builder.load_string("""

<Test>:
    size_hint: 1, 1
    pos_hint: {'center_x': .5, 'center_y': .5}
    do_default_tab: False

    TabbedPanelItem:
        text: 'Search'
        BoxLayout:
        Label:
            text: 'First tab content area'

    TabbedPanelItem:
        text: 'Deck Lists'
        BoxLayout:
            Label:
                text: 'Second tab content area'
            Button:
                text: 'Button that does nothing'
    TabbedPanelItem:
        text: 'Add Card'
        RstDocument:
            text:
                '\\n'.join(("Hello world", "-----------",
                "You are in the third tab."))
    TabbedPanelItem:
        text: 'Remove Card'
    TabbedPanelItem:
        text: 'New Deck'
""")


class Test(TabbedPanel):
    pass


class TabbedPanelApp(App):
    def build(self):
        return Test()'''


