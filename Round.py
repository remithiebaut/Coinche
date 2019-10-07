#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:30:05 2019

@author: rthiebaut
"""
import coinche_constant as const
import generical_function as generic
from Hand import Hand
from Card import Card
from Team import Team
import random as rand


class Round():
  """
  One Round of coinche
  """
  def __init__(self, team1_name, j1_name, j1_random, j3_name, j3_random,
               team2_name, j2_name, j2_random, j4_name, j4_random ,
               number,pioche, hidden=False): # e1 et e2 inutiles
    
   self.number=number
   self.atout=None
   self.coinche=False #indicator of coinche
   self.surcoinche=False
   self.pli=Hand(name="Pli in progress",cards=[], sort=False)
   assert(self.pli.rest["cards"]==0)
   self.pioche=pioche
   if self.number==0 :
     players=self.random_draw()
   else :
     players=self.classic_draw()
   self.teams=[Team(team_name=team1_name, team_number=0,
                    j1_name=j1_name, j1_random=j1_random, j1_cards=players[0],
                    j2_name=j3_name, j2_random=j3_random, j2_cards=players[2]),
               Team(team_name=team2_name, team_number=1,
                    j1_name=j2_name, j1_random=j2_random, j1_cards=players[1],
                    j2_name=j4_name, j2_random=j4_random, j2_cards=players[3])]
   self.hidden=hidden



  def random_draw(self):
    """
    #draw randomly in an array of cards
    """
    players=list()
    for nb_player in range(4):
      player=list()
      for nb_card in range(8):
        card=self.pioche.choose_card(random=True)
        card.rest=False
        player.append(card)
      players.append(player)

    for player in players:
      for card in player:
        card.rest=True

    self.pioche.reinitialize()
    return players



  def classic_draw(self, cut=False):
    """
    simulate the classic distribution in 3 3 2 self.pioche must countain the card in the rigth order
    """
    if cut :
      k=rand.randrange(32)#random cut the kieme card become the first the k-1 ieme become the last

      self.pioche.cards = self.pioche.cards[k:] + self.pioche.cards[:k]


    players=[(self.pioche.cards[3*i:3*i+3]+self.pioche.cards[3*i+12:3*i+15]+self.pioche.cards[2*i+24:2*i+26])
            for i in range(4)]

    self.pioche.reinitialize()
    return players



  def shortkey(self): #write quicker
    """
    In order to write quicker return an array of four players j1 j2 j3 j4
    """
    players=[self.teams[0].players[0],  self.teams[1].players[0], self.teams[0].players[1], self.teams[1].players[1]]
    return players



  def choose_atout(self): # pensez a display avant surcoinche empecher danooncer 170 180 tout atout sans atout
     """
     fix the atout and return true if someone didnt pass his turn
     """
     j=self.shortkey()
     bet=0
     annonce_actuelle=-1
     turn=0
     while turn!=4 and bet!='generale' and not self.coinche:
        for player in j:
           if turn==4 or bet=='generale' or self.coinche:
              break
           else:
              if not self.hidden :  #GRAPHIC
                player.Hand.display(player.random)

              if not generic.decision(random=player.random, question='annoncer', ouverte=False): #local variable referenced before assignment
                 turn+=1

              else:
                 turn=1

                 self.atout=generic.decision(const.liste_couleur, random=player.random, question ="Choisir la couleur d'atout : %s " % const.liste_couleur)

                 while True :

                    bet = generic.decision(const.liste_annonce, random=player.random, question="Choisir la hauteur d'annonce : %s " % const.liste_annonce )
                    annonce_voulue=const.liste_annonce.index(bet)
                    if annonce_voulue>annonce_actuelle :
                        annonce_actuelle=annonce_voulue

                        if not self.hidden :  #GRAPHIC
                          print(' {} prend à {} {} !'.format(player.name,bet,self.atout))

                        break

                 self.teams[player.team].bet=bet #fixe la bet de lteam attention bet est un char
                 self.teams[(player.team+1)%2].bet=None
                 if bet == "generale":
                     player.generale=True
                 for coincheur in self.teams[(player.team+1)%2].players:

                   if not self.hidden :  #GRAPHIC
                     coincheur.Hand.display(coincheur.random)

                   if not self.coinche :
                      self.coinche=generic.decision(random=coincheur.random, question='coincher sur {} {} ?'.format(bet,self.atout), ouverte=False)
                      if self.coinche:
                         if not self.hidden : #GRAPHIC
                           print(' {} coinche sur {} {} !'.format(coincheur.name,bet,self.atout))
                         for surcoincheur in self.teams[player.team].players:

                           if not self.hidden : #GRAPHIC
                             surcoincheur.Hand.display(surcoincheur.random)

                           if not self.surcoinche :
                               self.surcoinche=generic.decision(random=surcoincheur.random, question='surcoincher sur {} {} ?'.format(bet,self.atout), ouverte=False)
                               if self.surcoinche :
                                 if not self.hidden : #GRAPHIC
                                   print(' {} surcoinche sur {} {} !'.format(surcoincheur.name,bet,self.atout))

     if (self.atout==None):
          return False

     if not self.hidden :  #GRAPHIC
       for team in self.teams :
            if team.bet!=None:
                print("L'équipe '{}' a pris {} à {} !!!".format(team.name, team.bet, self.atout))

     return True



  def cards_update(self): #memory leak => the next round will start with a pli of 40 cards for no reason
    """
    Update the cards after the trump color is choosen
    """
    players=self.shortkey()
    #normal
    if self.atout in const.liste_couleur[:4]:

        for j in players:
            belote=0
            for card in j.Hand.cards:
                if card.color==self.atout:
                    card.atout=True
                    card.value=const.ordre_atout.index(card.number)
                    card.points=const.points[const.liste_mode[1]][card.number]
                    if card.number=="R" or card.number=="D":
                        belote+=1
                        if belote==2:
                            if not self.hidden :  #GRAPHIC
                              print("le joueur {} a la belote".format(j.name)) # do not tell it right away
                            self.teams[j.team].pli.points+=20

                else :
                    card.value=const.liste_numero.index(card.number)
                    card.points=const.points[const.liste_mode[0]][card.number]
    #sans atout
    elif self.atout==const.liste_couleur[4]:
        for j in players :
            for card in j.Hand.cards:
                card.value=const.liste_numero.index(card.number)
                card.points=const.points[const.liste_mode[2]][card.number]

    #tout atout
    elif self.atout==const.liste_couleur[5]:
        for j in players :
            for card in j.Hand.cards:
                card.atout=True
                card.value=const.ordre_atout.index(card.number)
                card.points=const.points[const.liste_mode[3]][card.number]

    total_points=0

    for team in self.teams: #associe la bet a un nombre de points
        if team.bet!= None:
            if team.bet=='capot':
                team.bet=250
            elif team.bet=='generale':
                team.bet=500
            else :
                team.bet=int(team.bet)

    for j in players: #donne le nombre des points de chaque Hand nest pas mis a jour par la suite


      total_points+=j.Hand.count_points()

    assert(total_points==152)


  def allowed_cards(self, choosen_color, j):
      """
      return cards allowed to play by the player who has to play
      """

      #cas 1 : la color demandée est atout
      if choosen_color==self.atout :

          #cas 1.1 : a de latout
          if j.Hand.rest[choosen_color]!=0 :
              atouts=[]

          #cas 1.11 : atout plus fort
              for carte in j.Hand.cards :
                  if carte.atout and carte.number!= None and carte.value > self.pli.cards[self.pli.winner()].value : #il faut checké que les cards sont présentes
                      atouts.append(carte)

              if len(atouts)!=0:
                  return Hand("Cards allowed",cards=atouts)

          # cas 1.12 : pas d'atouts plus forts

              return j.Hand.color(choosen_color)

          #cas 1.2 pas d'atout
          return Hand("Cards allowed",cards=j.Hand.cards)
      #cas 2 : la color demandée n'est pas latout

      #case 2.1 : a la color demandée
      if j.Hand.rest[choosen_color]!=0 :
          return j.Hand.color(choosen_color)

      #cas 2.2 : n'a  pas la color demandée

      #cas 2.21 : a atout
      if self.atout in const.liste_couleur[:4]:

          #cas 2.211 : le partenaire mène
          if self.pli.winner()%2==len(self.pli.cards)%2: #permet de se defausser sur partenaire
             return Hand("Cards allowed",cards=j.Hand.cards)


         #cas 2.212 : on doit couper
          if j.Hand.rest[self.atout]!=0 :
              return j.Hand.color(self.atout)

      #cas 2.22 pas datout
      return Hand("Cards allowed",cards=j.Hand.cards)




  def play_pli(self, players, pli_number): #•fonctionne
      """
      prends en entrée le tableau ORDONNEE des players de ce pli et le renvoi réordonné
      """

      #la meilleure card est le 1er joueur pour l'ini

      choosen_color=players[0].Hand.play_card( self.pli, players[0].Hand.choose_card(random=players[0].random))

      for j in players[1:]:
          if not self.hidden :#GRAPHIC
            self.pli.display(j.random)
          allowed_hand=self.allowed_cards( choosen_color, j)
          choosen_card=allowed_hand.choose_card(random=j.random)           # trois lignes a verifier
          j.Hand.play_card( self.pli, choosen_card)
      if not self.hidden :# GRAPHIC
        self.pli.display(self.hidden)

      winner=self.pli.winner()

      if not self.hidden :#GRAPHIC
          print("{} a gagné avec le {} de {}".format(players[winner].name, self.pli.cards[winner].number , self.pli.cards[winner].color ))
      new_order=[players[winner],players[(winner+1)%4], players[(winner+2)%4] ,players[(winner+3)%4]]
      players[winner].plis+=1
      self.teams[players[winner].team].pli+=self.pli #reinitialise le pli
      assert(self.pli.rest["cards"]==0)

       #compter 10 de der
      if pli_number==8 :
          self.teams[players[winner].team].pli.points+=10

      return new_order


def test_choose_atout(): #random test
   myround = Round( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                   team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                   hidden=True,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur]),number=0)
   myround.choose_atout()

def test_cards_update(): #random test
   myround = Round( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                   team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                   hidden=True,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur]),number=0)
   if myround.choose_atout() :
     myround.cards_update()

def test_play_pli(hidden=True): #•fonctionne
   myround = Round( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                   team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                   hidden=True,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur]),number=0)
   if myround.choose_atout() :
     myround.cards_update()
     players=myround.shortkey()
     for i in range(8):
       players=myround.play_pli(pli_number=i,players=players)









if __name__=="__main__"   :

  print("test init and random draw")
  myround = Round( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                   team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True,
                   hidden=False,pioche=Hand(name="pioche",cards=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur]),number=0)

  "check if pioche is empty"

  myround.pli.test("Pli in progress")

  "random draw cards assert that all cards are drawing"
  countinghand=Hand()
  for team in myround.teams :
    for player in team.players :
      assert(len(player.Hand.cards)==player.Hand.rest["cards"]==8)
      countinghand+=player.Hand

  cards_of_pioche=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]

  countinghand.test("Cards",8,8,8,8)

  for i in range(32):
    assert(countinghand.cards[i] not in (countinghand.cards[:i]+countinghand.cards[i+1:])) #check for double
    assert(countinghand.check_card(cards_of_pioche[i]))

  print("test ok")



  print("check classic_drawing ")

  myround.pioche = Hand(name="pioche",cards=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]])
  players=myround.classic_draw()

  "check if pioche is empty"

  myround.pli.test("Pli in progress")

  "check drawing"

  "the order should be"
  "7 8 9 coeur d r 10 pique 7 8 trefle"
  "v d r coeur As pique 7 8 carreau 9 v trefle"
  "10 as coeur 7 pique 9 v d carreau d r trefle"
  "8 9 v pique r 10 as carreau 10 as trefle"
  players_cards=[]
  players_cards.append([Card("7", "coeur"),Card("8", "coeur"),Card("9", "coeur"),
           Card("D", "pique"),Card("R", "pique"),Card("10", "pique"),
           Card("7", "trefle"),Card("8", "trefle")])

  players_cards.append([Card("V", "coeur"),Card("D", "coeur"),Card("R", "coeur"),
           Card("As", "pique"),Card("7", "carreau"),Card("8", "carreau"),
           Card("9", "trefle"),Card("V", "trefle")])

  players_cards.append([Card("10", "coeur"),Card("As", "coeur"),Card("7", "pique"),
           Card("9", "carreau"),Card("V", "carreau"),Card("D", "carreau"),
           Card("D", "trefle"),Card("R", "trefle")])

  players_cards.append([Card("8", "pique"),Card("9", "pique"),Card("V", "pique"),
           Card("R", "carreau"),Card("10", "carreau"),Card("As", "carreau"),
           Card("10", "trefle"),Card("As", "trefle")])

  for p in range(4) :
    myhand=Hand(cards=players[p])
    for i in range(8):
      assert(myhand.check_card(players_cards[p][i]))

  print("test ok")



  print("cut test")

  for nb_of_try in range(100):

    myround.pioche = Hand(name="pioche",cards=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]])
    players=myround.classic_draw(cut=True)

    countinghand=Hand(cards= (players[0]+players[1]+players[2]+players[3]) )
    cards_of_pioche=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur[:4]]

    countinghand.test("Cards",8,8,8,8)


    for i in range(32):
      assert(countinghand.cards[i] not in (countinghand.cards[:i]+countinghand.cards[i+1:])) #check for double
      assert(countinghand.check_card(cards_of_pioche[i]))

  print("test OK")



  print("shortcut test")

  p=myround.shortkey()
  p[1].Hand=Hand(cards=[Card("7","trefle")])
  assert(myround.teams[1].players[0].Hand.check_card(Card("7","trefle")))

  print("test OK")

  print("choose_atout test")
  for i in range(500):
    test_choose_atout()
  print("test OK")

  print("cards_update test")
  for i in range(500):
    test_cards_update()
  print("test OK")

  print("play_pli test")
  for i in range(500):
    test_play_pli()
  print("test OK")




