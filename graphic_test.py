#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:27:19 2019

@author: rthiebaut
"""

import pygame
import graphic_constant as gconst
import coinche_constant as const
from GraphicCard import GraphicCard
from generical_function import get_mouse,graphic_yesorno,draw_text


def draw_pos(screen,size,position,color=(255,255,255)):
    screen.fill(color,position+size)


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
  """
  for numero in const.liste_numero :
    cartes.append(GraphicCard(numero,"carreau", (gconst.position["J1"][i][0],gconst.screen_size[1]-gconst.card_size[1]) ))
    i+=1
  """
  pygame.init()
  screen=pygame.display.set_mode(gconst.screen_size)
  screen.fill(gconst.GREEN)

  while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
            break
    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT: #test
      screen.fill(gconst.YELLOW,(100,100,100,100))

    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
       #draw_rect(screen,gconst.position["J1"][1][0] ,gconst.position["J1"][1][1])
        screen.fill(gconst.BLUE,(gconst.card_size[0],gconst.screen_size[1]-gconst.card_size[1],110,110))

    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
       #draw_rect(screen,gconst.position["J1"][1][0] ,gconst.position["J1"][1][1])
        screen.fill(gconst.BLUE,gconst.grid[31][17])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT :
        draw_rect(screen,gconst.card_size,(0,0))
        """
    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :

        afficher_cartes(screen, cartes)

    if pygame.mouse.get_pos()[1]<(gconst.area["cards"]["J1"][1]):
      for carte in cartes:
        if pygame.mouse.get_pos()[0]>(carte.position[0]) and pygame.mouse.get_pos()[0]<(carte.position[0]+gconst.card_size[0]):
          if  event.type == pygame.MOUSEBUTTONDOWN :

             carte.jouer(screen)
             delete=cartes.index(carte)
             cartes=cartes[:delete]+cartes[delete+1:]
            """

    if event.type == pygame.KEYDOWN and event.key == pygame.K_1 :
        screen.fill(gconst.BLUE,gconst.area["j1"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_2 :
        screen.fill(gconst.BLUE,gconst.area["j2"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_3 :
        screen.fill(gconst.BLUE,gconst.area["j3"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_4 :
        screen.fill(gconst.BLUE,gconst.area["j4"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_5 :
        screen.fill(gconst.BLUE,gconst.area["middle"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_6 :
        screen.fill(gconst.BLUE,gconst.area["points"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_7 :
        screen.fill(gconst.BLUE,gconst.area["test"])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_9 :
        screen.fill(gconst.GREEN)

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP7 :
        screen.fill(gconst.YELLOW,gconst.area["cards"]["J1"][7])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP0 :
        screen.fill(gconst.YELLOW,gconst.area["cards"]["J1"][0])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP9 :
      choose_atout(screen)

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP4 :
      result=graphic_yesorno(screen,question="surcoincher ?",question_surface=gconst.area["choice"]["question"],
                      yes_surface=gconst.area["choice"]["yes"],no_surface=gconst.area["choice"]["no"])
      screen.fill(gconst.GREEN,gconst.area["middle"])
      draw_text(screen,str(result),gconst.area["middle"])





    pygame.display.flip()


  pygame.quit()


def choose_atout(screen):
    screen.fill(gconst.PURPLE,gconst.area["middle"])
    end=False
    while not end :
       event = pygame.event.poll()
       if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
         break
       if gconst.get_mouse(gconst.area["middle"]):
        if  event.type == pygame.MOUSEBUTTONDOWN :
          screen.fill(gconst.GREEN,gconst.area["middle"])
          end=True
       pygame.display.flip()



test()
