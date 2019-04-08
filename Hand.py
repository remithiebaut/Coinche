# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 14:40:42 2019

@author: rthie
"""

import coinche_constant as const
import generical_function as generic
from Card import Card

class Hand():
  """
  Hand of Game Cards
  """
  def __init__(self, name="Cards", cards=list(), sort=True): #cards nest pas vide
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
     if sort :
       self.color_sort()

  def display(self,hidden=False):
     """
     display an array of cards
     """
     if not hidden :
         print("\n \n {:^15} \n".format(self.name))
         for i in range(len(self.cards)):
           print("{} : {:>2} de {} ".format(str(i+1),self.cards[i].number,self.cards[i].color))
         print()

  def __iadd__(self, oldhand):
    """
    this is the defintion of += : add a Hand of Card and reinitialize the oldhand
    """
    self.cards+=oldhand.cards
    for key in self.rest:
      self.rest[key]+=oldhand.rest[key]
    oldhand.reinitialize()

    return self

  def color_sort(self):
    """
    sort cards by color
    """
    newcards=[]
    for color in const.liste_couleur[:4] :
      for card in self.cards:
        if card.color==color :
          newcards.append(card)
    self.cards=newcards

  def remove_cards(self):
    """
    remove all cards of the hand which have a rest=False
    """
    newcards=[]
    for card in self.cards:
      if card.rest :
        newcards.append(card)
      else :
        self.rest[card.color]-=1
        self.rest["cards"]-=1
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

  def choose_card(self,random=True):
     """
     choose and return a card
     """
     while True :
         card_position = generic.decision(const.liste_entier8[:len(self.cards)], random, "Quelle carte ? 1ère, 2ème ? ")
         card_position = int(card_position)-1
         if card_position<len(self.cards) :
             if self.cards[card_position].rest:
                 return self.cards[card_position]

  def play_card(self ,pli ,choosen_card):
   """
   add choosen card to pli and return its color
   """
   # before used copy.deepcopy
   temphand=Hand(cards=[choosen_card]) #use it to add cleanly the card to pli
   pli+=temphand
   choosen_color=choosen_card.color
   choosen_card.rest=False # use it to remove cleanly the card from self
   self.remove_cards()
   choosen_card.rest=True

   return choosen_color

  def winner(self):
    """
    give the winner number in the current pli order really important that the pli is not sorted
    """
    winner=self.cards[0]
    for card in self.cards:
        # the winning card is not an atout
        if not winner.atout:
            if card.atout :
                winner=card
            elif winner.color==card.color and card.value>winner.value:
                winner=card
        else :
            if card.value>winner.value and card.atout:
                winner=card
    return self.cards.index(winner)

if __name__=="__main__"   :

  print("ini and color_sort test")
  mycard1=Card("7","carreau")
  mycard2=Card("7","coeur")
  myhand2=Hand(name="Pli",cards=[mycard2,mycard1])
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

  print("Test OK")


  print("add test")
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
  print("Test OK")


  print("reintialize test")
  assert(myhand2.name=="Pli")
  assert(len(myhand2.cards)==0)
  assert(myhand2.points==0)
  for key in myhand2.rest :
    assert(myhand2.rest[key]==0)
  assert(len(myhand2.rest)==5)
  print("Test OK")


  print("count_points test")
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
  print("Test OK")


  print("color test")
  for color in const.liste_couleur[:4]:
    mycolor=mypioche.color(color)
    assert(mycolor.name==color)
    assert(len(mycolor.cards)==8)
    assert(mycolor.points==0)
    assert(mycolor.rest["cards"]==8)
    assert(mycolor.rest[color]==8)
    assert(len(mycolor.rest)==5)

  print("Test OK")


  print("display test")
  mypioche.display(hidden=True)
  myhand.display(hidden=True)
  myhand2.display(hidden=True)
  print("No Test")


  print("remove test")
  mypioche.cards[4].rest=False
  mypioche.remove_cards()
  assert(mypioche.name=="pioche")
  assert(len(mypioche.cards)==31)
  assert(mypioche.rest["cards"]==31)
  assert(mypioche.rest["coeur"]==7)
  assert(mypioche.rest["pique"]==8)
  assert(mypioche.rest["trefle"]==8)
  assert(mypioche.rest["carreau"]==8)

  mypioche.cards[4].rest=False
  mypioche.cards[7].rest=False
  mypioche.remove_cards()
  assert(mypioche.name=="pioche")
  assert(len(mypioche.cards)==29)
  assert(mypioche.rest["cards"]==29)
  assert(mypioche.rest["coeur"]==6)
  assert(mypioche.rest["pique"]==7)
  assert(mypioche.rest["trefle"]==8)
  assert(mypioche.rest["carreau"]==8)
  print("Test OK")


  print("choose test")

  for i in range (100):
    card=mypioche.choose_card()
    assert(card.rest)

  print("play_card test")
  mycard3=Card("7","carreau")
  mycard4=Card("7","coeur")
  mycard5=Card("As","coeur")
  mycard6=Card("R","pique")

  myhand3=Hand(cards=[mycard3,mycard4])
  mypli=Hand(name="Pli", cards=[mycard5,mycard6])

  myhand3.play_card(pli=mypli, choosen_card=mycard3)

  assert(myhand3.name=="Cards")
  assert(len(myhand3.cards)==1)
  assert(myhand3.points==mypli.points==0)
  assert(myhand3.rest["cards"]==1)
  assert(myhand3.rest["coeur"]==1)
  assert(myhand3.rest["pique"]==0)
  assert(myhand3.rest["trefle"]==0)
  assert(myhand3.rest["carreau"]==0)
  assert(len(myhand3.rest)==5)

  assert(mypli.name=="Pli")
  assert(len(mypli.cards)==3)
  assert(mypli.rest["cards"]==3)
  assert(mypli.rest["coeur"]==1)
  assert(mypli.rest["pique"]==1)
  assert(mypli.rest["trefle"]==0)
  assert(mypli.rest["carreau"]==1)
  assert(len(mypli.rest)==5)

  mypli.play_card(pli=myhand3, choosen_card=mycard3)
  mypli.play_card(pli=myhand3, choosen_card=mycard5)
  mypli.play_card(pli=myhand3, choosen_card=mycard6)

  assert(myhand3.name=="Cards")
  assert(len(myhand3.cards)==4)
  assert(myhand3.points==mypli.points==0)
  assert(myhand3.rest["cards"]==4)
  assert(myhand3.rest["coeur"]==2)
  assert(myhand3.rest["pique"]==1)
  assert(myhand3.rest["trefle"]==0)
  assert(myhand3.rest["carreau"]==1)
  assert(len(myhand3.rest)==5)

  assert(mypli.name=="Pli")
  assert(len(mypli.cards)==0)
  assert(mypli.rest["cards"]==0)
  assert(mypli.rest["coeur"]==0)
  assert(mypli.rest["pique"]==0)
  assert(mypli.rest["trefle"]==0)
  assert(mypli.rest["carreau"]==0)
  assert(len(mypli.rest)==5)
  print("Test OK")


  print("winner test")

  aspique=Card("As","pique")
  dpique=Card("D","pique")
  septcoeur=Card("7","coeur")

  mypli2=Hand(name="Pli", sort=False, cards=[aspique,dpique,septcoeur])

  "atout coeur"
  septcoeur.atout=True
  aspique.value=8
  septcoeur.value=9
  dpique.value=5
  assert(mypli2.winner()==2)

  "atout pique"
  septcoeur.atout=False
  aspique.atout=True
  dpique.atout=True
  aspique.value=14
  septcoeur.value=1
  dpique.value=11

  assert(mypli2.winner()==0)

  "no atout pique first"
  septcoeur.atout=False
  aspique.atout=False
  dpique.atout=False
  aspique.value=8
  septcoeur.value=1
  dpique.value=5
  assert(mypli2.winner()==0)

  "no atout coeur first"
  mypli3=Hand(name="Pli" ,sort=False, cards=[septcoeur,aspique,dpique])
  aspique.value=8
  septcoeur.value=1
  dpique.value=5
  assert(mypli3.winner()==0)





  print("Test OK")


