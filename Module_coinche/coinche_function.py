#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:30:05 2019

@author: rthiebaut
"""

import random #use randrange
import sys
import coinche_constant as const
import coinche_class 
import generical_function as generic
import copy

"""
Functions
"""

def affiche_cartes(cartes,nom="cartes",hidden=False):
   """
   affiche un tableau de cartes
   """
   if not hidden :
       print("\n \n {:^15} \n".format(nom))
       for i in range(len(cartes)):
           if not cartes[i].numero==None :
            print("{} : {:>2} de {} ".format(str(i+1),cartes[i].numero,cartes[i].couleur))
       print()



 

def choisir_carte(cartes,nom,aleatoire=True): 
     """
     choisie et retourne une carte
     """
     affiche_cartes(cartes,nom,aleatoire)
     while True :
         position_carte = generic.decision(const.liste_entier8[:len(cartes)], aleatoire, "Quelle carte ? 1ère, 2ème ? ")
         position_carte = int(position_carte)-1
         if position_carte<len(cartes) :
             if cartes[position_carte].numero!=None:
                 return cartes[position_carte]

              
    


    

def gain_pli(pli): 
    """
    donne lindice du gagnant du pli dans lordre du pli
    """
    gagnant=pli.cartes[0]
    for carte in pli.cartes:
        # la carte qui domine n'est pas un atout
        if not gagnant.atout:
            if carte.atout :
                gagnant=carte
            elif gagnant.couleur==carte.couleur and carte.valeur>gagnant.valeur:
                gagnant=carte
        
        else :
            if carte.valeur>gagnant.valeur and carte.atout:
                gagnant=carte
    return pli.cartes.index(gagnant)






