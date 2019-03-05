#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:46:45 2019

@author: rthiebaut
"""
import random

class main():
    def __init__(self,name): 
       self.name=name
       self.cartes=[]
       self.points=0
       #initialise les compteur
       self.reste={"cartes":0} #changé en dico
       for couleur in const.liste_couleur[:4]:
           self.reste[couleur]=0           
           
    def add(self, supplement):
        self.cartes+=supplement.cartes
        for key in self.reste:
            self.reste[key]+=supplement.reste[key]
            
    def tri_couleur(self):
        """
        trie les cartes par couleur et mets a jour les compteurs de restes à jour
        """
        new_cartes=[]
        for couleur in const.liste_couleur[:4] :
            for carte in self.cartes:
                if carte.couleur==couleur:
                    new_cartes.append(carte)
                    self.reste[couleur]+=1
        self.cartes=new_cartes
    
    def piocher(self,pioche):    
        while not self.reste["cartes"]==8 : #on peut probablement faire plus rapide(prendre aleatoirement dans les cartes restantes)
           x=int(1000*random.random()%8) # il est possible que le bug survienne apres plusieurs boucles (apres test)
           y=int(1000*random.random()%4)
           if pioche[y][x].reste==1:
               self.cartes.append(pioche[y][x])
               pioche[y][x].reste=0
               self.reste["cartes"]+=1
        self.tri_couleur() #remet les compteurs de couleur à jour
    
    def compter_points(self):
        for carte in self.cartes:
            self.points+=carte.points
        return self.points
    
    def couleur(self, couleur_choisie):
        """
        retournent toutes les cartes d'une couleur donnée
        """
        cartes_de_la_couleur=[]
        for carte in self.cartes:
            if carte.couleur==couleur_choisie: 
                cartes_de_la_couleur.append(carte)
        return cartes_de_la_couleur
    
    def jouer_carte(self,pli,carte_choisie):
     """
     joue la carte choisie et retourne sa couleur
     """
     pli.cartes.append(copy.deepcopy(carte_choisie)) # a priori marche voir doc deepcopy
     couleur_choisie=carte_choisie.couleur
     pli.reste[couleur_choisie]+=1
     pli.reste["cartes"]+=1
     self.reste[couleur_choisie]-=1
     self.reste["cartes"]-=1
     carte_choisie.numero=None 
     
     return couleur_choisie   


