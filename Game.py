#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:49:30 2019

@author: rthiebaut
"""
from Manche import Manche
import generical_function as generic


class Game():
     def __init__(self,joueurs=["joueur1","joueur2","joueur3","joueur4"],equipes=["e1","e2"],limite_score=2000,aleatoire=[False,True,True,True],hidden=False):
         
         self.data=[(joueurs[0],equipes[0],aleatoire[0]), (joueurs[1],equipes[1],aleatoire[1]),(joueurs[2],equipes[0],aleatoire[2]),(joueurs[3],equipes[1],aleatoire[3])] #trouver comment utiliser tuple en parametre
         self.Round=Round(self.data[0], self.data[1], self.data[2], self.data[3], hidden ) #faire un tableau de manche
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
                self.manche.equipes[k].pli.afficher()   
             self.fin_manche()
         self.nouvelle_manche()
                 
    def result(self): # normalement mise nest pas char
        points_totaux=self.equipes[0].pli.compter_points()+self.equipes[1].pli.compter_points()
        assert(points_totaux==162 or points_totaux==182) #compte les points par équipe pas encore de 10 de der
        if self.surcoinche :
            multiplicateur = 4
        elif self.coinche :
            multiplicateur = 2
        else :
            multiplicateur =1
  
        for equipe in self.equipes :
            if equipe.mise != None:
                capot= equipe.mise==250 and len(equipe.pli.cartes)==32 #bool capot
                generale=(equipe.joueurs[0].plis==8 and equipe.joueurs[0].generale==True ) or ( equipe.joueurs[1].plis==8 and equipe.joueurs[1].generale==True) #bool generale
                #cas 1 : réussite du contrat
                if equipe.mise<=equipe.pli.points or capot or generale : #faire cas général : compteur de pli gagné par joueur
                    print("l'équipe {} a réussit son contrat".format(equipe.nom))
  
                    #cas 1.1 : coinché ou surcoinché
                    if self.coinche :
                        score[equipe.nom] += equipe.mise*multiplicateur # seulement points contrats
                        score[self.equipes[(equipe.numero+1)%2].nom] += 0 #points defense
  
                    #cas 1.2 : normal
                    else :
                        score[equipe.nom] += equipe.mise # seulement points contrats
                        score[self.equipes[(equipe.numero+1)%2].nom] += self.equipes[(equipe.numero+1)%2].pli.points #points defense
  
                #cas 2 : échec du contrat
                else :
                    print("l'équipe {} a chuté ".format(equipe.nom))
                    score[self.equipes[(equipe.numero+1)%2].nom] += 160*multiplicateur
                    
     def fin_manche(self) :
         self.result()
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