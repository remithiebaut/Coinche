#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:49:30 2019

@author: rthiebaut
"""
from coinche_function import affiche_cartes
from coinche_class_manche import Manche
import generical_function as generic


class Partie():
     def __init__(self,joueurs=["joueur1","joueur2","joueur3","joueur4"],equipes=["e1","e2"],limite_score=2000,aleatoire=[False,True,True,True],hidden=False):
         
         self.data=[(joueurs[0],equipes[0],aleatoire[0]), (joueurs[1],equipes[1],aleatoire[1]),(joueurs[2],equipes[0],aleatoire[2]),(joueurs[3],equipes[1],aleatoire[3])] #trouver comment utiliser tuple en parametre
         self.manche=Manche(self.data[0], self.data[1], self.data[2], self.data[3], hidden ) #faire un tableau de manche
         self.limite=limite_score
         self.score={equipes[0]:0,equipes[1]:0}
         self.hidden=hidden
    
     def jouer_partie(self):
         j=self.manche.raccourci()
         if self.manche.choisir_atout() : #choisir valeur par defaut pour les test
             self.manche.debut(j)
             for i in range(8):
                if not self.hidden:
                    print("pli {} : \n \n".format(i))
                j=self.manche.jouer_pli( j, i+1) #erreur dans le decompte des plis confusion avec les tas joueur bug a iteration2 a priori fonctionne : confusion entre la position dans la main et celles des cartes possibles
             for k in range(2):
                affiche_cartes(self.manche.equipes[k].pli.cartes, self.manche.equipes[k].pli.name)   
             self.fin_manche()
         self.nouvelle_manche()
                 
             
     def fin_manche(self) :
         self.manche.resultat(self.score)
         print(self.score)
         for equipe in self.score:
             if self.score[equipe]>self.limite:
                 print( " l'équipe {} a gagné avec {} ".format(equipe, self.score))
                 return 0
             
     def nouvelle_manche(self) :       
                
         if generic.decision(question="nouvelle manche ?", ouverte=False,aleatoire=self.hidden):
             self.data=[self.data[1],self.data[2],self.data[3],self.data[0]]
             self.manche=Manche(self.data[0], self.data[1], self.data[2], self.data[3],self.hidden)
             self.jouer_partie()