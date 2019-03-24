#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:27:19 2019

@author: rthiebaut
"""

import pygame 
import classes 
import graphic_constant as gconst





def afficher_cartes(screen, cartes):
    for i in range(len(cartes)):
        #dessin_carte(screen,(card_size[0]+2*card_size[0]*i,screen_size[1]-card_size[1]),"valet")
        screen.blit(gconst.image, (gconst.card_size[0]+1/2*gconst.card_size[0]*i,gconst.screen_size[1]-gconst.card_size[1])) #rendre transparent

def dessin_carte(screen,position,nom):
    screen.fill(gconst.WHITE,position+gconst.card_size)


def draw_rect(screen,size,position,color=(255,255,255)):    
    screen.fill(color,position+size)
    

def main():  
    pygame.init() 
    screen=pygame.display.set_mode(gconst.screen_size)
    screen.fill(gconst.GREEN)                   
    while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    break
    
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screen.fill(gconst.GREEN)
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT : 
                draw_rect(screen,gconst.card_size,(0,0))
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
                afficher_cartes(screen,[1,2,3,4,5,6,7,8])
                
            if pygame.mouse.get_pos()[1]>(gconst.screen_size[1]-gconst.card_size[1]) and pygame.mouse.get_pos()[0]>(gconst.card_size[0]) and pygame.mouse.get_pos()[0]<(2*gconst.card_size[0]):
                if  event.type == pygame.MOUSEBUTTONDOWN : 
                    draw_rect(screen,gconst.card_size,(0,0),(0,255,255))
          
            pygame.Surface((100, 100))
            pygame.display.flip()
            
    pygame.quit()
        
main()