# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:40:42 2019

@author: rthie
"""

import random
import copy
import coinche_constant as const
import generical_function as generic
from Card import Card

class Hand():
  """
  Hand of Game Cards
  """
  def __init__(self, name="Cards", cards=list()): #cards nest pas vide
     self.name=name
     self.cards=cards #array of cards
     self.points=0
     #initialise th counter
     self.rest={"cards":len(cards)} 
     for color in const.liste_couleur[:4]:
       self.rest[color]=0 
       for card in self.cards:
         if card.color==color:
           self.rest[color]+=1
     self.color_sort()
     
  def __iadd__(self, oldhand):
    """
    this is the defintion of += : add a Hand of Card sort them and reinitialize the oldhand
    """
    self.cards+=oldhand.cards
    for key in self.rest:
      self.rest[key]+=oldhand.rest[key]
    oldhand.reinitialize() 
    self.color_sort()
    return self

  def color_sort(self):
      """
      sort cards by color
      """
      newcards=[]
      for color in const.liste_couleur[:4] :
        for card in self.cards:
          if card.color==color:
            newcards.append(card)
      self.cards=newcards
      
  def reinitialize(self):
    "reinitialize the Hand with no cards"
    self.cards=list() #array of cards
    self.points=0
    #reinitialize counters
    for key in self.rest:
      self.rest[key]=0

  def count_points(self):
    """
    count points in the hand
    """
    for card in self.cards:
        self.points += card.points
    return self.points

  def color(self, chosen_color):
    """
    return all the cards of a given color => it is now returning a Hand !!
    """
    cards_of_this_color=[]
    for card in self.cards:
        if card.color==chosen_color: 
            cards_of_this_color.append(card)
    colorhand=Hand(cards=cards_of_this_color, name =chosen_color)
    return colorhand
  
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
  
  "ini and sort test"
  mycard1=Card("7","carreau")
  mycard2=Card("7","coeur")
  myhand2=Hand(name="Pli",cards=[mycard1,mycard2])
  assert(myhand2.name=="Pli")
  assert(len(myhand2.cards)==2)
  assert(myhand2.points==0) 
  assert(myhand2.rest["coeur"]==1)
  assert(myhand2.rest["cards"]==2)
  assert(myhand2.rest["pique"]==0)
  assert(myhand2.rest["trefle"]==0)
  assert(myhand2.rest["carreau"]==1)
  assert(myhand2.cards[0].color=="coeur")
  assert(myhand2.cards[1].color=="carreau")
  assert(len(myhand2.rest)==5)
  
  myhand=Hand()
  assert(myhand.name=="Cards")
  assert(len(myhand.cards)==0)
  assert(myhand.points==0) 
  for key in myhand.rest :
    assert(myhand.rest[key]==0)
  assert(len(myhand.rest)==5)
  
  "add test"
  myhand += myhand2
  assert(myhand.name=="Cards")
  assert(len(myhand.cards)==2)
  assert(myhand.points==0) 
  assert(myhand.rest["coeur"]==1)
  assert(myhand.rest["cards"]==2)
  assert(myhand.rest["pique"]==0)
  assert(myhand.rest["trefle"]==0)
  assert(myhand.rest["carreau"]==1)
  assert(myhand.cards[0].color=="coeur")
  assert(myhand.cards[1].color=="carreau")
  assert(len(myhand.rest)==5)
  
  "reintialize test"
  assert(myhand2.name=="Pli")
  assert(len(myhand2.cards)==0)
  assert(myhand2.points==0) 
  for key in myhand2.rest :
    assert(myhand2.rest[key]==0)
  assert(len(myhand2.rest)==5)
  
  
  "count_points test"
  mycard1.points+=4
  mycard2.points+=5
  assert(myhand.count_points()==9==myhand.points)
  assert(myhand.points==9)
  assert(myhand2.count_points()==myhand2.points==0)


  pioche =[ Card(i,j) for j in const.liste_couleur[:4] for i in const.liste_numero] 
  mypioche=Hand(cards=pioche,name="pioche")
  assert(mypioche.name=="pioche")
  assert(len(mypioche.cards)==32)
  assert(mypioche.rest["cards"]==32)
  assert(mypioche.cards==pioche)
  for color in const.liste_couleur[:4]:
    assert(mypioche.rest[color]==8)
    
    
  "color test"
  for color in const.liste_couleur[:4]:
    mycolor=mypioche.color(color)
    assert(mycolor.name==color)
    assert(len(mycolor.cards)==8)
    assert(mycolor.points==0) 
    assert(mycolor.rest["cards"]==8)
    assert(mycolor.rest[color]==8)
    assert(len(mycolor.rest)==5)
  

  
  print("test OK")
  
  
