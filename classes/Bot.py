# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 22:34:33 2019

@author: rthie
"""
import coinche_constant as const
from Carte import Carte

class Bot:
  """
  AI Prototype which count cards each round
  """
  def __init__(self, level="beginner"):
    self.level=level
    self.counter={}
    for color in const.liste_couleur[:4] :
      self.counter[color]=0
        
  def count(self, card):
    """
    call after each card is played
    """
    self.counter[card.couleur]+=1
      
  def reinitialize(self):
    """
    reinitialize for a new round
    """
    for color in self.counter:
      self.counter[color]=0
      
      
      
class AdvancedBot(Bot):
  """
  AI Prototype who keep track of previous games
  """
  def __init__(self, level="beginner"):
    Bot.__init__(self,level)
    self.previouscounter={} #keep track of the last round
      
  def reinitialize(self):
    """
    reinitialize for a new round
    """
    for color in self.counter:
      self.previouscounter[color]=self.counter[color]
    Bot.reinitialize(self)
    
    
    
    
if __name__=="__main__" :
  carte={}
  for color in const.liste_couleur[:4] :
    carte[color]=Carte("As",color)
  bob = Bot()
  bob.count(carte[const.liste_couleur[3]])
  assert(bob.counter[const.liste_couleur[3]]==1)
  
  bill = AdvancedBot()
  bill.counter
  bill.count(carte[const.liste_couleur[2]])
  bill.count(carte[const.liste_couleur[1]])
  assert(bill.counter[const.liste_couleur[2]]==1)
  assert(bill.counter[const.liste_couleur[1]]==1)
  bill.reinitialize()
  assert(bill.previouscounter[const.liste_couleur[2]]==1)
  assert(bill.previouscounter[const.liste_couleur[1]]==1)
  bill.count(carte[const.liste_couleur[0]])
  assert(bill.counter[const.liste_couleur[0]]==1)
  assert(bill.previouscounter[const.liste_couleur[0]]==0)
  
  print("Test OK")
