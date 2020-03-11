#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:30:05 2019

@author: rthiebaut
"""
import coinche_constant as const
import generical_function as generic
import graphic_constant as gconst
from generical_function import get_mouse,graphic_yesorno,draw_text,wait_or_pass
import pygame


from GraphicPlayer import GraphicPlayer
from GraphicHand import GraphicHand
from GraphicCard import GraphicCard
from GraphicTeam import GraphicTeam
from Round import Round

import random as rand
from Bot import Bot


class GraphicRound(Round):
  """
  One Round of coinche
  """
  def __init__(self, team1_name, j1_name, j1_random, j3_name, j3_random,
               team2_name, j2_name, j2_random, j4_name, j4_random ,
               number,pioche, hidden=False,screen=None): # e1 et e2 inutiles
    self.number=number
    self.atout=None
    self.coinche=False #indicator of coinche
    self.surcoinche=False
    self.pli=GraphicHand(name="Pli in progress",cards=[], sort=False)
    assert(self.pli.rest["cards"]==0)
    self.pioche=pioche

    if self.number==0 :
      players_cards=self.random_draw()
    else :
      players_cards=self.classic_draw()

    #bots creation
    # number_of_bots = j1_random+j2_random+j3_random+j4_random) #count number of bots
    self.bots={}
    if j1_random :
      self.bots[j1_name]=Bot(players_cards[0])
    if j2_random :
      self.bots[j2_name]=Bot(players_cards[1])
    if j3_random :
      self.bots[j3_name]=Bot(players_cards[2])
    if j4_random :
      self.bots[j4_name]=Bot(players_cards[3])

    self.teams=[GraphicTeam(team_name=team1_name, team_number=0,
                      j1_name=j1_name, j1_random=j1_random, j1_cards=players_cards[0],
                      j2_name=j3_name, j2_random=j3_random, j2_cards=players_cards[2]),
                 GraphicTeam(team_name=team2_name, team_number=1,
                      j1_name=j2_name, j1_random=j2_random, j1_cards=players_cards[1],
                      j2_name=j4_name, j2_random=j4_random, j2_cards=players_cards[3])]
    self.hidden=hidden
    self.screen=screen



  def display(self,screen):
    """
    display the four hands
    """

    if not self.hidden :
       for player in self.shortkey():
         player.display(screen)
         player.display(screen) # BIG PROBLEM HERE DONT GET WHY
    """
    self.teams[0].players[0].display(screen)
    graphic_yesorno(screen,question="montrer ?",question_surface=gconst.area["choice"]["question"],
                    yes_surface=gconst.area["choice"]["yes"],no_surface=gconst.area["choice"]["no"])
    self.teams[0].players[0].display(screen)
    """






  def graphic_choose_atout(self,screen,annonce_actuelle):
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
        draw_text(screen,"you must bet higher ! ",gconst.area["message"])


      screen.fill(gconst.GREEN,gconst.area["middle"])
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
              draw_text(screen,announce,gconst.area["announce"][value_or_color][announce],background_color=gconst.RED)
              pygame.display.flip()
              return announce
            else :
              if confirmation_zone!=None : # already click elsewhere
                draw_text(screen,confirmed_announce,confirmation_zone)
              draw_text(screen,announce,gconst.area["announce"][value_or_color][announce],background_color=gconst.YELLOW)
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
            self.coinche=False # TODO : COINCHE
            #self.coinche=generic.decision(random=coincheur.random, question='coincher sur {} {} ?'.format(bet,self.atout), ouverte=False)
          #PLAYER
          else :
            self.coinche= graphic_yesorno(screen,question="coincher ?",question_surface=gconst.area["choice"]["question"],
                                   yes_surface=gconst.area["choice"]["yes"],no_surface=gconst.area["choice"]["no"])
          if self.coinche:


             if not self.hidden : #GRAPHIC
               draw_text(screen,' {} coinche sur {} {} !'.format(coincheur.name,bet,self.atout),gconst.area["message"])
               wait_or_pass(2)



             for surcoincheur in self.teams[player.team].players:

               if not self.surcoinche :
                 #BOT
                 if surcoincheur.random:
                   self.surcoinche=False # TODO : COINCHE
                   #self.surcoinche=generic.decision(random=surcoincheur.random, question='surcoincher sur {} {} ?'.format(bet,self.atout), ouverte=False)
                 #PLAYER
                 else :
                   self.surcoinche= graphic_yesorno(screen,question="surcoincher ?",question_surface=gconst.area["choice"]["question"],
                                           yes_surface=gconst.area["choice"]["yes"],no_surface=gconst.area["choice"]["no"])
                 if self.surcoinche :
                     if not self.hidden : #GRAPHIC
                       draw_text(screen,' {} surcoinche sur {} {} !'.format(surcoincheur.name,bet,self.atout),gconst.area["message"])
                       wait_or_pass(2)




  def choose_atout(self,screen,background_color="GREEN"): # pensez a display avant surcoinche empecher danooncer 170 180 tout atout sans atout
    """
    select the atout and return true if someone didnt pass his turn
    """
    j=self.shortkey()
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
            """
            if not generic.decision(random=player.random, question='annoncer', ouverte=False): #local variable referenced before assignment
              turn+=1
            else :
              turn=1

              self.atout=generic.decision(const.liste_couleur, random=player.random, question ="Choisir la couleur d'atout : %s " % const.liste_couleur)

              while True :
                bet = generic.decision(const.liste_annonce, random=player.random, question="Choisir la hauteur d'annonce : %s " % const.liste_annonce )
                annonce_voulue=const.liste_annonce.index(bet)
                """

            wanted_bet,betColor=self.bots[player.name].bet()

            if wanted_bet!=None :
              annonce_voulue=const.liste_annonce.index(wanted_bet)

              if annonce_voulue>annonce_actuelle :
                bet=wanted_bet
                annonce_actuelle=annonce_voulue
                self.atout=betColor

                if not self.hidden :  #GRAPHIC
                  draw_text(screen,' {} prend à {} {} !'.format(player.name,bet,self.atout),gconst.area["message"])
                  draw_text(screen,'{} : {} {}'.format(self.teams[player.team].name,bet,self.atout),gconst.area["points"])
                  wait_or_pass(2)

                self.coincher(screen,player,bet)

                turn=1

              else : #bet too low

                turn+=1

            else : #doesnt bet

              turn+=1
            #print(player.name,turn,wanted_bet,betColor) # TODO : for test only remove this


          #PLAYER
          else :
            if not graphic_yesorno(screen,question="annoncer ?",question_surface=gconst.area["choice"]["question"],
                                   yes_surface=gconst.area["choice"]["yes"],no_surface=gconst.area["choice"]["no"]) :
              turn+=1
            else:
              turn=1
              self.atout,bet,annonce_actuelle=self.graphic_choose_atout(screen,annonce_actuelle)
              if not self.hidden :  #GRAPHIC
                draw_text(screen,'{} : {} {}'.format(self.teams[player.team].name,bet,self.atout),gconst.area["points"])#WE ASSUME

              self.coincher(screen,player,bet)


    if (self.atout==None):
          return False

    if not self.hidden :  #GRAPHIC
      for team in self.teams :
        if team.bet!=None:
          draw_text(screen,"L'équipe '{}' a pris {} {} !!!".format(team.name, team.bet, self.atout),gconst.area["message"])
          screen.fill(gconst.GREEN,gconst.area["middle"])

    return True




  def allowed_cards(self, choosen_color, j):
      """
      return cards allowed to play by the player who has to play
      """

      #cas 1 : la color demandée est atout
      if choosen_color==self.atout :

          #cas 1.1 : a de latout
          if j.Hand.rest[choosen_color]!=0 :
              atouts=[]

          #cas 1.11 : atout plus fort
              for carte in j.Hand.cards :
                  if carte.atout and carte.number!= None and carte.value > self.pli.cards[self.pli.winner()].value : #il faut checké que les cards sont présentes
                      atouts.append(carte)

              if len(atouts)!=0:
                  return GraphicHand("Cards allowed",cards=atouts)

          # cas 1.12 : pas d'atouts plus forts

              return j.Hand.color(choosen_color)

          #cas 1.2 pas d'atout
          return GraphicHand("Cards allowed",cards=j.Hand.cards)
      #cas 2 : la color demandée n'est pas latout

      #case 2.1 : a la color demandée
      if j.Hand.rest[choosen_color]!=0 :
          return j.Hand.color(choosen_color)

      #cas 2.2 : n'a  pas la color demandée

      #cas 2.21 : a atout
      if self.atout in const.liste_couleur[:4]:

          #cas 2.211 : le partenaire mène
          if self.pli.winner()%2==len(self.pli.cards)%2: #permet de se defausser sur partenaire
             return GraphicHand("Cards allowed",cards=j.Hand.cards)


         #cas 2.212 : on doit couper
          if j.Hand.rest[self.atout]!=0 :
              return j.Hand.color(self.atout)

      #cas 2.22 pas datout
      return GraphicHand("Cards allowed",cards=j.Hand.cards)

  def play_pli(self, players, pli_number): #•fonctionne
      """
      prends en entrée le tableau ORDONNEE des players de ce pli et le renvoi réordonné
      """

      #la meilleure card est le 1er joueur pour l'ini
      choosen_color=players[0].Hand.play(self.screen,players[0].number,players[0].random, self.pli,hand=players[0].Hand)

      for j in players[1:]:
          allowed_hand=self.allowed_cards( choosen_color, j)
          j.Hand.play(self.screen,j.number,j.random,self.pli,hand=allowed_hand)
      if not self.hidden :
        wait_or_pass(4)

      """
      choosen_color=players[0].Hand.play_card( self.pli, players[0].Hand.choose_card(random=players[0].random))

      for j in players[1:]:
          if not self.hidden :#GRAPHIC
            self.pli.display(self.screen,"board")
          allowed_hand=self.allowed_cards( choosen_color, j)
          choosen_card=allowed_hand.choose_card(random=j.random)           # trois lignes a verifier
          j.Hand.play_card( self.pli, choosen_card)
      if not self.hidden :# GRAPHIC
        self.pli.display(self.screen,"board")
      """

      winner=self.pli.winner()

      if not self.hidden :#GRAPHIC
        draw_text(self.screen,str("{} a gagné avec le {} de {}".format(players[winner].name, self.pli.cards[winner].number , self.pli.cards[winner].color )),gconst.area["points"])

      new_order=[players[winner],players[(winner+1)%4], players[(winner+2)%4] ,players[(winner+3)%4]]
      players[winner].plis+=1
      self.teams[players[winner].team].pli+=self.pli #reinitialise le pli
      assert(self.pli.rest["cards"]==0)

       #compter 10 de der
      if pli_number==8 :
          self.teams[players[winner].team].pli.points+=10

      return new_order


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
  for i in range(500):
    print(i)
    myround = GraphicRound( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                     team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                     hidden=True,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),number=0)
    myround.choose_atout(None)



def test_cards_update(): #random test

  for i in range( 500):
    myround = GraphicRound( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                   team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                   hidden=True,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),number=0)
    if myround.choose_atout(None) :
      myround.cards_update()


def test_play_pli(hidden=True): #•fonctionne
  for i in range( 500):
    myround = GraphicRound( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                   team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                   hidden=True,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),number=0)
    if myround.choose_atout(None) :
      myround.cards_update()
      players=myround.shortkey()
      for i in range(8):
        players=myround.play_pli(pli_number=i,players=players)






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



def test_cut():
  myround = GraphicRound( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                 team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                 hidden=True,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),number=0)

  for nb_of_try in range(100):

    myround.pioche = GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]])
    players=myround.classic_draw(cut=True)

    countinghand=GraphicHand(cards= (players[0]+players[1]+players[2]+players[3]) )
    cards_of_pioche=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]

    countinghand.test("Cards",8,8,8,8)


    for i in range(32):
      assert(countinghand.cards[i] not in (countinghand.cards[:i]+countinghand.cards[i+1:])) #check for double
      assert(countinghand.check_card(cards_of_pioche[i]))


def test_shortcut():
  myround = GraphicRound( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                 team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                 hidden=True,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),number=0)


  p=myround.shortkey()
  p[1].Hand=GraphicHand(cards=[GraphicCard("7","trefle")])
  assert(myround.teams[1].players[0].Hand.check_card(GraphicCard("7","trefle")))



def test_graphic_round():
  """
  Playing as Bob
  """

  pygame.init()
  screen=pygame.display.set_mode(gconst.screen_size)

  screen.fill(gconst.GREEN)
  pygame.display.flip()

  myround = GraphicRound( team1_name ="Les winners", j1_name="Bob", j1_random=False, j3_name="Fred", j3_random=True,
               team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
               hidden=False,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),number=0)
  myround.display(screen)

  while True:
    event = pygame.event.poll()


    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
            break

    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
      myround.pioche.display(screen,"j1")

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

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP1 :
      if myround.choose_atout(screen) :
        myround.cards_update()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_9 :
        screen.fill(gconst.GREEN)

    pygame.display.flip()

  pygame.quit()







if __name__=="__main__"   :

#ALLOWED_CARD COULD NOT WORK
  generic.test("init and random draw",test_init)
  generic.test("choose_atout",test_choose_atout)
  generic.test("cards_update",test_cards_update)
  generic.test("play_pli",test_play_pli)
  generic.test("classic_drawing",test_classic_drawing)
  generic.test("cut",test_cut)
  generic.test("shortcut",test_shortcut)
  """
  #GRAPHIC
  generic.test("Graphic",test_graphic_round)
  """
