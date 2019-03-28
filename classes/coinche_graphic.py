#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:27:19 2019

@author: rthiebaut
"""

import pygame 
import graphic_constant as gconst
from Carte import Carte

class Graphic_Carte(Carte):
    
    def __init__(self, numero, couleur, position, reste=1):
         Carte.__init__(self, numero, couleur, reste)
         self.image = gconst.list_image[self.ID] 
         self.position=position
         self.hidden=True
    def affichage(self):
        if self.hidden :
            return gconst.list_image["Dos"]
        else :
            return self.image
             
    def effacer(self,screen):
         draw_rect(screen, gconst.card_size, self.position, color=gconst.GREEN,)


    def jouer(self,screen,position_table= (gconst.screen_size[1]/2,gconst.screen_size[1]/2)):
        self.effacer(screen)
        screen.blit(self.image,position_table) #rendre transparent
        



def afficher_cartes(screen, cartes):
    for j in range(1,5):
        for i in range(len(cartes)):
            #dessin_carte(screen,(card_size[0]+2*card_size[0]*i,screen_size[1]-card_size[1]),"valet")
            screen.blit(cartes[i].affichage(), gconst.position["J"+str(j)][i]) #rendre transparent


def dessin_carte(screen,position,nom):
    screen.fill(gconst.WHITE,position+gconst.card_size)


def draw_rect(screen,size,position,color=(255,255,255)):    
    screen.fill(color,position+size)
    

def main(carte):  
    pygame.init() 
    screen=pygame.display.set_mode(gconst.screen_size)
    screen.fill(gconst.GREEN)                   
    while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    break
    
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
               #draw_rect(screen,gconst.position["J1"][1][0] ,gconst.position["J1"][1][1])
                screen.fill(gconst.BLUE,(gconst.card_size[0],gconst.screen_size[1]-gconst.card_size[1],110,110))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT : 
                draw_rect(screen,gconst.card_size,(0,0))
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
                afficher_cartes(screen, [carte,carte2])
                
            if pygame.mouse.get_pos()[1]>(gconst.screen_size[1]-gconst.card_size[1]) and pygame.mouse.get_pos()[0]>(gconst.card_size[0]) and pygame.mouse.get_pos()[0]<(2*gconst.card_size[0]):
                if  event.type == pygame.MOUSEBUTTONDOWN : 
                    #draw_rect(screen,gconst.card_size,(0,0),(0,255,255))
                    carte.jouer(screen)
                    print("got you")
          
            pygame.Surface((100, 100))
            pygame.display.flip()
            
    pygame.quit()

       
carte=Graphic_Carte("V","carreau", (gconst.card_size[0],gconst.screen_size[1]-gconst.card_size[1]) )
carte2=Graphic_Carte("As","coeur", (gconst.card_size[0],gconst.screen_size[1]-gconst.card_size[1]) )

main(carte)
