#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:45:54 2019

@author: rthiebaut
"""
from Player import Player
from Hand import Hand
from Card import Card


class Team():
  def __init__(self, team_name, team_number, j1_name, j1_random, j1_cards, j2_name, j2_random, j2_cards ):

   self.name=team_name
   self.number=team_number
   self.players=[Player(team_number=team_number, name=j1_name, random=j1_random, cards=j1_cards),
                 Player(team_number=team_number, name=j2_name, random=j2_random, cards=j2_cards)]
   self.pli=Hand(name=( "plis de l'equipe " + str(team_number) ), sort=False) #a reinitialiser
   self.bet=None  # == mise

  def reinitialize(self, j1_cards, j2_cards):
    """
    reintialize for a new round with the drawing cards
    """
    self.players[0].reinitialize(cards=j1_cards)
    self.players[1].reinitialize(cards=j2_cards)
    self.pli.reinitialize()
    self.bet=None
    
  def test(self, name1, name2, team_name, team_number=0, bet=None,
           coeur1=0, pique1=0, carreau1=0, trefle1=0, points1=0, generale1=False, plis1=0, random1=True,
           coeur2=0, pique2=0, carreau2=0, trefle2=0, points2=0, generale2=False, plis2=0, random2=True,
           pli_coeur=0, pli_pique=0, pli_carreau=0, pli_trefle=0, pli_points=0,
            ):
    """
    assert that the team is as it should be. It is set by default as empty
    """
    self.pli.test(name=( "plis de l'equipe " + str(team_number) ),
                  coeur=pli_coeur,pique=pli_pique,carreau=pli_carreau,trefle=pli_trefle,points=pli_points)
    
    self.players[0].test(name=name1,coeur=coeur1,pique=pique1,carreau=carreau1,trefle=trefle1,points=points1,
                         team_number=team_number, generale=generale1, plis=plis1, random=random1)
    
    self.players[1].test(name=name2,coeur=coeur2,pique=pique2,carreau=carreau2,trefle=trefle2,points=points2,
                         team_number=team_number, generale=generale2, plis=plis2, random=random2)

    assert self.name==team_name
    assert self.number==team_number
    assert self.bet==bet






if __name__=="__main__"   :

  mycard1=Card("7","carreau")
  mycard2=Card("7","coeur")
  myteam=Team(team_name="Les winners", team_number=0, j1_name="Bob", j1_random = True, j1_cards=[mycard1, mycard2],
              j2_name="Fred", j2_random = True, j2_cards=[])

  assert(myteam.number==0)
  assert(myteam.name=="Les winners")
  assert(myteam.bet==None)# == mise


  "pli test"
  assert(myteam.pli.name=="plis de l'equipe 0")
  assert(len(myteam.pli.cards)==0)
  assert(myteam.pli.points==0)
  assert(myteam.pli.rest["coeur"]==0)
  assert(myteam.pli.rest["cards"]==0)
  assert(myteam.pli.rest["pique"]==0)
  assert(myteam.pli.rest["trefle"]==0)
  assert(myteam.pli.rest["carreau"]==0)
  assert(len(myteam.pli.rest)==5)


  "player 1 test"
  assert(myteam.players[0].Hand.name==myteam.players[0].name=="Bob")
  assert(len(myteam.players[0].Hand.cards)==2)
  assert(myteam.players[0].Hand.points==0)
  assert(myteam.players[0].Hand.rest["coeur"]==1)
  assert(myteam.players[0].Hand.rest["cards"]==2)
  assert(myteam.players[0].Hand.rest["pique"]==0)
  assert(myteam.players[0].Hand.rest["trefle"]==0)
  assert(myteam.players[0].Hand.rest["carreau"]==1)
  assert(myteam.players[0].Hand.cards[0].color=="coeur")
  assert(myteam.players[0].Hand.cards[1].color=="carreau")
  assert(len(myteam.players[0].Hand.rest)==5)
  assert(myteam.players[0].plis==0)
  assert(myteam.players[0].team==0)
  assert(myteam.players[0].generale==False)
  assert(myteam.players[0].random==True)


  "player 2 test"

  assert(myteam.players[1].Hand.name==myteam.players[1].name=="Fred")
  assert(len(myteam.players[1].Hand.cards)==0)
  assert(myteam.players[1].Hand.points==0)
  assert(myteam.players[1].Hand.rest["coeur"]==0)
  assert(myteam.players[1].Hand.rest["cards"]==0)
  assert(myteam.players[1].Hand.rest["pique"]==0)
  assert(myteam.players[1].Hand.rest["trefle"]==0)
  assert(myteam.players[1].Hand.rest["carreau"]==0)
  assert(len(myteam.players[1].Hand.rest)==5)
  assert(myteam.players[1].plis==0)
  assert(myteam.players[1].team==0)
  assert(myteam.players[1].generale==False)
  assert(myteam.players[1].random==True)
  
  
  print("check  test")
  
  myteam.test(name1="Bob",name2="Fred", team_name="Les winners",carreau1=1,coeur1=1)
  
  print("test ok")

  myteam.players[1].reinitialize(cards=[mycard1, mycard2])
  
  
  
  assert(myteam.players[1].Hand.name==myteam.players[1].name=="Fred")
  assert(len(myteam.players[1].Hand.cards)==2)
  assert(myteam.players[1].Hand.points==0)
  assert(myteam.players[1].Hand.rest["coeur"]==1)
  assert(myteam.players[1].Hand.rest["cards"]==2)
  assert(myteam.players[1].Hand.rest["pique"]==0)
  assert(myteam.players[1].Hand.rest["trefle"]==0)
  assert(myteam.players[1].Hand.rest["carreau"]==1)
  assert(len(myteam.players[1].Hand.rest)==5)
  assert(myteam.players[1].plis==0)
  assert(myteam.players[1].team==0)
  assert(myteam.players[1].generale==False)
  assert(myteam.players[1].random==True)

  myteam.test(name1="Bob",name2="Fred", team_name="Les winners",carreau1=1,coeur1=1,coeur2=1,carreau2=1)

  print("test reinitialize")

  myteam.reinitialize(j1_cards=[mycard1, mycard2], j2_cards=[])
  myteam.pli.test("plis de l'equipe 0")


  assert(myteam.players[0].Hand.name==myteam.players[0].name=="Bob")
  myteam.players[0].Hand.test("Bob",coeur=1,carreau=1)
  assert(myteam.players[0].plis==0)
  assert(myteam.players[0].team==0)
  assert(myteam.players[0].generale==False)
  assert(myteam.players[0].random==True)


  assert(myteam.players[1].Hand.name==myteam.players[1].name=="Fred")
  myteam.players[1].Hand.test("Fred")
  assert(myteam.players[1].plis==0)
  assert(myteam.players[1].team==0)
  assert(myteam.players[1].generale==False)
  assert(myteam.players[1].random==True)

  myteam.test(name1="Bob",name2="Fred", team_name="Les winners",carreau1=1,coeur1=1)



  print("test OK")
