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

    
  def jouer_carte(self,pli,carte_choisie, screen, position_table= gconst.area["cards"]["board"]["j1"]):
   """
   joue la carte choisie et retourne sa couleur affiche cetteaction graphiquement
   """
   Hand.playcard(self,pli,carte_choisie)
   carte_choisie.jouer(screen, position_table= position_table)
   delete=self.cartes.index(carte_choisie)
   self.cartes=self.cartes[:delete]+self.cartes[delete+1:]
   
  def display(self,screen,player):
     """
     display the board of cards
     """
     i=0
     for card in self.cards:
      card.play(screen=screen,new_position=gconst.area["cards"][player][i])
      i+=1

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
                   return card

    else: #BOT
         card_position = generic.decision(liste_choix_possible=const.liste_entier32[:len(self.cards)], random=random, question="Quelle carte ? 1ère, 2ème ? ")
         card_position = int(card_position)-1
         if card_position<len(self.cards) :
             if self.cards[card_position].rest:
                 return self.cards[card_position]

"""
def test_graphic_hand():
  cards=[]
  i=0
  for numero in const.liste_numero :
    cards.append(GraphicCard(numero,"carreau", position=gconst.area["cards"]["j1"][i]))
    i+=1
  pygame.init() 
  screen=pygame.display.set_mode(gconst.screen_size)
  screen.fill(gconst.GREEN)                   
  while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
            break
    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT: #test
      screen.fill(gconst.YELLOW,(100,100,100,100))

    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        screen.fill(gconst.BLUE,(gconst.card_size[0],gconst.screen_size[1]-gconst.card_size[1],110,110))
        
    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        screen.fill(gconst.BLUE,gconst.grid[31][17])
        
        
        
    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
      
        afficher_cartes(screen, cartes)
        
    #if pygame.mouse.get_pos()[1]<(gconst.area["cards"]["J1"][1]):
    for card in cards:
      if pygame.mouse.get_pos()[0]>(card.position[0]) and pygame.mouse.get_pos()[0]<(card.position[0]+gconst.card_size[0]):
        if  event.type == pygame.MOUSEBUTTONDOWN : 
          
           card.play(screen)
           delete=cards.index(card)
           cards=cards[:delete]+cards[delete+1:]
            
             
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
        screen.fill(gconst.BLUE,gconst.area["test"])
        
    if event.type == pygame.KEYDOWN and event.key == pygame.K_9 :
        screen.fill(gconst.GREEN)
        
    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP7 :
        screen.fill(gconst.YELLOW,gconst.area["cards"]["J1"][7])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP0 :
        screen.fill(gconst.YELLOW,gconst.area["cards"]["J1"][0])
    pygame.display.flip()
    
  pygame.quit()
 """
 
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

  print("display test")
  mypioche.display(hidden=True)
  myhand.display(hidden=True)
  myhand2.display(hidden=True)
  print("No Test")

