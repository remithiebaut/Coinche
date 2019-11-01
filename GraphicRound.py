#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:30:05 2019

@author: rthiebaut
"""
import coinche_constant as const
import generical_function as generic
import graphic_constant as gconst
from generical_function import get_mouse,graphic_yesorno,draw_text
import pygame


from GraphicPlayer import GraphicPlayer
from GraphicHand import GraphicHand
from GraphicCard import GraphicCard
from GraphicTeam import GraphicTeam
from Round import Round

import random as rand


class GraphicRound(Round):
  """
  One Round of coinche
  """
  def __init__(self, team1_name, j1_name, j1_random, j3_name, j3_random,
               team2_name, j2_name, j2_random, j4_name, j4_random ,
               number,pioche, hidden=False,): # e1 et e2 inutiles

   self.number=number
   self.atout=None
   self.coinche=False #indicator of coinche
   self.surcoinche=False
   self.pli=GraphicHand(name="Pli in progress",cards=[], sort=False)
   assert(self.pli.rest["cards"]==0)
   self.pioche=pioche
   if self.number==0 :
     players=self.random_draw()
   else :
     players=self.classic_draw()
   self.teams=[GraphicTeam(team_name=team1_name, team_number=0,
                    j1_name=j1_name, j1_random=j1_random, j1_cards=players[0],
                    j2_name=j3_name, j2_random=j3_random, j2_cards=players[2]),
               GraphicTeam(team_name=team2_name, team_number=1,
                    j1_name=j2_name, j1_random=j2_random, j1_cards=players[1],
                    j2_name=j4_name, j2_random=j4_random, j2_cards=players[3])]
   self.hidden=hidden





  def graphic_choose_atout(self,screen,annonce_actuelle):
      screen.fill(gconst.PURPLE,gconst.area["middle"])
      for announce in gconst.area["announce"]["value"]:
        draw_text(screen,announce,gconst.area["announce"]["value"][announce])
      for announce in gconst.area["announce"]["color"]:
        draw_text(screen,announce,gconst.area["announce"]["color"][announce])
      color=self.choose_announce(screen,"color")
      while True :
        bet = self.choose_announce(screen,"value")
        annonce_voulue=const.liste_annonce.index(bet)
        if annonce_voulue>annonce_actuelle :
            annonce_actuelle=annonce_voulue
            break

      screen.fill(gconst.GREEN,gconst.area["middle"])
      draw_text(screen,bet + " " + color,gconst.area["middle"])
      return (color,bet,annonce_actuelle)



  def choose_announce(self,screen,value_or_color):
    assert((value_or_color=="color") or (value_or_color=="value"))
    confirmation_zone=None
    while True :
      event = pygame.event.poll()
      if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
        break
      for announce in gconst.area["announce"][value_or_color]:
        if gconst.get_mouse(gconst.area["announce"][value_or_color][announce]):
          if  event.type == pygame.MOUSEBUTTONDOWN :
            if confirmation_zone==gconst.area["announce"][value_or_color][announce] : #second click
              screen.fill(gconst.RED,gconst.area["announce"][value_or_color][announce])
              draw_text(screen,announce,gconst.area["announce"][value_or_color][announce])
              pygame.display.flip()
              return announce
            else :
              if confirmation_zone!=None : # already click elsewhere
                screen.fill(gconst.PURPLE,confirmation_zone)
                draw_text(screen,confirmed_announce,confirmation_zone)
              screen.fill(gconst.YELLOW,gconst.area["announce"][value_or_color][announce])
              draw_text(screen,announce,gconst.area["announce"][value_or_color][announce])
              pygame.display.flip()
              confirmation_zone=gconst.area["announce"][value_or_color][announce] #click once to highligth, click twice to confirm
              confirmed_announce=announce


  def coincher(self,screen,player,bet):
    """
    make a turn of coince take as argument the player who just bet
    """
    self.teams[player.team].bet=bet #fixe la bet de lteam attention bet est un char
    self.teams[(player.team+1)%2].bet=None
    if bet == "generale":
      player.generale=True

    for coincheur in self.teams[(player.team+1)%2].players:
        if not self.coinche :
          #BOT
          if coincheur.random:
            self.coinche=generic.decision(random=coincheur.random, question='coincher sur {} {} ?'.format(bet,self.atout), ouverte=False)
          #PLAYER
          else :
            self.coinche= graphic_yesorno(screen,question="coincher ?",question_surface=gconst.area["choice"]["question"],
                                   yes_surface=gconst.area["choice"]["yes"],no_surface=gconst.area["choice"]["no"])
          if self.coinche:


             if not self.hidden : #GRAPHIC
               draw_text(screen,' {} coinche sur {} {} !'.format(coincheur.name,bet,self.atout),gconst.area["middle"])



             for surcoincheur in self.teams[player.team].players:

               if not self.surcoinche :
                 #BOT
                 if coincheur.random:
                   self.surcoinche=generic.decision(random=surcoincheur.random, question='surcoincher sur {} {} ?'.format(bet,self.atout), ouverte=False)
                 #PLAYER
                 else :
                   self.surcoinche= graphic_yesorno(screen,question="surcoincher ?",question_surface=gconst.area["choice"]["question"],
                                           yes_surface=gconst.area["choice"]["yes"],no_surface=gconst.area["choice"]["no"])
                 if self.surcoinche :
                     if not self.hidden : #GRAPHIC
                       draw_text(screen,' {} surcoinche sur {} {} !'.format(surcoincheur.name,bet,self.atout),gconst.area["middle"])



  def choose_atout(self,screen,background_color="GREEN"): # pensez a display avant surcoinche empecher danooncer 170 180 tout atout sans atout
    """
    select the atout and return true if someone didnt pass his turn
    """
    j=self.shortkey()
    screen.fill(gconst.PURPLE,gconst.area["middle"])
    bet=0
    annonce_actuelle=-1
    turn=0
    while turn!=4 and bet!='generale' and not self.coinche:
      for player in j:
        if turn==4 or bet=='generale' or self.coinche:
          break
        else:

          #BOT
          if player.random:
            if not generic.decision(random=player.random, question='annoncer', ouverte=False): #local variable referenced before assignment
              turn+=1
            else :
              turn=1

              self.atout=generic.decision(const.liste_couleur, random=player.random, question ="Choisir la couleur d'atout : %s " % const.liste_couleur)

              while True :
                bet = generic.decision(const.liste_annonce, random=player.random, question="Choisir la hauteur d'annonce : %s " % const.liste_annonce )
                annonce_voulue=const.liste_annonce.index(bet)
                if annonce_voulue>annonce_actuelle :
                    annonce_actuelle=annonce_voulue

                    if not self.hidden :  #GRAPHIC
                      print(' {} prend à {} {} !'.format(player.name,bet,self.atout))

                    break
              self.coincher(screen,player,bet)

          #PLAYER
          else :
            if not graphic_yesorno(screen,question="annoncer ?",question_surface=gconst.area["choice"]["question"],
                                   yes_surface=gconst.area["choice"]["yes"],no_surface=gconst.area["choice"]["no"]) :
              turn+=1
            else:
              turn=1
              self.atout,bet,annonce_actuelle=self.graphic_choose_atout(screen,annonce_actuelle)
              self.coincher(screen,player,bet)


    if (self.atout==None):
          return False

    if not self.hidden :  #GRAPHIC
      for team in self.teams :
        if team.bet!=None:
          print("L'équipe '{}' a pris {} à {} !!!".format(team.name, team.bet, self.atout))

    return True


def test_init():
  myround = GraphicRound( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                   team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                   hidden=False,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),number=0)

  "check if pioche is empty"

  myround.pli.test("Pli in progress")

  "random draw cards assert that all cards are drawing"
  countinghand=GraphicHand()
  for team in myround.teams :
    for player in team.players :
      assert(len(player.Hand.cards)==player.Hand.rest["cards"]==8)
      countinghand+=player.Hand

  cards_of_pioche=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]

  countinghand.test("Cards",8,8,8,8)

  for i in range(32):
    assert(countinghand.cards[i] not in (countinghand.cards[:i]+countinghand.cards[i+1:])) #check for double
    assert(countinghand.check_card(cards_of_pioche[i]))




def test_choose_atout(): #random test
  pygame.init()
  screen=pygame.display.set_mode(gconst.screen_size)

  screen.fill(gconst.GREEN)
  pygame.display.flip()
  for i in range( 500):
    myround = GraphicRound( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                     team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                     hidden=True,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),number=0)
    myround.choose_atout(screen)
  pygame.quit()

def test_cards_update(): #random test
  pygame.init()
  screen=pygame.display.set_mode(gconst.screen_size)

  screen.fill(gconst.GREEN)
  pygame.display.flip()
  for i in range( 500):
    myround = GraphicRound( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                   team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                   hidden=True,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),number=0)
    if myround.choose_atout(screen) :
      myround.cards_update()
  pygame.quit()


def test_play_pli(hidden=True): #•fonctionne
  pygame.init()
  screen=pygame.display.set_mode(gconst.screen_size)

  screen.fill(gconst.GREEN)
  pygame.display.flip()
  for i in range( 500):
    myround = GraphicRound( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                   team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                   hidden=True,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),number=0)
    if myround.choose_atout(screen) :
      myround.cards_update()
      players=myround.shortkey()
      for i in range(8):
        players=myround.play_pli(pli_number=i,players=players)
  pygame.quit()






def test_classic_drawing():
  myround = GraphicRound( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                 team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                 hidden=True,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),number=0)
  myround.pioche = GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]])
  players=myround.classic_draw()

  "check if pioche is empty"

  myround.pli.test("Pli in progress")

  "check drawing"

  "the order should be"
  "7 8 9 coeur d r 10 pique 7 8 trefle"
  "v d r coeur As pique 7 8 carreau 9 v trefle"
  "10 as coeur 7 pique 9 v d carreau d r trefle"
  "8 9 v pique r 10 as carreau 10 as trefle"
  players_cards=[]
  players_cards.append([GraphicCard("7", "coeur"),GraphicCard("8", "coeur"),GraphicCard("9", "coeur"),
           GraphicCard("D", "pique"),GraphicCard("R", "pique"),GraphicCard("10", "pique"),
           GraphicCard("7", "trefle"),GraphicCard("8", "trefle")])

  players_cards.append([GraphicCard("V", "coeur"),GraphicCard("D", "coeur"),GraphicCard("R", "coeur"),
           GraphicCard("As", "pique"),GraphicCard("7", "carreau"),GraphicCard("8", "carreau"),
           GraphicCard("9", "trefle"),GraphicCard("V", "trefle")])

  players_cards.append([GraphicCard("10", "coeur"),GraphicCard("As", "coeur"),GraphicCard("7", "pique"),
           GraphicCard("9", "carreau"),GraphicCard("V", "carreau"),GraphicCard("D", "carreau"),
           GraphicCard("D", "trefle"),GraphicCard("R", "trefle")])

  players_cards.append([GraphicCard("8", "pique"),GraphicCard("9", "pique"),GraphicCard("V", "pique"),
           GraphicCard("R", "carreau"),GraphicCard("10", "carreau"),GraphicCard("As", "carreau"),
           GraphicCard("10", "trefle"),GraphicCard("As", "trefle")])

  for p in range(4) :
    myhand=GraphicHand(cards=players[p])
    for i in range(8):
      assert(myhand.check_card(players_cards[p][i]))



"""
  print("cut test")

  for nb_of_try in range(100):

    myround.pioche = Hand(name="pioche",cards=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]])
    players=myround.classic_draw(cut=True)

    countinghand=Hand(cards= (players[0]+players[1]+players[2]+players[3]) )
    cards_of_pioche=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]

    countinghand.test("Cards",8,8,8,8)


    for i in range(32):
      assert(countinghand.cards[i] not in (countinghand.cards[:i]+countinghand.cards[i+1:])) #check for double
      assert(countinghand.check_card(cards_of_pioche[i]))

  print("test OK")



  print("shortcut test")

  p=myround.shortkey()
  p[1].Hand=Hand(cards=[Card("7","trefle")])
  assert(myround.teams[1].players[0].Hand.check_card(Card("7","trefle")))

  print("test OK")

"""










if __name__=="__main__"   :

#ALLOWED_CARD COULD NOT WORK

  generic.test("init and random draw",test_init)
  generic.test("choose_atout",test_choose_atout)
  generic.test("cards_update",test_cards_update)
  generic.test("play_pli",test_play_pli)
  generic.test("classic_drawing",test_classic_drawing)




