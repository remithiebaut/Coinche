#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:27:19 2019

@author: rthiebaut
"""

import pygame 
import graphic_constant as gconst
import coinche_constant as const


'''
from Carte import Carte
from Main import Main

class Graphic_Main(Main):
  
  def __init__(self,name="cartes"):
    Main.__init__(self, name=name)
    
  def jouer_carte(self,pli,carte_choisie, screen, position_table= (gconst.screen_size[1]/2,gconst.screen_size[1]/2)):
   """
   joue la carte choisie et retourne sa couleur affiche cetteaction graphiquement
   """
   Main.jouer_carte(self,pli,carte_choisie)
   carte_choisie.jouer(screen, position_table= position_table)
   delete=self.cartes.index(carte_choisie)
   self.cartes=self.cartes[:delete]+self.cartes[delete+1:]
     
class Graphic_Carte(Carte):
    
  def __init__(self, numero, couleur, position, reste=1):
    Carte.__init__(self, numero, couleur, reste)
    self.image = gconst.list_image[self.ID] 
    self.position=position
    self.hidden=True
  def affichage(self, inverse=False):
      if self.hidden :
        if not inverse :
          return gconst.list_image["Dos"]
        else :
          return gconst.list_image["Dos_inverse"]
      else :
        return self.image
            
  def effacer(self,screen):
       draw_rect(screen, gconst.card_size, self.position, color=gconst.GREEN,)


  def jouer(self, screen, position_table= (gconst.screen_size[1]/2,gconst.screen_size[1]/2)):
    self.effacer(screen)
    screen.blit(self.image,position_table) #rendre transparent
    
'''


def afficher_cartes(screen, cartes):
  """
  Print the hand of cards for each player
  """

  for j in range(1,5):
    if j%2==0:
      inverse=True
    else :
      inverse = False
    for i in range(len(cartes)):
      screen.blit(cartes[i].affichage(inverse), gconst.position["J"+str(j)][i]) #rendre transparent


def draw_rect(screen,size,position,color=(255,255,255)):    
    screen.fill(color,position+size)
    

def test():  
  cartes=[]
  i=0
  for numero in const.liste_numero :
    cartes.append(Graphic_Carte(numero,"carreau", (gconst.position["J1"][i][0],gconst.screen_size[1]-gconst.card_size[1]) ))
    i+=1
  pygame.init() 
  screen=pygame.display.set_mode(gconst.screen_size)
  screen.fill(gconst.GREEN)                   
  while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
            break

    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
       #draw_rect(screen,gconst.position["J1"][1][0] ,gconst.position["J1"][1][1])
        screen.fill(gconst.BLUE,(gconst.card_size[0],gconst.screen_size[1]-gconst.card_size[1],110,110))
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT : 
        draw_rect(screen,gconst.card_size,(0,0))
        
    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
        afficher_cartes(screen, cartes)
        
    if pygame.mouse.get_pos()[1]>(gconst.position["J1"][0][1]):
      for carte in cartes:
        if pygame.mouse.get_pos()[0]>(carte.position[0]) and pygame.mouse.get_pos()[0]<(carte.position[0]+gconst.card_size[0]):
          if  event.type == pygame.MOUSEBUTTONDOWN : 
             carte.jouer(screen)
             delete=cartes.index(carte)
             cartes=cartes[:delete]+cartes[delete+1:]  
    pygame.display.flip()
    
  pygame.quit()

       


test()
