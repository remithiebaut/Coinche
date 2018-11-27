# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 23:58:04 2018

@author: rthie le bg
"""

import random
import copy

def indice(liste,element): #trouve l'indice de l'élément dans la liste attention lelement doit etre present
  for i,e in enumerate(liste):
      if e==element:
        return i

def choix(proposition): #souhaitez vous "proposition" ? si oui -> vrai / si non -> false
 x=0
 while not x=='oui' and not x=='non' :
   x=input("Souhaitez-vous %s ? oui/non " % proposition)
 if x=='oui':
   return True
 else:
   return False

def verification(question, conditions) :
    """
    return une proposition qui reponds aux conditions requises
    """
    while True :
        proposition = input(question)
        if proposition in conditions :
            return proposition

liste_numero=['7', '8', '9', '10', 'V', 'D', 'R', 'A']
liste_couleur=['coeur', 'pique', 'carreau', 'trefle',  'sans atout', 'tout atout']
liste_annonce=[str(80+10*i) for i in range(11)]
liste_annonce.append('capot')
liste_annonce.append('generale')
liste_entier8=[]
for i in range(1,9):
    liste_entier8.append(str(i))



class carte():
 def __init__(self, numero, couleur, reste=1):
  self.numero=numero
  self.couleur=couleur
  self.reste=reste


class joueur():
   def __init__(self, pioche, numero_equipe, numero_joueur):
       self.reste={"cartes":0} #changé en dico
       for couleur in liste_couleur[:4]:
           self.reste[couleur]=0
       self.main=[]
       self.equipe=numero_equipe
       self.numero=numero_joueur
       
       #initialise les compteur
       self.reste={"cartes":0} #changé en dico
       for couleur in liste_couleur[:4]:
           self.reste[couleur]=0
       #attention peut poser probleme quand les cartes dun joueur diminue
       while not self.reste["cartes"]==8 :
           x=int(1000*random.random()%8)
           y=int(1000*random.random()%4)
           if pioche[y][x].reste==1:
               self.main.append(pioche[y][x])
               pioche[y][x].reste=0
               self.reste["cartes"]+=1
       tri_couleur(self) #remet les compteurs de couleur à jour


class equipe():
    def __init__(self,pioche,j1, j2, numero_joueur1, numero_joueur2, numero_equipe):
     self.j1=joueur(pioche,numero_equipe,numero_joueur1)
     self.j2=joueur(pioche,numero_equipe,numero_joueur2)
     self.pli=[ [carte(i,j,0) for i in liste_numero] for j in liste_couleur]#a reinitialiser
     self.mise=None                                                #a reinitialiser

class manche():
    def __init__(self,j1="joueur1",j2="joueur2",j3="joueur3",j4="joueur4",e1="e1",e2="e2"):
     self.atout=None
     self.coinche=False #indicateur de coinche
     self.surcoinche=False
     self.pli=[] #pli en cours
     self.pioche =[ [carte(i,j) for i in liste_numero] for j in liste_couleur] #ligne = couleur/ colonne= numero
     self.e1=equipe(self.pioche,j1,j3,1,3,1) #attention e1 est une variable pose potentiellement probleme
     self.e2=equipe(self.pioche,j2,j4,2,4,2)

class partie():
     def __init__(self,j1="joueur1",j2="joueur2",j3="joueur3",j4="joueur4",e1="e1",e2="e2",limite_score=2000):
         self.manche=manche(j1,j2,j3,j4,e1,e2)
         self.limite=limite_score
         self.points=[0,0]


def raccourci(manche): #allège lecriture
     j=[manche.e1.j1, manche.e1.j2, manche.e2.j1, manche.e2.j2]
     return j

def affiche_main(main):
   """
   affiche un tableau de cartes
   """
   for i in range(len(main)):
       if not main[i].numero==None:
        print(str(i+1) + "ème carte : "+ main[i].numero  + " de " + main[i].couleur)
   print()

def choisir_atout(manche):
   """
   fixe l'atout et la mise d'atout
   """
   j=raccourci(manche)
   coinche=manche.coinche
   surcoinche=manche.surcoinche
   mise=0
   annonce_actuelle=-1
   tour=0
   while tour!=4 and mise!='generale' and not coinche:
      for numero_joueur in range(4):
         if tour==4 or mise=='generale' or coinche:
            break
         else:
            print ("Joueur numero ", numero_joueur+1 )
            affiche_main(j[numero_joueur].main)

            if not choix('annoncer'): #local variable referenced before assignment
               tour+=1

            else:
               tour=1
               manche.atout=verification("Choisir la couleur d'atout : %s " % liste_couleur, liste_couleur)

               while True :
                  mise = verification("Choisir la hauteur d'annonce : %s " % liste_annonce , liste_annonce)
                  annonce_voulue=indice(liste_annonce,mise)
                  if annonce_voulue>annonce_actuelle :
                      break

               annonce_actuelle=annonce_voulue


               if numero_joueur%2==0: #faire un tour dans lautre equipe pour coinche
                  manche.e1.mise=mise #fixe la mise de lequipe attention mise est un char

                  for k in [1,3]:
                     affiche_main(j[k].main)
                     if not coinche :
                        coinche=choix('coincher')
                        manche.coinche=coinche
                        if coinche:
                           for l in [0,2]:
                              if not surcoinche :
                                 surcoinche=choix('surcoincher')
                                 manche.surcoinche=surcoinche

               else : #la flemme de généraliser
                  manche.e2.mise=mise #fixe la mise de lequipe attention mise est un char
                  for k in [0,2]:
                     affiche_main(j[k].main)
                     if not coinche :
                        coinche=choix('coincher')
                        manche.coinche=coinche
                        if coinche:
                           for l in [1,3]:
                              if not surcoinche :
                                 surcoinche=choix('surcoincher')
                                 manche.surcoinche=surcoinche







def tri_couleur(joueur):
    """
    on va trier les cartes par couleur et mettre a jour les compteurs de restes
    """
    new_main=[]
    for couleur in liste_couleur[:4] :
        for carte in joueur.main:
            if carte.couleur==couleur:
                new_main.append(carte)
                joueur.reste[couleur]+=1
    joueur.main=new_main

def choisir_carte(main, pli): 
     """
     retourne  carte choisie et sa position dans la main
     """
     affiche_main(main)
     while True :
         position_carte = verification("Quelle carte ? 1ère, 2ème ? ",liste_entier8[:len(main)])
         position_carte = int(position_carte)-1
         if position_carte<len(main) :
             if main[position_carte].numero!=None:
                     pli.append(copy.deepcopy(main[position_carte])) # a priori marche voir doc deepcopy
                     main[position_carte].numero=None 
                     return main[position_carte].couleur


def jouer_pli(manche,joueurs):
    """
    prends en entrée le tableau ORDONNEE des joueurs de ce pli
    """
    couleur_choisie=choisir_carte(joueurs[0].main, manche.pli)

    for j in joueurs[1:]:
        choisir_carte(cartes_possibles(manche, couleur_choisie, j), manche.pli)
    affiche_main(manche.pli)    
    #il faut maintenant determiner le gagnant
   

def cartes_possibles(manche, couleur_choisie, j):
    main_possible=[]
    main_actuelle=j.main+[]
    
    #cas 1 : la couleur demandée est atout
    if couleur_choisie==manche.atout :
        
        #cas 1.1 : a de latout ATTENTION on ne monte pas encore a latout, on utilisera la fonction qui determine le gagnant
        if j.reste[couleur_choisie]!=0 :           #
            for carte in main_actuelle :           #
                if carte.couleur==couleur_choisie: # structure à généraliser !
                    main_possible.append(carte)    #
            return main_possible                   #
        
        #cas 1.2 pas d'atout
        return main_actuelle
    
    #cas 2 : la couleur demandée n'est pas latout   
    
    #case 2.1 : a la couleur demandée
    if j.reste[couleur_choisie]!=0 :
        for carte in main_actuelle:
            if carte.couleur==couleur_choisie:
                main_possible.append(carte)
        return main_possible
    
    #cas 2.2 : n'a  pas la couleur demandée
    
    #cas 2.21 : a atout ATTENTION on ne peut pas encore se defaussersur la carte dun partenaire, on utilisera la fonction qui determine le gagnant
    if j.reste[manche.atout]!=0 :
        for carte in main_actuelle:
            if carte.couleur==manche.atout:
                main_possible.append(carte)
        return main_possible
    
    #cas 2.22 pas datout
    return main_actuelle
        
partie=partie()
j=raccourci(partie.manche)
choisir_atout(partie.manche)
#ini_manche(partie.manche,j)    
jouer_pli(partie.manche, j)
"""
def tour_de_jeu(partie):
   j=raccourci(partie)
   #while j[1].reste["cartes"]>0 and j[2].reste["cartes"]>0 and j[3].reste["cartes"]>0 and j[4].reste["cartes"]>0:
   for a in range(8):
       for joueur in j:
         while condition(carte,partie)==False:
           (carte,numero_carte)=choisir_carte(joueur)
           joueur.main[numero_carte].numero=None
           joueur.reste-=1
         partie.pli[joueur.numero]

def tri_valeur(manche,joueurs):
    for j in joueurs:
        new_main=[]
        for c in couleur[:4]:
            for carte in main:
                if carte.couleur==manche.atout:
                    new_main.append(carte)
        for i in range(8):
            print(new_main[i].valeur)
        return new_main
def ini_manche(manche,joueurs):

    if manche.atout in liste_couleur[:4]:
        for j in joueurs:
            for carte in j.main:
                if carte.couleur==manche.atout:
                    carte.atout=True

"""