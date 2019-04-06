# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:40:42 2019

@author: rthie
"""

import random
import copy
import coinche_constant as const
import generical_function as generic

class Hand():
  """
  Hand of Game Cards
  """
  def __init__(self,name="Cards"): #cards nest pas vide
     self.name=name
     self.cards=[]
     self.points=0
     #initialise les compteur
     self.rest={"cards":0} #changé en dico
     for color in const.liste_couleur[:4]:
         self.rest[color]=0 
         
  def add_cartes(self, cartes):
      for carte in cartes :
          self.cartes.append(carte)
          self.reste["cartes"]+=1
      self.tri_couleur()   
          
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
    """
    count points in the hand
    """
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
 
  def afficher(self,hidden=False):
     """
     affiche un tableau de self.cartes
     """
     if not hidden :
         print("\n \n {:^15} \n".format(self.name))
         for i in range(len(self.cartes)):
             if not self.cartes[i].numero==None :
              print("{} : {:>2} de {} ".format(str(i+1),self.cartes[i].numero,self.cartes[i].couleur))
         print()
 

  def choisir(self,aleatoire=True): 
     """
     choisie et retourne une carte
     """
     self.afficher(hidden=aleatoire)
     while True :
         position_carte = generic.decision(const.liste_entier8[:len(self.cartes)], aleatoire, "Quelle carte ? 1ère, 2ème ? ")
         position_carte = int(position_carte)-1
         if position_carte<len(self.cartes) :
             if self.cartes[position_carte].numero!=None:
                 return self.cartes[position_carte]
  

  def gagnant(self): 
    """
    donne lindice du gagnant du pli dans lordre du pli
    """
    gagnant=self.cartes[0]
    for carte in self.cartes:
        # la carte qui domine n'est pas un atout
        if not gagnant.atout:
            if carte.atout :
                gagnant=carte
            elif gagnant.couleur==carte.couleur and carte.valeur>gagnant.valeur:
                gagnant=carte
        
        else :
            if carte.valeur>gagnant.valeur and carte.atout:
                gagnant=carte
    return self.cartes.index(gagnant) 

if __name__=="__main__"   :             
  myhand=Hand("Pli")
  myhand2=Hand()
  assert(myhand.name=="Pli")
  assert(myhand2.name=="Cards")
  assert(len(myhand.cards)==0)
  assert(myhand.points==0) 
  for key in myhand.rest :
    assert(myhand.rest[key]==0)
  assert(len(myhand.rest)==5)
  
  print("test OK")