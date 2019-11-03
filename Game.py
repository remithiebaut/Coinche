#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:49:30 2019

@author: rthiebaut
"""
from Round import Round
from Hand import Hand
from Card import Card

import generical_function as generic
import coinche_constant as const




class Game():
   def __init__(self, team1_name="e1", j1_name="joueur1", j1_random=False, j3_name="joueur3", j3_random=True,
             team2_name="e2", j2_name="joueur2", j2_random=True,j4_name="joueur4", j4_random=True,
             score_limit=2000,hidden=False):

     self.data={"team1_name":team1_name, "j1_name":j1_name, "j1_random":j1_random, "j3_name":j3_name, "j3_random":j3_random,
             "team2_name":team2_name, "j2_name":j2_name, "j2_random":j2_random,"j4_name":j4_name, "j4_random":j4_random}

     self.Round=Round(team1_name=self.data["team1_name"], j1_name=self.data["j1_name"], j1_random=self.data["j1_random"],
                j3_name=self.data["j3_name"], j3_random=self.data["j3_random"],
                team2_name=self.data["team2_name"], j2_name=self.data["j2_name"], j2_random=self.data["j2_random"],
                j4_name=self.data["j4_name"], j4_random=self.data["j4_random"],
                number=0,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur]),hidden=hidden)

     #self.Round=Round(team1_name=team1_name, j1_name=j1_name, j1_random=j1_random, j3_name=j3_name, j3_random=j3_random,
     #team2_name=team2_name, j2_name=j2_name, j2_random=j2_random,j4_name=j4_name, j4_random=j4_random, hidden=hidden ) #faire un tableau de manche
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
                  print("l'équipe {} a réussit son contrat".format(team.name))

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
                    print("l'équipe {} a chuté ".format(team.name))
                  self.score[self.Round.teams[(team.number+1)%2].name] += 160*multiplicator

   def end_round(self) :

       self.result()
       if not self.hidden: #GRAPHIC
         print(self.score)
       for team in self.score:
         if self.score[team]>self.limit: #error
               if not self.hidden: #GRAPHIC
                 print(self.Round.atout, self.Round.teams[0].bet, self.Round.teams[1].bet)
                 print( " l'équipe {} a gagné avec {} ".format(team, self.score))
               return False
       return True

   def new_round(self,round_number) :

    pioche=Hand(name="pioche",cards=[],sort=False)
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

    self.Round=Round(team1_name=self.data["team1_name"], j1_name=self.data["j1_name"], j1_random=self.data["j1_random"],
                        j3_name=self.data["j3_name"], j3_random=self.data["j3_random"],
                        team2_name=self.data["team2_name"], j2_name=self.data["j2_name"], j2_random=self.data["j2_random"],
                        j4_name=self.data["j4_name"], j4_random=self.data["j4_random"],
                        number=round_number,pioche=pioche,hidden=self.hidden)


   def play(self):
       if self.Round.choose_atout() : #choisir valeur par defaut pour les test
         players_in_order=self.Round.shortkey() #changer ordre a chaque manche ????
         self.Round.cards_update()
         for i in range(8):
            if not self.hidden: #GRAPHIC
                print("pli {} : \n \n".format(i))
            players_in_order=self.Round.play_pli( players=players_in_order, pli_number=i+1) #erreur dans le decompte des plis confusion avec les tas player bug a iteration2 a priori fonctionne : confusion entre la position dans la main et celles des cartes possibles
         for k in range(2):
            if not self.hidden: #GRAPHIC
              self.Round.teams[k].pli.display()
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
    mygame=Game(j1_random=True,hidden=True)
    mygame.run()

if __name__=="__main__"   :

  print("random test")
  for i in range(500):
    random_test()
  print("test OK")

