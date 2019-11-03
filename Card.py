#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:48:39 2019

@author: rthiebaut
"""

class Card():
  """
  a game Card
  """
  def __init__(self, number, color, rest=True):
    self.number=number #prend la valeur none quand inexistant ACHANGER
    self.color=color
    self.rest=rest #utilisé seulement dans la distribution de cartes, lutiliser a la place de none ?
    self.value=None #order of power in teh actual announcing 16 atout Jacket and 1:7 normal
    self.atout=False
    self.points=0
    self.ID=number+color  #ATENTION SI Numero = None ne devrait pas marcher


  def reset(self):
    """
    reset cards values
    """
    self.rest=True #utilisé seulement dans la distribution de cartes, lutiliser a la place de none ?
    self.value=None #order of power in teh actual announcing 16 atout Jacket and 1:7 normal
    self.atout=False
    self.points=0

if __name__=="__main__"   :
  mycard=Card("7","Coeur")
  mycard2=Card("7","Coeur",False)
  assert(mycard2.number=="7")
  assert(mycard2.color=="Coeur")
  assert(mycard2.rest==False)
  assert(mycard.number=="7")
  assert(mycard.color=="Coeur")
  assert(mycard.rest==True)
  assert(mycard.value==None)
  assert(mycard.points==0)
  assert(mycard.ID=="7Coeur")

  print("test OK")
