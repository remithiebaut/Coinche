# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 08:56:59 2019

@author: rthie
"""

import generical_function as generic
from GraphicCard import GraphicCard
from Hand import Hand
import graphic_constant as gconst
import pygame
import coinche_constant as const
import sys


class GraphicHand(Hand):

  def display(self,screen,player):
     """
     display the board of cards
     """
     inverse=False
     hidden=False
     if( player == "j2" )or( player == "j4") :
       inverse=True
     if( player != "j1") :
       hidden=True
     i=0
     for card in self.cards:
       card.play(screen=screen,new_position=gconst.area["cards"][player][i],inverse=inverse,hidden=hidden)
       i+=1
     pygame.display.flip()


  def choose_card(self,random=True):
    """
     choose and return a card
    """
    if not random : #Real player
      while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
              pygame.quit()
              sys.exit()

        for card in self.cards:
          mouse=pygame.mouse.get_pos()
          if mouse[0]>card.position[0] and mouse[0]<(card.position[0]+card.position[2]) and mouse[1]>card.position[1] and mouse[1]<(card.position[1]+card.position[3]):
            if  event.type == pygame.MOUSEBUTTONDOWN :
               if card.rest:
                 pygame.display.flip()
                 return card

    else: #BOT
      while True :
         card_position = generic.decision(liste_choix_possible=const.liste_entier32[:len(self.cards)], random=random, question="Quelle carte ? 1ère, 2ème ? ")
         card_position = int(card_position)-1
         if card_position<len(self.cards) :
             if self.cards[card_position].rest:
                 return self.cards[card_position]



  def play(self,screen,player,random,pli,hand): # could not work // dont play a empty hand with bots
    """
    play a graphic card
    """
    if screen!=None :
      screen.fill(gconst.GREEN,gconst.area[player])
      hand.display(screen=screen,player=player)
    card=hand.choose_card(random=random)
    choosen_color=self.play_card(pli=pli,choosen_card=card)
    if screen!=None :
      card.play(screen,new_position=gconst.area["cards"]["board"][player])
      self.display(screen=screen,player=player)
    return choosen_color




  def color(self, chosen_color):
    """
    return all the cards of a given color => it is now returning a Hand !!
    """
    cards_of_this_color=[]
    for card in self.cards:
        if card.color==chosen_color:
            cards_of_this_color.append(card)
    return GraphicHand(cards=cards_of_this_color, name =chosen_color)


def test_graphic_hand():
  cards=[]
  i=0
  for numero in const.liste_numero :
    cards.append(GraphicCard(numero,"carreau", position=gconst.area["cards"]["j1"][i]))
    i+=1
  myhand=GraphicHand(name="Pli",cards=cards)
  mypli=GraphicHand(name="Pli",cards=[])
  pygame.init()
  screen=pygame.display.set_mode(gconst.screen_size)

  screen.fill(gconst.GREEN)
  pygame.display.flip()


  while True:
    event = pygame.event.poll()


    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
            break

    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
      myhand.play(screen,player="j1",random=False,pli=mypli,hand=myhand)

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

    #if event.type == pygame.KEYDOWN and event.key == pygame.K_7 :
     #   screen.fill(gconst.BLUE,gconst.area["test"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_9 :
        screen.fill(gconst.GREEN)

    pygame.display.flip()

  pygame.quit()

if __name__=="__main__"   :




  print("ini and color_sort test")
  mycard1=GraphicCard("7","carreau")
  mycard2=GraphicCard("7","coeur")
  myhand2=GraphicHand(name="Pli",cards=[mycard2,mycard1])
  assert(myhand2.name=="Pli")
  assert(len(myhand2.cards)==2)
  assert(myhand2.points==0)
  assert(myhand2.rest["coeur"]==1)
  assert(myhand2.rest["cards"]==2)
  assert(myhand2.rest["pique"]==0)
  assert(myhand2.rest["trefle"]==0)
  assert(myhand2.rest["carreau"]==1)
  assert(myhand2.cards[0].color=="coeur")
  assert(myhand2.cards[1].color=="carreau")
  assert(len(myhand2.rest)==5)

  myhand=GraphicHand()
  assert(myhand.name=="Cards")
  assert(len(myhand.cards)==0)
  assert(myhand.points==0)
  for key in myhand.rest :
    assert(myhand.rest[key]==0)
  assert(len(myhand.rest)==5)

  print("Test OK")


  print("assert that test work correctly")

  myhand2.test("Pli",1,0,1,0,0)
  myhand.test()

  print("Test OK")


  print("add test")
  myhand += myhand2
  myhand.test(carreau=1,coeur=1)
  print("Test OK")


  print("reintialize test")
  myhand2.test(name="Pli")
  print("Test OK")


  print("count_points test")
  mycard1.points+=4
  mycard2.points+=5
  assert(myhand.count_points()==9==myhand.points)
  assert(myhand2.count_points()==myhand2.points==0)


  pioche =[ GraphicCard(i,j) for j in const.liste_couleur[:4] for i in const.liste_numero]
  mypioche=GraphicHand(cards=pioche,name="pioche")
  mypioche.test("pioche",8,8,8,8,0)
  print("Test OK")


  print("color test")
  mycolor={}
  for color in const.liste_couleur[:4]:
    mycolor[color]=mypioche.color(color)
  mycolor["coeur"].test(name="coeur",coeur=8)
  mycolor["pique"].test(name="pique",pique=8)
  mycolor["carreau"].test(name="carreau",carreau=8)
  mycolor["trefle"].test(name="trefle",trefle=8)


  print("Test OK")





  print("remove test")
  mypioche.cards[4].rest=False
  mypioche.remove_cards()
  mypioche.test("pioche",7,8,8,8)


  mypioche.cards[4].rest=False
  mypioche.cards[7].rest=False
  mypioche.remove_cards()
  mypioche.test("pioche",6,7,8,8)

  print("Test OK")


  print("choose test")

  for i in range (100):
    card=mypioche.choose_card()
    assert(card.rest)

  print("play_card test")
  mycard3=GraphicCard("7","carreau")
  mycard4=GraphicCard("7","coeur")
  mycard5=GraphicCard("As","coeur")
  mycard6=GraphicCard("R","pique")

  myhand3=GraphicHand(cards=[mycard3,mycard4])
  mypli=GraphicHand(name="Pli", cards=[mycard5,mycard6])

  myhand3.play_card(pli=mypli, choosen_card=mycard3)

  myhand3.test(coeur=1)

  mypli.test("Pli",coeur=1,pique=1,carreau=1)


  mypli.play_card(pli=myhand3, choosen_card=mycard3)
  mypli.play_card(pli=myhand3, choosen_card=mycard5)
  mypli.play_card(pli=myhand3, choosen_card=mycard6)

  myhand3.test(coeur=2,pique=1,carreau=1)
  mypli.test("Pli")

  print("Test OK")


  print("winner test")

  aspique=GraphicCard("As","pique")
  dpique=GraphicCard("D","pique")
  septcoeur=GraphicCard("7","coeur")

  mypli2=GraphicHand(name="Pli", sort=False, cards=[aspique,dpique,septcoeur])

  "atout coeur"
  septcoeur.atout=True
  aspique.value=8
  septcoeur.value=9
  dpique.value=5
  assert(mypli2.winner()==2)

  "atout pique"
  septcoeur.atout=False
  aspique.atout=True
  dpique.atout=True
  aspique.value=14
  septcoeur.value=1
  dpique.value=11

  assert(mypli2.winner()==0)

  "no atout pique first"
  septcoeur.atout=False
  aspique.atout=False
  dpique.atout=False
  aspique.value=8
  septcoeur.value=1
  dpique.value=5
  assert(mypli2.winner()==0)

  "no atout coeur first"
  mypli3=GraphicHand(name="Pli" ,sort=False, cards=[septcoeur,aspique,dpique])
  aspique.value=8
  septcoeur.value=1
  dpique.value=5
  assert(mypli3.winner()==0)

  print("Test OK")

  print("Check check_card")

  myhand=GraphicHand(cards=[aspique,dpique])
  assert(myhand.check_card(GraphicCard("As","pique")))
  assert(myhand.check_card(GraphicCard("D","pique")))
  assert(not myhand.check_card(GraphicCard("7","pique")))
  assert(myhand.check_card(aspique))
  assert(myhand.check_card(dpique))

  print("Test OK")

  print("graphic test")
  test_graphic_hand()
  print("No Test")

