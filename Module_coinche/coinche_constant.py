#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:32:38 2019

@author: rthiebaut
"""

"""
Constante
"""

liste_numero=['7', '8', '9', 'V', 'D', 'R', '10', 'A']
liste_couleur=['coeur', 'pique', 'carreau', 'trefle',  'sans atout', 'tout atout']
liste_mode=["normal","atout","sans atout","tout atout"]
#attention erreur

normal=[0, 0, 0, 2, 3, 4, 10, 11] 
atout=[0, 0, 14, 20, 3, 4, 10, 11]
sansatout=[0, 0, 0, 2, 3, 4, 10, 19]
toutatout=[0, 0, 9, 14, 1, 2, 5, 7]
liste_point=[normal,atout,sansatout,toutatout]

points={}
j=0
for annonce in liste_mode :    
    points[annonce]={}
    for i in range(8):
        points[annonce][liste_numero[i]]=liste_point[j][i]
    assert(len(points[annonce])==8)
    j+=1
assert(4*sum(points[liste_mode[3]].values())==152)  
assert(4*sum(points[liste_mode[2]].values())==152)
assert(3*sum(points[liste_mode[0]].values())+sum(points[liste_mode[1]].values())==152)   


liste_annonce=[str(80+10*i) for i in range(11)]
liste_annonce.append('capot')
liste_annonce.append('generale')
liste_entier8=[]
for i in range(1,9):
    liste_entier8.append(str(i))
ordre_atout=['7', '8', 'D', 'R', '10', 'A', '9', 'V']