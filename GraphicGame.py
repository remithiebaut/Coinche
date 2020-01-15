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
  def __init__(self, team1_name="e1", j1_name="joueur1", j1_random=False, j3_name="joueur3", j3_random=True,
               team2_name="e2", j2_name="joueur2", j2_random=True,j4_name="joueur4", j4_random=True,
               score_limit=2000,hidden=False,screen=None):

    self.data={"team1_name":team1_name, "j1_name":j1_name, "j1_random":j1_random, "j3_name":j3_name, "j3_random":j3_random,
           "team2_name":team2_name, "j2_name":j2_name, "j2_random":j2_random,"j4_name":j4_name, "j4_random":j4_random}

    self.Round=GraphicRound(team1_name=self.data["team1_name"], j1_name=self.data["j1_name"], j1_random=self.data["j1_random"],
              j3_name=self.data["j3_name"], j3_random=self.data["j3_random"],
              team2_name=self.data["team2_name"], j2_name=self.data["j2_name"], j2_random=self.data["j2_random"],
              j4_name=self.data["j4_name"], j4_random=self.data["j4_random"],
              number=0,pioche=GraphicHand(name="pioche",cards=[GraphicCard(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]),hidden=hidden,screen=screen)

    self.screen=screen
    self.limit=score_limit
    self.score={team1_name:0,team2_name:0}
    self.hidden=hidden


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

    self.Round=GraphicRound(team1_name=self.data["team1_name"], j1_name=self.data["j1_name"], j1_random=self.data["j1_random"],
                        j3_name=self.data["j3_name"], j3_random=self.data["j3_random"],
                        team2_name=self.data["team2_name"], j2_name=self.data["j2_name"], j2_random=self.data["j2_random"],
                        j4_name=self.data["j4_name"], j4_random=self.data["j4_random"],
                        number=round_number,pioche=pioche,hidden=self.hidden,screen=self.screen)


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
    self.score={self.data["team1_name"]:0,self.data["team2_name"]:0}



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
    mygame=GraphicGame(j1_random=True,hidden=True)
    mygame.run()

def test_graphic_game():
  """
  Playing as joueur1
  """

  pygame.init()
  screen=pygame.display.set_mode(gconst.screen_size)

  screen.fill(gconst.GREEN)
  pygame.display.flip()
  mygame=GraphicGame(j1_random=False,hidden=False,screen=screen)


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

  print("random test")
  for i in range(500):
    random_test()
  print("test OK")

  test_graphic_game()

