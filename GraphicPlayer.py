# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 07:51:36 2019

@author: rthie
"""

from Player import Player
from GraphicHand import GraphicHand
import graphic_constant as gconst
import pygame
from GraphicCard import GraphicCard
import coinche_constant as const


class GraphicPlayer(Player):
  """
  a game player
  """
  def __init__(self, team_number, name, random, cards, number):
    """
    team number =1 or 0 / random = T or F / cards is an array of cards / number = 1 2 3 or 4
    """
    self.name=name
    self.Hand=GraphicHand(name=name, cards=cards) #bug with cards
    self.team=team_number
    self.plis=0
    self.generale=False #indicator of genereale annonce
    self.random=random
    self.number="j"+str(number)


  def reinitialize(self, cards):
    """
    reintialize player for a new round or a new game
    """
    self.Hand=GraphicHand(name=self.name, cards=cards) #bug with cards
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

  def display(self,screen):
     """
     display the board of cards
     """
     self.Hand.display(screen,self.number)

def test_graphic_player():
  cards1=[]
  cards2=[]
  cards3=[]
  cards4=[]
  mypli=GraphicHand(name="Pli",cards=[])


  i=0
  for numero in const.liste_numero :
    cards1.append(GraphicCard(numero,"carreau", position=gconst.area["cards"]["j1"][i]))
    cards2.append(GraphicCard(numero,"pique", position=gconst.area["cards"]["j3"][i]))
    cards3.append(GraphicCard(numero,"trefle", position=gconst.area["cards"]["j2"][i]))
    cards4.append(GraphicCard(numero,"carreau", position=gconst.area["cards"]["j4"][i]))

    i+=1
  myplayer1=GraphicPlayer(team_number=0, name="Bob", random = False, cards=cards1,number=1)
  myplayer2=GraphicPlayer(team_number=0, name="Fred", random = True, cards=cards2,number=3)
  myplayer3=GraphicPlayer(team_number=1, name="Fred", random = True, cards=cards3,number=2)
  myplayer4=GraphicPlayer(team_number=1, name="Fred", random = True, cards=cards4,number=4)


  pygame.init()
  screen=pygame.display.set_mode(gconst.screen_size)
  screen.fill(gconst.GREEN)
  pygame.display.flip()


  while True:
    event = pygame.event.poll()


    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
            break

    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
        myplayer1.Hand.play(screen,player=myplayer1.number,random=myplayer1.random,pli=mypli)



    if event.type == pygame.KEYDOWN and event.key == pygame.K_1 :
        screen.fill(gconst.BLUE,gconst.area["j1"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_2 :
        screen.fill(gconst.BLUE,gconst.area["j2"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_3 :
        screen.fill(gconst.BLUE,gconst.area["j3"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_4 :
        screen.fill(gconst.BLUE,gconst.area["j4"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_5 :
        screen.fill(gconst.BLUE,gconst.area["middle"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_6 :
        screen.fill(gconst.BLUE,gconst.area["points"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_7 :
      myplayer1.display(screen)
      myplayer2.display(screen)
      myplayer3.display(screen)
      myplayer4.display(screen)


    if event.type == pygame.KEYDOWN and event.key == pygame.K_9 :
        screen.fill(gconst.GREEN)

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP2 :
        myplayer2.Hand.play(screen,player=myplayer2.number,random=myplayer2.random,pli=mypli)



    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP3 :
        myplayer3.Hand.play(screen,player=myplayer3.number,random=myplayer3.random,pli=mypli)

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP4 :
        myplayer4.Hand.play(screen,player=myplayer4.number,random=myplayer4.random,pli=mypli)

    pygame.display.flip()

  pygame.quit()


if __name__=="__main__"   :

  print ("check test")
  mycard1=GraphicCard("7","carreau")
  mycard2=GraphicCard("7","coeur")
  myplayer=GraphicPlayer(team_number=0, name="Bob", random = True, cards=[mycard1, mycard2],number=1)
  assert(myplayer.Hand.name==myplayer.name=="Bob")
  myplayer.test("Bob",coeur=1,carreau=1)
  print("Test OK")


  print("check color sort")
  assert(myplayer.Hand.cards[0].color=="coeur")
  assert(myplayer.Hand.cards[1].color=="carreau")

  myplayer2=GraphicPlayer(team_number=0, name="Fred", random = True, cards=list(),number=3)

  myplayer2.test("Fred")


  print("Test OK")


  print("check reinitialize")
  myplayer2.reinitialize(cards=[mycard1, mycard2])
  myplayer2.test(name="Fred",coeur=1,carreau=1)


  print("Test OK")

  print("Test graphic")
  test_graphic_player()
  print("Test OK")


