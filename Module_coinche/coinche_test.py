#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:33:21 2019

@author: rthiebaut
"""
import random #use randrange
import sys
import coinche_constant as constant
import coinche_function 
import coinche_class 
import generical_function as generic



if __name__=="__main__"   :             
    for i in range(20) :  #lance 200 parties 
        print("NEW GAME")    
        Partie=coinche_class.partie(joueurs=["Yan le pd","Vincent","Pierre","Guilhem"],equipes=["Les Boss","les loseurs"],aleatoire=[False,True,True,True])
        Partie.jouer_partie()
        print(Partie.manche.atout, Partie.manche.equipes[0].mise, Partie.manche.equipes[1].mise, Partie.score)
        print("END GAME")   