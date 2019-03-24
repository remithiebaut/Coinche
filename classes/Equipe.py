#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:45:54 2019

@author: rthiebaut
"""
from Joueur import Joueur
from Main import Main


class Equipe():
    def __init__(self,pioche, j1, j2, numero_equipe):
     
     self.nom=j1[1]
     self.numero=numero_equipe
     self.joueurs=[Joueur(pioche,self.numero,j1[0],j1[2]), Joueur(pioche,self.numero,j2[0],j2[2])]
     self.pli=Main("pli de l'equipe " + str(numero_equipe)) #a reinitialiser
     self.mise=None  #a reinitialiser