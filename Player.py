#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:45:53 2019

@author: rthiebaut
"""
from Hand import Hand
from Card import Card



class Player():
  """
  a game player
  """
  def __init__(self, team_number, name, random, cards):
    """
    team number =1 or 0 / random = T or F / cards is an array of cards
    """
    self.name=name
    self.Hand=Hand(name=name, cards=cards) #bug with cards
    self.team=team_number
    self.plis=0
    self.generale=False #indicator of genereale annonce
    self.random=random

  def reinitialize(self, cards):
    """
    reintialize player for a new round or a new game
    """
    self.Hand=Hand(name=self.name, cards=cards) #bug with cards
    self.plis=0
    self.generale=False #indicator of genereale annonce
    
  def test(self, name, coeur=0, pique=0, carreau=0, trefle=0, points=0,
           team_number=0, generale=False, plis=0, random=True):
    """
    assert that the player is as it should be. It is set by default as empty
    """
    self.Hand.test(name=name,coeur=coeur,pique=pique,carreau=carreau,trefle=trefle,points=points)
    assert self.name==name
    assert self.team==team_number
    assert self.plis==plis
    assert self.generale==generale #indicator of genereale annonce
    assert self.random==random



if __name__=="__main__"   :
  
  print ("check test")
  mycard1=Card("7","carreau")
  mycard2=Card("7","coeur")
  myplayer=Player(team_number=0, name="Bob", random = True, cards=[mycard1, mycard2])
  assert(myplayer.Hand.name==myplayer.name=="Bob")
  myplayer.test("Bob",coeur=1,carreau=1)
  print("Test OK")

  
  print("check color sort")
  assert(myplayer.Hand.cards[0].color=="coeur")
  assert(myplayer.Hand.cards[1].color=="carreau")

  myplayer2=Player(team_number=0, name="Fred", random = True, cards=list())

  myplayer2.test("Fred")


  print("Test OK")


  print("check reinitialize")
  myplayer2.reinitialize(cards=[mycard1, mycard2])
  myplayer2.test(name="Fred",coeur=1,carreau=1)


  print("Test OK")




