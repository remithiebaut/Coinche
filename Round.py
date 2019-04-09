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

class Round():
  def __init__(self, team1_name, j1_name, j1_random, j3_name, j3_random,
               team2_name, j2_name, j2_random, j4_name, j4_random, hidden=False): # e1 et e2 inutiles

   self.atout=None
   self.coinche=False #indicator of coinche
   self.surcoinche=False
   self.pli=Hand(name="Pli in progress", sort=False)
   self.pioche =Hand(name="pioche",cards=[Card(i,j) for i in const.liste_numero for j in const.liste_couleur]) #first game
   players=self.random_draw()
   self.teams=[Team(team_name=team1_name, team_number=0, j1_name=j1_name, j1_random=j1_random, j1_cards=players[0],
                      j2_name=j3_name, j2_random=j3_random, j2_cards=players[2]),
                 Team(team_name=team2_name, team_number=1, j1_name=j2_name, j1_random=j2_random, j1_cards=players[1],
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





  def debut(self, joueurs):
      #normal
      if self.atout in const.liste_couleur[:4]:

          for j in joueurs:
              belote=0
              for carte in j.main.cartes:
                  if carte.couleur==self.atout:
                      carte.atout=True
                      carte.valeur=const.ordre_atout.index(carte.numero)
                      carte.points=const.points[const.liste_mode[1]][carte.numero]
                      if carte.numero=="R" or carte.numero=="D":
                          belote+=1
                          if belote==2:
                              print("le joueur {} a la belote".format(j.name)) # achanger pour pas le dire direct a fonctionné deux fois ????
                              self.equipes[j.equipe].pli.points+=20

                  else :
                      carte.valeur=const.liste_numero.index(carte.numero)
                      carte.points=const.points[const.liste_mode[0]][carte.numero]
      #sans atout
      elif self.atout==const.liste_couleur[4]:
          for j in joueurs :
              for carte in j.main.cartes:
                  carte.valeur=const.liste_numero.index(carte.numero)
                  carte.points=const.points[const.liste_mode[2]][carte.numero]

      #tout atout
      elif self.atout==const.liste_couleur[5]:
          for j in joueurs :
              for carte in j.main.cartes:
                  carte.atout=True
                  carte.valeur=const.ordre_atout.index(carte.numero)
                  carte.points=const.points[const.liste_mode[3]][carte.numero]

      total_points=0

      for equipe in self.equipes: #associe la mise a un nombre de points
          if equipe.mise!= None:
              if equipe.mise=='capot':
                  equipe.mise=250
              elif equipe.mise=='generale':
                  equipe.mise=500
              else :
                  equipe.mise=int(equipe.mise)

      for j in joueurs: #donne le nombre des points de chaque main nest pas mis a jour par la suite
          j.main.afficher()
          total_points+=j.main.compter_points()

      assert(total_points==152) #probleme lorrs dune des boucles

  def choisir_atout(manche, aleatoire=True): # pensez a afficher avant surcoinche empecher danooncer 170 180 tout atout sans atout
     """
     fixe l'atout et la mise d'atout et retourne True si tout le monde n'a pas passé
     """
     j=manche.raccourci()
     mise=0
     annonce_actuelle=-1
     tour=0
     while tour!=4 and mise!='generale' and not manche.coinche:
        for joueur in j:
           if tour==4 or mise=='generale' or manche.coinche:
              break
           else:

              joueur.main.afficher(joueur.aleatoire)

              if not generic.decision(aleatoire=joueur.aleatoire, question='annoncer', ouverte=False): #local variable referenced before assignment
                 tour+=1

              else:
                 tour=1

                 manche.atout=generic.decision(const.liste_couleur, aleatoire=joueur.aleatoire, question ="Choisir la couleur d'atout : %s " % const.liste_couleur)

                 while True :

                    mise = generic.decision(const.liste_annonce, aleatoire=joueur.aleatoire, question="Choisir la hauteur d'annonce : %s " % const.liste_annonce )
                    annonce_voulue=const.liste_annonce.index(mise)
                    if annonce_voulue>annonce_actuelle :
                        annonce_actuelle=annonce_voulue
                        print('le joueur {} prend à {} {} !'.format(joueur.name,mise,manche.atout))
                        break

                 manche.equipes[joueur.equipe].mise=mise #fixe la mise de lequipe attention mise est un char
                 manche.equipes[(joueur.equipe+1)%2].mise=None
                 if mise == "generale":
                     joueur.generale=True
                 for coincheur in manche.equipes[(joueur.equipe+1)%2].joueurs:
                   coincheur.main.afficher(coincheur.aleatoire)
                   if not manche.coinche :
                      manche.coinche=generic.decision(aleatoire=coincheur.aleatoire, question='coincher sur {} {} ?'.format(mise,manche.atout), ouverte=False)
                      if manche.coinche:
                         for surcoincheur in manche.equipes[joueur.equipe].joueurs:
                            surcoincheur.main.afficher(surcoincheur.aleatoire)
                            if not manche.surcoinche :
                               manche.surcoinche=generic.decision(aleatoire=surcoincheur.aleatoire, question='surcoincher sur {} {} ?'.format(mise,manche.atout), ouverte=False)
     if (manche.atout==None):
          return False
     for equipe in manche.equipes :
          if equipe.mise!=None:
              print("l'équipe {} a pris {} à {} ".format(equipe.nom, equipe.mise, manche.atout))
     return True

  def raccourci(self): #allège lecriture
       joueurs=[self.equipes[0].joueurs[0],  self.equipes[1].joueurs[0], self.equipes[0].joueurs[1], self.equipes[1].joueurs[1]]
       return joueurs

  def resultat(self,score): # normalement mise nest pas char
      points_totaux=self.equipes[0].pli.compter_points()+self.equipes[1].pli.compter_points()
      assert(points_totaux==162 or points_totaux==182) #compte les points par équipe pas encore de 10 de der
      if self.surcoinche :
          multiplicateur = 4
      elif self.coinche :
          multiplicateur = 2
      else :
          multiplicateur =1

      for equipe in self.equipes :
          if equipe.mise != None:
              capot= equipe.mise==250 and len(equipe.pli.cartes)==32 #bool capot
              generale=(equipe.joueurs[0].plis==8 and equipe.joueurs[0].generale==True ) or ( equipe.joueurs[1].plis==8 and equipe.joueurs[1].generale==True) #bool generale
              #cas 1 : réussite du contrat
              if equipe.mise<=equipe.pli.points or capot or generale : #faire cas général : compteur de pli gagné par joueur
                  print("l'équipe {} a réussit son contrat".format(equipe.nom))

                  #cas 1.1 : coinché ou surcoinché
                  if self.coinche :
                      score[equipe.nom] += equipe.mise*multiplicateur # seulement points contrats
                      score[self.equipes[(equipe.numero+1)%2].nom] += 0 #points defense

                  #cas 1.2 : normal
                  else :
                      score[equipe.nom] += equipe.mise # seulement points contrats
                      score[self.equipes[(equipe.numero+1)%2].nom] += self.equipes[(equipe.numero+1)%2].pli.points #points defense

              #cas 2 : échec du contrat
              else :
                  print("l'équipe {} a chuté ".format(equipe.nom))
                  score[self.equipes[(equipe.numero+1)%2].nom] += 160*multiplicateur

  def cartes_possibles(self, couleur_choisie, j):
      """
      retournes les cartes jouables pour le joueur dont cest le tour dans la self actuelle
      """

      #cas 1 : la couleur demandée est atout
      if couleur_choisie==self.atout :

          #cas 1.1 : a de latout
          if j.main.reste[couleur_choisie]!=0 :
              atouts=[]

          #cas 1.11 : atout plus fort
              for carte in j.main.cartes :
                  if carte.atout and carte.numero!= None and carte.valeur > self.pli.cartes[self.pli.winner()].valeur : #il faut checké que les cartes sont présentes
                      atouts.append(carte)

              if len(atouts)!=0:
                  return atouts

          # cas 1.12 : pas d'atouts plus forts

              return j.main.couleur(couleur_choisie)

          #cas 1.2 pas d'atout
          return j.main.cartes
      #cas 2 : la couleur demandée n'est pas latout

      #case 2.1 : a la couleur demandée
      if j.main.reste[couleur_choisie]!=0 :
          return j.main.couleur(couleur_choisie)

      #cas 2.2 : n'a  pas la couleur demandée

      #cas 2.21 : a atout
      if self.atout in const.liste_couleur[:4]:

          #cas 2.211 : le partenaire mène
          if self.pli.winner()%2==len(self.pli.cartes)%2: #permet de se defausser sur partenaire
             return j.main.cartes

         #cas 2.212 : on doit couper
          if j.main.reste[self.atout]!=0 :
              return j.main.couleur(self.atout)

      #cas 2.22 pas datout
      return j.main.cartes

  def jouer_pli(self,joueurs, nombre_plis, aleatoire=True): #•fonctionne
      """
      prends en entrée le tableau ORDONNEE des joueurs de ce pli et le renvoi réordonné
      """

      #la meilleure carte est le 1er joueur pour l'ini
      couleur_choisie=joueurs[0].main.jouer_carte( self.pli, joueurs[0].main.choisir(aleatoire=joueurs[0].aleatoire))

      for j in joueurs[1:]:
          self.pli.afficher(j.aleatoire)
          cartespossibles=Hand("Cards possibles")
          cartespossibles.add_cartes(self.cartes_possibles( couleur_choisie, j))
          carte_choisie=cartespossibles.choisir(aleatoire=j.aleatoire)           # trois lignes a verifier
          j.main.jouer_carte( self.pli, carte_choisie)
      self.pli.afficher(self.hidden)

      winner=self.pli.winner()
      if not self.hidden :
          print(" Le winner est {} avec le {} de {}".format(joueurs[winner].name, self.pli.cartes[winner].numero , self.pli.cartes[winner].couleur ))
      nouvel_ordre=[joueurs[winner],joueurs[(winner+1)%4], joueurs[(winner+2)%4] ,joueurs[(winner+3)%4]]
      joueurs[winner].plis+=1
      self.equipes[joueurs[winner].equipe].pli.add(self.pli)

       #compter 10 de der
      if nombre_plis==8 :
          self.equipes[joueurs[winner].equipe].pli.points+=10


      self.pli=Hand(self.pli.name) #reinitialise le pli
      return nouvel_ordre

if __name__=="__main__"   :

  myround = Round( team1_name ="Les winners", j1_name="Bob", j1_random=True, j3_name="Fred", j3_random=True,
                   team2_name="Les loseurs", j2_name = "Bill", j2_random=True, j4_name="John", j4_random=True, hidden=False) # e1 et e2 inutiles

  "random draw cards assert that all cards are drawing"
  countinghand=Hand()
  for team in myround.teams :
    for player in team.players :
      assert(len(player.Hand.cards)==player.Hand.rest["cards"]==8)
      countinghand+=player.Hand


  assert(len(countinghand.cards)==32)
  assert(countinghand.points==0)
  assert(countinghand.rest["coeur"]==8)
  assert(countinghand.rest["cards"]==32)
  assert(countinghand.rest["pique"]==8)
  assert(countinghand.rest["trefle"]==8)
  assert(countinghand.rest["carreau"]==8)
  assert(len(countinghand.rest)==5)
  for i in range(32):
    assert(countinghand.cards[i] not in (countinghand.cards[:i]+countinghand.cards[i+1:])) #check for double


  """
  mycard1=Card("7","carreau")
  mycard2=Card("7","coeur")
  myteam=Team(team_name="Les winners", team_number=0, j1_name="Bob", j1_random = True, j1_cards=[mycard1, mycard2],
              j2_name="Fred", j2_random = True, j2_cards=[])

  assert(myteam.number==0)
  assert(myteam.name=="Les winners")
  assert(myteam.bet==None)# == mise


  "pli test"
  assert(myteam.pli.name=="plis de l'equipe 0")
  assert(len(myteam.pli.cards)==0)
  assert(myteam.pli.points==0)
  assert(myteam.pli.rest["coeur"]==0)
  assert(myteam.pli.rest["cards"]==0)
  assert(myteam.pli.rest["pique"]==0)
  assert(myteam.pli.rest["trefle"]==0)
  assert(myteam.pli.rest["carreau"]==0)
  assert(len(myteam.pli.rest)==5)


  "player 1 test"
  assert(myteam.players[0].Hand.name==myteam.players[0].name=="Bob")
  assert(len(myteam.players[0].Hand.cards)==2)
  assert(myteam.players[0].Hand.points==0)
  assert(myteam.players[0].Hand.rest["coeur"]==1)
  assert(myteam.players[0].Hand.rest["cards"]==2)
  assert(myteam.players[0].Hand.rest["pique"]==0)
  assert(myteam.players[0].Hand.rest["trefle"]==0)
  assert(myteam.players[0].Hand.rest["carreau"]==1)
  assert(myteam.players[0].Hand.cards[0].color=="coeur")
  assert(myteam.players[0].Hand.cards[1].color=="carreau")
  assert(len(myteam.players[0].Hand.rest)==5)
  assert(myteam.players[0].plis==0)
  assert(myteam.players[0].team==0)
  assert(myteam.players[0].generale==False)
  assert(myteam.players[0].random==True)


  "player 2 test"

  assert(myteam.players[1].Hand.name==myteam.players[1].name=="Fred")
  assert(len(myteam.players[1].Hand.cards)==0)
  assert(myteam.players[1].Hand.points==0)
  assert(myteam.players[1].Hand.rest["coeur"]==0)
  assert(myteam.players[1].Hand.rest["cards"]==0)
  assert(myteam.players[1].Hand.rest["pique"]==0)
  assert(myteam.players[1].Hand.rest["trefle"]==0)
  assert(myteam.players[1].Hand.rest["carreau"]==0)
  assert(len(myteam.players[1].Hand.rest)==5)
  assert(myteam.players[1].plis==0)
  assert(myteam.players[1].team==0)
  assert(myteam.players[1].generale==False)
  assert(myteam.players[1].random==True)

  myteam.players[1].reinitialize(cards=[mycard1, mycard2])
  assert(myteam.players[1].Hand.name==myteam.players[1].name=="Fred")
  assert(len(myteam.players[1].Hand.cards)==2)
  assert(myteam.players[1].Hand.points==0)
  assert(myteam.players[1].Hand.rest["coeur"]==1)
  assert(myteam.players[1].Hand.rest["cards"]==2)
  assert(myteam.players[1].Hand.rest["pique"]==0)
  assert(myteam.players[1].Hand.rest["trefle"]==0)
  assert(myteam.players[1].Hand.rest["carreau"]==1)
  assert(len(myteam.players[1].Hand.rest)==5)
  assert(myteam.players[1].plis==0)
  assert(myteam.players[1].team==0)
  assert(myteam.players[1].generale==False)
  assert(myteam.players[1].random==True)

  "test reinitialize"
  myteam.reinitialize(j1_cards=[mycard1, mycard2], j2_cards=[])

  assert(myteam.pli.name=="plis de l'equipe 0")
  assert(len(myteam.pli.cards)==0)
  assert(myteam.pli.points==0)
  assert(myteam.pli.rest["coeur"]==0)
  assert(myteam.pli.rest["cards"]==0)
  assert(myteam.pli.rest["pique"]==0)
  assert(myteam.pli.rest["trefle"]==0)
  assert(myteam.pli.rest["carreau"]==0)
  assert(len(myteam.pli.rest)==5)


  assert(myteam.players[0].Hand.name==myteam.players[0].name=="Bob")
  assert(len(myteam.players[0].Hand.cards)==2)
  assert(myteam.players[0].Hand.points==0)
  assert(myteam.players[0].Hand.rest["coeur"]==1)
  assert(myteam.players[0].Hand.rest["cards"]==2)
  assert(myteam.players[0].Hand.rest["pique"]==0)
  assert(myteam.players[0].Hand.rest["trefle"]==0)
  assert(myteam.players[0].Hand.rest["carreau"]==1)
  assert(myteam.players[0].Hand.cards[0].color=="coeur")
  assert(myteam.players[0].Hand.cards[1].color=="carreau")
  assert(len(myteam.players[0].Hand.rest)==5)
  assert(myteam.players[0].plis==0)
  assert(myteam.players[0].team==0)
  assert(myteam.players[0].generale==False)
  assert(myteam.players[0].random==True)


  assert(myteam.players[1].Hand.name==myteam.players[1].name=="Fred")
  assert(len(myteam.players[1].Hand.cards)==0)
  assert(myteam.players[1].Hand.points==0)
  assert(myteam.players[1].Hand.rest["coeur"]==0)
  assert(myteam.players[1].Hand.rest["cards"]==0)
  assert(myteam.players[1].Hand.rest["pique"]==0)
  assert(myteam.players[1].Hand.rest["trefle"]==0)
  assert(myteam.players[1].Hand.rest["carreau"]==0)
  assert(len(myteam.players[1].Hand.rest)==5)
  assert(myteam.players[1].plis==0)
  assert(myteam.players[1].team==0)
  assert(myteam.players[1].generale==False)
  assert(myteam.players[1].random==True)
  """


  print("test OK")
