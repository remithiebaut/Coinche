# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 17:07:46 2019

@author: rthie
"""
import pygame 
import classes.coinche_constant as const

screen_size=(800,800)
card_size=(int(screen_size[0]/12),int(3/2*(screen_size[0]/12)))   
WHITE=(255,255,255)
RED=(125,0,0)
GREEN=(0,125,0)
BLUE=(0,0,125)
BLACK=(0,0,0)
PURPLE=(125,0,125)
YELLOW=(125,125,0)
CYAN=(0,125,125)

image={}

for numero in const.liste_numero :
    for couleur in const.liste_couleur[:4]:
        ID = numero+couleur    
        image = pygame.image.load('{}.png'.format(ID))
        image = pygame.transform.scale(image,card_size)
        image[ID] = image
