import tkinter as tk
from tkinter import *
from tkinter import ttk

class Home(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Magic: The Gathered")
        self.master.geometry('600x600')
        self.createHomeWidgets()

    def createHomeWidgets(self):
        self.frame = Frame(width=200, height=200)
        self.frame.grid(column=1, row=1)
        self.left = Frame(width=190, height=200)
        self.left.grid(column=0, row=1)
        self.right = Frame(width=200, height=200)
        self.right.grid(column=2, row=1)
        self.topFrame = Frame(width=600, height=200)
        self.topFrame.grid(column=0, columnspan=3, row=0)

        self.srchBtn = Button(self.frame, text="Search", width=34, command=self.createSearch) #opens the search dialog
        self.srchBtn.grid(column=1, columnspan=2, padx=2,  row=2)

        self.deckBtn = Button(self.frame, text="Deck Lists", width= 34) #opens the deck dialog
        self.deckBtn.grid(column=1, columnspan=2, padx=2, pady=4, row=3)

        self.addBtn = Button(self.frame, text="Add Card", width=16, command=self.createNewCard) #opens the add card dialog
        self.addBtn.grid(column=1, row=4, padx=2, pady=4)

        self.removeBtn = Button(self.frame, text="Remove Card", width= 16) #opens the remove card dialog
        self.removeBtn.grid(column=2, row=4, padx=2, pady=4)

        self.newDeckBtn = Button(self.frame, text="Add New Deck", width= 34) #opens the new deck dialog
        self.newDeckBtn.grid(column=1, columnspan=2, padx=2, pady=4, row=5)
    
    def createSearch(self):
        self.top = Toplevel()
        self.top.geometry('500x500')
        self.top.title("Card Search")

        self.label = Label(self.top, text="Category:")
        self.label.grid(column=1, row=1)

        self.category = ttk.Combobox(self.top, width=20)
        self.category.grid(column=2, row=1, padx=3)
        self.category['values']= ("Name", "Card Type", "Subtype", "Color/s", "Set", "Rarity")

        self.entry = tk.Entry(self.top, textvariable=N, width=35)
        self.entry.grid(column=1, row=2)

        self.search = Button(self.top, text="Search", width=15)
        self.search.grid(column=2, row=2, padx=3, pady=3)
        
        self.clear = Button(self.top, text="Clear Search")
        self.clear["width"] = self.category["width"] = self.search["width"]
        self.clear.grid(column=2, row=3, padx=3)

    def createNewCard(self):
        self.top = Toplevel()
        self.top.geometry('600x600')
        self.top.title("Add New Card")

        self.main = Frame(self.top, width=200, height=200)
        self.main.grid(column=1, row=1)
        self.left = Frame(self.top, width=190, height=200)
        self.left.grid(column=0, row=1)
        self.right = Frame(width=200, height=200)
        self.right.grid(column=2, row=1)
        self.topFrame = Frame(self.top, width=600, height=200)
        self.topFrame.grid(column=0, columnspan=3, row=0)
        
        self.label = Label(self.main, text="Name of card:")
        self.label.grid(row=1, column=1)
        
        self.entry = Entry(self.main, text="Enter a card name...")
        self.entry.grid(row=1, column=2)

        self.button = Button(self.main, text="Add!")
        self.button.grid(row=1, column=3, padx=3)

root = tk.Tk()
app = Home(master=root)
app.mainloop()


