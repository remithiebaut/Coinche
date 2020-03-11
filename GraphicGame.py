# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:14:01 2019

@author: rthie
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:49:30 2019

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
from GraphicRound import GraphicRound

from Game import Game

import random as rand



class GraphicGame(Game):
  def __init__(self, team_names=["e1","e2"], player_names=["j1","j2","j3","j4"], player_bots=[False,True,True,True],
               score_limit=2000,hidden=False,screen=None,
               difficulty="beginner"):

    self.data= {"team_names":team_names, "player_names":player_names, "player_bots":player_bots}

    self.Round=GraphicRound(team_names=self.data["team_names"], player_names=self.data["player_names"], player_bots=self.data["player_bots"],
              number=0,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),hidden=hidden,screen=screen,
              difficulty=difficulty)

    self.screen=screen
    self.limit=score_limit
    self.score={team_names[0]:0,team_names[1]:0}
    self.hidden=hidden
    self.difficulty=difficulty


  def result(self): # normalement mise nest pas char
    total_points=self.Round.teams[0].pli.count_points()+self.Round.teams[1].pli.count_points()
    assert(total_points==162 or total_points==182) #compte les points par équipe pas encore de 10 de der
    if self.Round.surcoinche :
        multiplicator = 4
    elif self.Round.coinche :
        multiplicator = 2
    else :
        multiplicator =1

    for team in self.Round.teams :
        if team.bet != None:
            capot= team.bet==250 and len(team.pli.cards)==32 #bool capot
            generale=(team.players[0].plis==8 and team.players[0].generale==True ) or ( team.players[1].plis==8 and team.players[1].generale==True) #bool generale
            #cas 1 : réussite du contrat
            if team.bet<=team.pli.points or capot or generale : #faire cas général : compteur de pli gagné par player
              if not self.hidden: #GRAPHIC
                draw_text(self.screen,"l'équipe {} a réussit son contrat".format(team.name),gconst.area["announce"]["bet"])

              #cas 1.1 : coinché ou surcoinché
              if self.Round.coinche :
                  self.score[team.name] += team.bet*multiplicator # seulement points contrats
                  self.score[self.Round.teams[(team.number+1)%2].name] += 0 #points defense

              #cas 1.2 : normal
              else :
                  self.score[team.name] += team.bet # seulement points contrats
                  self.score[self.Round.teams[(team.number+1)%2].name] += self.Round.teams[(team.number+1)%2].pli.points #points defense

            #cas 2 : échec du contrat
            else :
                if not self.hidden: #GRAPHIC
                  draw_text(self.screen,"l'équipe {} a chuté ".format(team.name),gconst.area["announce"]["bet"])
                self.score[self.Round.teams[(team.number+1)%2].name] += 160*multiplicator

  def end_round(self) :
    self.result()
    if not self.hidden: #GRAPHIC
      draw_text(self.screen,str(self.score),gconst.area["points"])
    for team in self.score:
      if self.score[team]>self.limit: #error
        if not self.hidden: #GRAPHIC
          draw_text(self.screen, " l'équipe {} a gagné avec {} ".format(team, self.score),gconst.area["message"])
        return False
    return True

  def new_round(self,round_number) :


    pioche=GraphicHand(name="pioche",cards=[],sort=False)
      # the last round was played
    pioche+=self.Round.teams[0].pli
    pioche+=self.Round.teams[1].pli
      # the last round wasn't played
    players_in_order=self.Round.shortkey() #changer ordre a chaque manche ????
    for player in players_in_order :
      pioche+=player.Hand
    assert(pioche.rest["cards"]==32)
    for card in pioche.cards : # it seems to work
      card.reset()

    self.Round=GraphicRound(team_names=self.data["team_names"], player_names=self.data["player_names"], player_bots=self.data["player_bots"],
                        number=round_number,pioche=pioche,hidden=self.hidden,screen=self.screen,
                        difficulty=self.difficulty)


  def play(self):
    self.Round.display(self.screen)
    if self.Round.choose_atout(self.screen) : #choisir valeur par defaut pour les test
      players_in_order=self.Round.shortkey() #changer ordre a chaque manche ????
      self.Round.cards_update()
      for i in range(8):
        #if not self.hidden: #GRAPHIC
        #  print("pli {} : \n \n".format(i))
        players_in_order=self.Round.play_pli( players=players_in_order, pli_number=i+1) #erreur dans le decompte des plis confusion avec les tas player bug a iteration2 a priori fonctionne : confusion entre la position dans la main et celles des cartes possibles
        if not self.hidden :
          self.screen.fill(gconst.GREEN,gconst.area["middle"])
      #for k in range(2):
        #if not self.hidden: #GRAPHIC
        #  self.Round.teams[k].pli.display(self.screen,"board")
      return True #a trump was picked
    else :
      return False #nobody picked a trump : it's a white round



  def reinitialize(self):
    self.new_round(round_number=0)
    self.score={self.data["team_names"][0]:0,self.data["team_names"][1]:0}



  def run(self):
    while True : #game root
      round_number = -1 # to start the first at 0
      played = True
      while True: # round root
        while True : #round of assertion : is a trump is taken or not
          round_number+=1
          self.new_round(round_number)
          played=self.play()
          if played :
            break
        if not self.end_round():
           break
      if not generic.decision(question="une nouvelle partie", ouverte=False,random=self.hidden):
        break
      else :
        self.reinitialize()

def random_test():
    mygame=GraphicGame(player_bots=[True]*4,hidden=True,difficulty="advanced")
    mygame.run()

def test_graphic_game():
  """
  Playing as joueur1
  """

  pygame.init()
  screen=pygame.display.set_mode(gconst.screen_size)

  screen.fill(gconst.GREEN)
  pygame.display.flip()
  mygame=GraphicGame(player_bots=[False,True,True,True],hidden=False,screen=screen,difficulty="advanced")


  while True:
    event = pygame.event.poll()


    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
            break

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
      mygame.run()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_9 :
        screen.fill(gconst.GREEN)

    pygame.display.flip()

  pygame.quit()


if __name__=="__main__"   :

  """
  print("random test")
  for i in range(500):
    random_test()
  print("test OK")
  """
  test_graphic_game()

