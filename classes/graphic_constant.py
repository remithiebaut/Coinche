# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 17:07:46 2019

@author: rthie
"""
import pygame 
import coinche_constant as const

screen_size=(800,800)
card_size=(int(screen_size[0]/10),int(3/2*(screen_size[0]/10)))   
WHITE=(255,255,255)
RED=(125,0,0)
GREEN=(0,125,0)
BLUE=(0,0,125)
BLACK=(0,0,0)
PURPLE=(125,0,125)
YELLOW=(125,125,0)
CYAN=(0,125,125)

position={}

for i in range(1,5):
    position["J"+str(i)]={}
    
for j in range(8):
        #position["J1"][j]=( (screen_size[1],screen_size[1]-card_size[1]), (card_size[0]*j, 2*card_size[0]+card_size[0]*j) )
        position["J1"][j]=(card_size[0]+card_size[0]*j,screen_size[1]-card_size[0])
        position["J2"][j]=(-card_size[0]/2,3*card_size[0]+card_size[0]*j/2)
        position["J3"][j]=(screen_size[0]-4*card_size[0]-card_size[0]*j/2,-card_size[0]/2)
        position["J4"][j]=(screen_size[0]-card_size[0],screen_size[1]-4*card_size[0]-card_size[0]*j/2)




list_image={}

ID ="Dos"   
image = pygame.image.load('images/{}.jpg'.format(ID))
image = pygame.transform.scale(image,card_size)
list_image[ID] = image

ID ="Dos_inverse"   
image = pygame.image.load('images/{}.jpg'.format(ID))
image = pygame.transform.scale(image,(card_size[1],card_size[0]))
list_image[ID] = image

for numero in const.liste_numero :
    for couleur in const.liste_couleur[:4]:
        ID = numero+couleur    
        image = pygame.image.load('images/{}.jpg'.format(ID))
        image = pygame.transform.scale(image,card_size)
        list_image[ID] = image

