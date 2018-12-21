#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 16:19:07 2018

@author: rthiebaut
"""

import pygame 

card_size=(40,30)  


def draw_rect(screen,size,position,color=(255,255,255)):    
    screen.fill(color,position+size)
    







    

def main():  
    pygame.init() 
    screen=pygame.display.set_mode((1000,1000))
    screen.fill((0,0,0))                   
    while True:
            rectangle=pygame.Rect(0,0,40,30)
            event = pygame.event.poll()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    break
    
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                screen.fill((255,0,0))
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT : 
                draw_rect(screen,card_size,(0,0))
            pygame.display.flip()
            
    pygame.quit()
        
main()