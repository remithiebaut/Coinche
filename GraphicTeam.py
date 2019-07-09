# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 09:56:35 2019

@author: rthie
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:45:54 2019

@author: rthiebaut
"""
from GraphicPlayer import GraphicPlayer
from GraphicHand import GraphicHand
from GraphicCard import GraphicCard
from Team import Team

class GraphicTeam(Team):
  def __init__(self, team_name, team_number, j1_name, j1_random, j1_cards, j2_name, j2_random, j2_cards ):

   self.name=team_name
   self.number=team_number
   self.players=[GraphicPlayer(team_number=team_number, name=j1_name, random=j1_random, cards=j1_cards, number=1+team_number),
                 GraphicPlayer(team_number=team_number, name=j2_name, random=j2_random, cards=j2_cards, number=3+team_number)]
   self.pli=GraphicHand(name=( "plis de l'equipe " + str(team_number) ),cards=[], sort=False) #a reinitialiser
   self.bet=None  # == mise


if __name__=="__main__"   :

  mycard1=GraphicCard("7","carreau")
  mycard2=GraphicCard("7","coeur")
  myteam=GraphicTeam(team_name="Les winners", team_number=0, j1_name="Bob", j1_random = True, j1_cards=[mycard1, mycard2],
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
  assert(myteam.players[0].number=="j1")



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
  assert(myteam.players[1].number=="j3")


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
