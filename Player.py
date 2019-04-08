#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:45:53 2019

@author: rthiebaut
"""
from Hand import Hand
from Card import Card


class Player():
   def __init__(self, team_number, name, random, cards):

       self.name=name
       self.Hand=Hand(name=name, cards=cards) #bug with cards
       self.team=team_number
       self.plis=0
       self.generale=False #indicator of genereale annonce
       self.random=random

if __name__=="__main__"   :
  mycard1=Card("7","carreau")
  mycard2=Card("7","coeur")
  myplayer=Player(team_number=0, name="Bob", random = True, cards=[mycard1, mycard2])
  assert(myplayer.Hand.name==myplayer.name=="Bob")
  assert(len(myplayer.Hand.cards)==2)
  assert(myplayer.Hand.points==0)
  assert(myplayer.Hand.rest["coeur"]==1)
  assert(myplayer.Hand.rest["cards"]==2)
  assert(myplayer.Hand.rest["pique"]==0)
  assert(myplayer.Hand.rest["trefle"]==0)
  assert(myplayer.Hand.rest["carreau"]==1)
  assert(myplayer.Hand.cards[0].color=="coeur")
  assert(myplayer.Hand.cards[1].color=="carreau")
  assert(len(myplayer.Hand.rest)==5)
  assert(myplayer.plis==0)
  assert(myplayer.team==0)
  assert(myplayer.generale==False)
  assert(myplayer.random==True)

  myplayer=Player(team_number=0, name="Fred", random = True, cards=list())
  assert(myplayer.Hand.name==myplayer.name=="Fred")
  assert(len(myplayer.Hand.cards)==0)
  assert(myplayer.Hand.points==0)
  assert(myplayer.Hand.rest["coeur"]==0)
  assert(myplayer.Hand.rest["cards"]==0)
  assert(myplayer.Hand.rest["pique"]==0)
  assert(myplayer.Hand.rest["trefle"]==0)
  assert(myplayer.Hand.rest["carreau"]==0)
  assert(len(myplayer.Hand.rest)==5)
  assert(myplayer.plis==0)
  assert(myplayer.team==0)
  assert(myplayer.generale==False)
  assert(myplayer.random==True)




  print("test OK")


