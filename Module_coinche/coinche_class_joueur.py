#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:45:53 2019

@author: rthiebaut
"""
from coinche_class_main import Main


class Joueur():
   def __init__(self, pioche, numero_equipe, name, aleatoire):
       
       self.name=name
       self.main=Main(name)
       self.main.piocher(pioche)
       self.equipe=numero_equipe
       self.plis=0
       self.generale=False #indicateur dannonce generale
       self.aleatoire=aleatoire
       



