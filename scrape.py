from bs4 import BeautifulSoup as bs
import _pickle as pickle

class card():
   def __init__(self, cname, type, subtype, color, set, rarity, power, tough, cmc, cost):
       self.name=cname
       self.type=type
       self.subtype=subtype
       self.color=color
       self.set=set
       self.rarity=rarity
       self.power=power
       self.tough=tough
       self.cmc=cmc
       self.cost=cost

    
def scrape(target):

    pass
