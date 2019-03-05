#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:30:05 2019

@author: rthiebaut
"""
import random #use randrange
import coinche_constant as const
import coinche_function as cfunc 
import generical_function as generic
import coinche_class_main as cmain



class manche():
    def __init__(self,j1,j2,j3,j4,hidden=False): # e1 et e2 inutiles
     
     self.atout=None
     self.coinche=False #indicateur de coinche
     self.surcoinche=False
     self.pli=cmain.main("pli en cours") 
     self.pioche =[ [carte(i,j) for i in const.liste_numero] for j in const.liste_couleur] #ligne = couleur/ colonne= numero
     self.equipes=[equipe(self.pioche,j1,j3,0),equipe(self.pioche,j2,j4,1)] #attention e1 est une variable pose potentiellement probleme
     self.hidden=hidden
     
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
            total_points+=j.main.compter_points()
        print(total_points)
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
                
                affiche_cartes(joueur.main.cartes, joueur.name, joueur.aleatoire )
    
                if not generic.decision(aleatoire=joueur.aleatoire, question='annoncer', ouverte=False): #local variable referenced before assignment
                   tour+=1
    
                else:
                   tour=1
    
                   manche.atout=decision(liste_couleur, aleatoire=joueur.aleatoire, question ="Choisir la couleur d'atout : %s " % liste_couleur)
    
                   while True :
                      
                      mise = decision(liste_annonce, aleatoire=joueur.aleatoire, question="Choisir la hauteur d'annonce : %s " % liste_annonce )
                      annonce_voulue=liste_annonce.index(mise)
                      if annonce_voulue>annonce_actuelle :
                          annonce_actuelle=annonce_voulue
                          print('le joueur {} prend à {} {} !'.format(joueur.name,mise,manche.atout))
                          break
                   
                   manche.equipes[joueur.equipe].mise=mise #fixe la mise de lequipe attention mise est un char
                   manche.equipes[(joueur.equipe+1)%2].mise=None
                   if mise == "generale":
                       joueur.generale=True
                   for coincheur in manche.equipes[(joueur.equipe+1)%2].joueurs:
                     affiche_cartes(coincheur.main.cartes, coincheur.name, coincheur.aleatoire)
                     if not manche.coinche :
                        manche.coinche=decision(aleatoire=coincheur.aleatoire, question='coincher sur {} {} ?'.format(mise,manche.atout), ouverte=False)
                        if manche.coinche:
                           for surcoincheur in manche.equipes[joueur.equipe].joueurs:
                              affiche_cartes(surcoincheur.main.cartes, surcoincheur.name, surcoincheur.aleatoire)
                              if not manche.surcoinche :
                                 manche.surcoinche=decision(aleatoire=surcoincheur.aleatoire, question='surcoincher sur {} {} ?'.format(mise,manche.atout), ouverte=False)              
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
                    if carte.atout and carte.numero!= None and carte.valeur > self.pli.cartes[gain_pli(self.pli)].valeur : #il faut checké que les cartes sont présentes 
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
        if self.atout in liste_couleur[:4]:
            
            #cas 2.211 : le partenaire mène
            if gain_pli(self.pli)%2==len(self.pli.cartes)%2: #permet de se defausser sur partenaire
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
        couleur_choisie=jouer_carte(joueurs[0].main, self.pli, choisir_carte(joueurs[0].main.cartes, joueurs[0].name,aleatoire=joueurs[0].aleatoire))    
    
        for j in joueurs[1:]:
            affiche_cartes(self.pli.cartes, self.pli.name,j.aleatoire)    
            carte_choisie=choisir_carte(cartes_possibles(self, couleur_choisie, j),j.name,aleatoire=j.aleatoire)
            jouer_carte(j.main, self.pli, carte_choisie)
        affiche_cartes(self.pli.cartes, self.pli.name, self.hidden)    
        
        gagnant=gain_pli(self.pli)
        if not self.hidden :
            print(" Le gagnant est {} avec le {} de {}".format(joueurs[gagnant].name, self.pli.cartes[gagnant].numero , self.pli.cartes[gagnant].couleur ))
        nouvel_ordre=[joueurs[gagnant],joueurs[(gagnant+1)%4], joueurs[(gagnant+2)%4] ,joueurs[(gagnant+3)%4]]
        joueurs[gagnant].plis+=1
        self.equipes[joueurs[gagnant].equipe].pli.add(self.pli) 
        
         #compter 10 de der    
        if nombre_plis==8 :
            self.equipes[joueurs[gagnant].equipe].pli.points+=10 
        
            
        self.pli=main(self.pli.name) #reinitialise le pli
        return nouvel_ordre
