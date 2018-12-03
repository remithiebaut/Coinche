# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 23:58:04 2018

@author: rthie le bg
"""

import random
import copy
import sys


def indice(liste,element): #trouve l'indice de l'élément dans la liste attention lelement doit etre present
  for i,e in enumerate(liste):
      if e==element:
        return i

def choix(proposition): #rajout dun quit
  """  
  souhaitez vous "proposition" ? si oui -> vrai / si non -> false
  """
  while True :
       x=input("Souhaitez-vous %s ? oui/non " % proposition)
       if x=='quit':
           sys.exit()
       if x=='oui' or x=='non' :
           break
  if x=='oui':
      return True
  else :
      return False

def verification(question, conditions) : #rajout dun quit
    """
    return une proposition qui reponds aux conditions requises
    """
    while True :
        proposition = input(question)
        if proposition=="quit":
            sys.exit()
        if proposition in conditions :
            return proposition

liste_numero=['7', '8', '9', 'V', 'D', 'R', '10', 'A']
liste_couleur=['coeur', 'pique', 'carreau', 'trefle',  'sans atout', 'tout atout']
liste_annonce=["normal","atout","sans atout","tout atout"]

#attention erreur

liste_point[tout_atout]=[0, 0, 9, 14, 1, 2, 5, 7]
assert(4*sum(liste_point_tout_atout))==152 and len(liste_point_tout_atout)==8

liste_point[sans_atout]=[0, 0, 0, 2, 3, 4, 10, 19]
assert(4*sum(liste_point_sans_atout))==152 and len(liste_point_sans_atout)==8

liste_point["normal"]=[0, 0, 0, 2, 3, 4, 10, 11] 
liste_point["atout"]=[0, 0, 14, 20, 3, 4, 10, 11]
assert(3*sum(liste_point)+sum(liste_point_atout))==152 and len(liste_point_atout)==8 and len(liste_point)==8




points={}
for annonce in liste_annonce :
    points[annonce]={}
    j=0
    for numero in liste_numero:
        points[annonce][numero]=liste_point[annonce]+j
        j+=1
    

liste_annonce=[str(80+10*i) for i in range(11)]
liste_annonce.append('capot')
liste_annonce.append('generale')
liste_entier8=[]
for i in range(1,9):
    liste_entier8.append(str(i))
ordre_atout=['7', '8', 'D', 'R', '10', 'A', '9', 'V']



class carte():
 def __init__(self, numero, couleur, reste=1):
  self.numero=numero #prend la valeur none quand inexistant
  self.couleur=couleur
  self.reste=reste #utilisé seulement dans la distribution de cartes, lutiliser a la place de none ?
  self.valeur=None #ordre de puissance dans lannonce actuelle 16 valet datout et 1:7 normal
  self.atout=False
  self.points=0
  
class main():
    def __init__(self,name): 
       self.name=name
       self.cartes=[]     
       #initialise les compteur
       self.reste={"cartes":0} #changé en dico
       for couleur in liste_couleur[:4]:
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
        for couleur in liste_couleur[:4] :
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


class joueur():
   def __init__(self, pioche, numero_equipe, name):
       
       self.name=name
       self.main=main(name)
       self.main.piocher(pioche)
       self.equipe=numero_equipe
       
       



class equipe():
    def __init__(self,pioche, name1, name2, numero_equipe):
     
     self.j1=joueur(pioche,numero_equipe,name1)
     self.j2=joueur(pioche,numero_equipe,name2)
     self.pli=main("pli de l'equipe " + str(numero_equipe)) #a reinitialiser
     self.mise=None  #a reinitialiser




class manche():
    def __init__(self,j1,j2,j3,j4,e1,e2): # e1 et e2 inutiles
     
     self.atout=None
     self.coinche=False #indicateur de coinche
     self.surcoinche=False
     self.pli=main("pli en cours") 
     self.pioche =[ [carte(i,j) for i in liste_numero] for j in liste_couleur] #ligne = couleur/ colonne= numero
     self.equipe=(equipe(self.pioche,j1,j3,0),equipe(self.pioche,j2,j4,1)) #attention e1 est une variable pose potentiellement probleme
   
    def debut(self, joueurs):
        #normal
        if self.atout in liste_couleur[:4]:
            for j in joueurs:
                for carte in j.main.cartes:
                    if carte.couleur==self.atout:
                        carte.atout=True
                        carte.valeur=indice(ordre_atout,carte.numero)
                        carte.points=liste_point_atout[carte.numero]
                    else :
                        carte.valeur=indice(liste_numero,carte.numero)
                        carte.points=liste_point[carte.numero]
        #sans atout
        elif self.atout==liste_couleur[4]:
            for j in joueurs :
                for carte in j.main.cartes:
                    carte.valeur=indice(liste_numero,carte.numero)
                    carte.points=liste_point_sans_atout[carte.numero]
        
        #tout atout
        elif self.atout==liste_couleur[5]:
            for j in joueurs :
                for carte in j.main.cartes:
                    carte.atout=True
                    carte.valeur=indice(ordre_atout,carte.numero)
                    carte.points=liste_point_tout_atout[carte.numero]
        
        
        
    def raccourci(self): #allège lecriture
         j=[self.equipe[0].j1,  self.equipe[1].j1, self.equipe[0].j2, self.equipe[1].j2]
         return j

class partie():
     def __init__(self,j1="joueur1",j2="joueur2",j3="joueur3",j4="joueur4",e1="e1",e2="e2",limite_score=2000):
         
         self.manche=manche(j1,j2,j3,j4,e1,e2)
         self.limite=limite_score
         self.points=[0,0]





def affiche_cartes(cartes,name="cartes"):
   """
   affiche un tableau de cartes
   """
   print("\n \n {:^15} \n".format(name))
   for i in range(len(cartes)):
       if not cartes[i].numero==None :
        print("{} : {:>2} de {} ".format(str(i+1),cartes[i].numero,cartes[i].couleur))
   print()








def choisir_atout(manche): # pensez a afficher avant surcoinche
   """
   fixe l'atout et la mise d'atout
   """
   j=manche.raccourci()
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
            affiche_cartes(j[numero_joueur].main.cartes, j[numero_joueur].name )

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
                  manche.equipe[0].mise=mise #fixe la mise de lequipe attention mise est un char

                  for k in [1,3]:
                     affiche_cartes(j[k].main.cartes, j[k].name)
                     if not coinche :
                        coinche=choix('coincher')
                        manche.coinche=coinche
                        if coinche:
                           for l in [0,2]:
                              if not surcoinche :
                                 surcoinche=choix('surcoincher')
                                 manche.surcoinche=surcoinche

               else : #la flemme de généraliser
                  manche.equipe[1].mise=mise #fixe la mise de lequipe attention mise est un char
                  for k in [0,2]:
                     affiche_cartes(j[k].main.cartes, j[k].name)
                     if not coinche :
                        coinche=choix('coincher')
                        manche.coinche=coinche
                        if coinche:
                           for l in [1,3]:
                              if not surcoinche :
                                 surcoinche=choix('surcoincher')
                                 manche.surcoinche=surcoinche









def choisir_carte(cartes,nom): 
     """
     choisie et retourne une carte
     """
     affiche_cartes(cartes,nom)
     while True :
         position_carte = verification("Quelle carte ? 1ère, 2ème ? ",liste_entier8[:len(cartes)])
         position_carte = int(position_carte)-1
         if position_carte<len(cartes) :
             if cartes[position_carte].numero!=None:
                 return cartes[position_carte]

def jouer_carte(main,pli,carte_choisie):
     """
     joue la carte choisie et retourne sa couleur
     """
     pli.cartes.append(copy.deepcopy(carte_choisie)) # a priori marche voir doc deepcopy
     couleur_choisie=carte_choisie.couleur
     pli.reste[couleur_choisie]+=1
     pli.reste["cartes"]+=1
     main.reste[couleur_choisie]-=1
     main.reste["cartes"]-=1
     carte_choisie.numero=None 
     
     return couleur_choisie                 
    


def cartes_possibles(manche, couleur_choisie, j):
    
    cartes_possible=[]
    
    #cas 1 : la couleur demandée est atout
    if couleur_choisie==manche.atout : 
        
        #cas 1.1 : a de latout ATTENTION on ne monte pas encore a latout, on utilisera la fonction qui determine le gagnant
        if j.main.reste[couleur_choisie]!=0 :           #
            for carte in j.main.cartes :           #
                if carte.couleur==couleur_choisie: # structure à généraliser !
                    cartes_possible.append(carte)    #
            return cartes_possible                   #
        
        #cas 1.2 pas d'atout
        return j.main.cartes
    #cas 2 : la couleur demandée n'est pas latout   
    
    #case 2.1 : a la couleur demandée
    if j.main.reste[couleur_choisie]!=0 :
        for carte in j.main.cartes:
            if carte.couleur==couleur_choisie:
                cartes_possible.append(carte)
        return cartes_possible
    
    #cas 2.2 : n'a  pas la couleur demandée
    
    #cas 2.21 : a atout ATTENTION on ne peut pas encore se defaussersur la carte dun partenaire, on utilisera la fonction qui determine le gagnant
    if manche.atout in liste_couleur[:4]:
        if j.main.reste[manche.atout]!=0 :
            for carte in j.main.cartes:
                if carte.atout: 
                    cartes_possible.append(carte)
            return cartes_possible
    
    #cas 2.22 pas datout
    return j.main.cartes


def gain_pli(pli): 
    """
    donne lindice du gagnant du pli dans lordre du pli
    """
    gagnant=pli.cartes[0]
    for carte in pli.cartes:
        if not gagnant.atout:
            if carte.atout :
                gagnant=carte
            elif gagnant.couleur==carte.couleur and carte.valeur>gagnant.valeur:
                gagnant=carte
        
        else :
            if carte.valeur>gagnant.valeur:
                gagnant=carte
    return indice(pli.cartes,gagnant)




def jouer_pli(manche,joueurs): #•fonctionne
    """
    prends en entrée le tableau ORDONNEE des joueurs de ce pli et le renvoi réordonné
    """
    
    #la meilleure carte est le 1er joueur pour l'ini
    couleur_choisie=jouer_carte(joueurs[0].main, manche.pli, choisir_carte(joueurs[0].main.cartes, joueurs[0].name))

    for j in joueurs[1:]:
        affiche_cartes(j.main.cartes, j.name)
        carte_choisie=choisir_carte(cartes_possibles(manche, couleur_choisie, j),j.name)
        jouer_carte(j.main, manche.pli, carte_choisie)
    affiche_cartes(manche.pli.cartes, manche.pli.name)    
    
    gagnant=gain_pli(manche.pli)
    print(" Le gagnant est {} avec le {} de {}".format(joueurs[gagnant].name, manche.pli.cartes[gagnant].numero , manche.pli.cartes[gagnant].couleur ))
    nouvel_ordre=[joueurs[gagnant],joueurs[(gagnant+1)%4], joueurs[(gagnant+2)%4] ,joueurs[(gagnant+3)%4]]
    manche.equipe[joueurs[gagnant].equipe].pli.add(manche.pli) # trouver methode pour que les plis sajoutent pour linstant ils se remplacent
    manche.pli=main(manche.pli.name) #reinitialise le pli

    return nouvel_ordre
                    
                
        
partie=partie(j1="Remi",j2="Vincent",j3="Pierre",j4="Guilhem")
j=partie.manche.raccourci()
choisir_atout(partie.manche) #choisir valeur par defaut pour les test
partie.manche.debut(j)
for i in range(8):
    print("pli {} : \n \n".format(i))
    j=jouer_pli(partie.manche, j) #erreur dans le decompte des plis confusion avec les tas joueur bug a iteration2 a priori fonctionne : confusion entre la position dans la main et celles des cartes possibles
    for k in range(2):
        affiche_cartes(partie.manche.equipe[k].pli.cartes, partie.manche.equipe[k].pli.name)


print("FIN")   
while True :
    a=0
        
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

def ini_manche(manche, joueurs):
    if manche.atout in liste_couleur[:4]:
        for j in joueurs:
            for carte in j.main:
                if carte.couleur==manche.atout:
                    carte.atout=True

for joueur in j:
    affiche_cartes(joueur.main.cartes,joueur.name,toutes=True)
    for carte in joueur.main.cartes:
        print(carte.points)
"""