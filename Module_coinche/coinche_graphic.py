#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:27:19 2019

@author: rthiebaut
"""

import pygame 
import jeu_de_coinche


screen_size=(955,1000)
card_size=(int(screen_size[0]/12),int(3/2*(screen_size[0]/12)))   
WHITE=(255,255,255)
RED=(125,0,0)
GREEN=(0,125,0)
BLUE=(0,0,125)
image = pygame.image.load('v_carreau.png')
image=pygame.transform.scale(image,card_size)

def afficher_cartes(screen, cartes):
    for i in range(len(cartes)):
        #dessin_carte(screen,(card_size[0]+2*card_size[0]*i,screen_size[1]-card_size[1]),"valet")
        screen.blit(image, (card_size[0]+1/2*card_size[0]*i,screen_size[1]-card_size[1])) #rendre transparent

def dessin_carte(screen,position,nom):
    screen.fill(WHITE,position+card_size)


def draw_rect(screen,size,position,color=(255,255,255)):    
    screen.fill(color,position+size)
    

def main():  
    pygame.init() 
    screen=pygame.display.set_mode(screen_size)
    screen.fill(GREEN)                   
    while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    break
    
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screen.fill(GREEN)
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT : 
                draw_rect(screen,card_size,(0,0))
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
                afficher_cartes(screen,[1,2,3,4,5,6,7,8])
                
            if pygame.mouse.get_pos()[1]>(screen_size[1]-card_size[1]) and pygame.mouse.get_pos()[0]>(card_size[0]) and pygame.mouse.get_pos()[0]<(2*card_size[0]):
                if  event.type == pygame.MOUSEBUTTONDOWN : 
                    draw_rect(screen,card_size,(0,0),(0,255,255))
          
            pygame.Surface((100, 100))
            pygame.display.flip()
            
    pygame.quit()
        
main()