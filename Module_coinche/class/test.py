#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:33:21 2019

@author: rthiebaut
"""
from Partie import Partie




if __name__=="__main__"   :             
    for i in range(20) :  #lance 200 parties 
        print("NEW GAME")    
        partie=Partie(joueurs=["Yan le pd","Vincent","Pierre","Guilhem"],equipes=["Les Boss","les loseurs"],aleatoire=[True,True,True,True],hidden=True)
        partie.jouer_partie()
        print(partie.manche.atout, partie.manche.equipes[0].mise, partie.manche.equipes[1].mise, partie.score)
        print("END GAME")   