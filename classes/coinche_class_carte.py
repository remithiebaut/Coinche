#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:48:39 2019

@author: rthiebaut
"""

class carte():
 def __init__(self, numero, couleur, reste=1):
  self.numero=numero #prend la valeur none quand inexistant
  self.couleur=couleur
  self.reste=reste #utilisé seulement dans la distribution de cartes, lutiliser a la place de none ?
  self.valeur=None #ordre de puissance dans lannonce actuelle 16 valet datout et 1:7 normal
  self.atout=False
  self.points=0