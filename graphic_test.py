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
from generical_function import get_mouse,graphic_yesorno,draw_text,wait_or_pass


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
        wait_or_pass(1)

    if event.type == pygame.KEYDOWN and event.key == pygame.K_9 :
        screen.fill(gconst.GREEN)

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP7 :
        screen.fill(gconst.YELLOW,gconst.area["cards"]["j1"][7])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP0 :
        screen.fill(gconst.YELLOW,gconst.area["cards"]["j1"][0])

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP9 :
      choose_atout(screen)

    if event.type == pygame.KEYDOWN and event.key == pygame.K_KP4 :
      result=graphic_yesorno(screen,question="surcoincher ?",question_surface=gconst.area["choice"]["question"],
                      yes_surface=gconst.area["choice"]["yes"],no_surface=gconst.area["choice"]["no"])
      pygame.time.wait(1000)
      screen.fill(gconst.GREEN,gconst.area["middle"])
      draw_text(screen,str(result),gconst.area["middle"])







    pygame.display.flip()


  pygame.quit()


def choose_atout(screen):
    screen.fill(gconst.PURPLE,gconst.area["middle"])

    for announce in gconst.area["announce"]["value"]:
      draw_text(screen,announce,gconst.area["announce"]["value"][announce])
    for announce in gconst.area["announce"]["color"]:
      draw_text(screen,announce,gconst.area["announce"]["color"][announce])
    color=choose_announce(screen,"color")
    value=choose_announce(screen,"value")

    screen.fill(gconst.GREEN,gconst.area["middle"])
    draw_text(screen,value + " " + color,gconst.area["middle"])



def choose_announce(screen,value_or_color):
  assert((value_or_color=="color") or (value_or_color=="value"))
  confirmation_zone=None
  while True :
    event = pygame.event.poll()
    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #escape
      break
    for announce in gconst.area["announce"][value_or_color]:
      if gconst.get_mouse(gconst.area["announce"][value_or_color][announce]):
        if  event.type == pygame.MOUSEBUTTONDOWN :
          if confirmation_zone==gconst.area["announce"][value_or_color][announce] : #second click
            screen.fill(gconst.RED,gconst.area["announce"][value_or_color][announce])
            draw_text(screen,announce,gconst.area["announce"][value_or_color][announce])
            pygame.display.flip()
            return announce
          else :
            if confirmation_zone!=None : # already click elsewhere
              screen.fill(gconst.PURPLE,confirmation_zone)
              draw_text(screen,confirmed_announce,confirmation_zone)
            screen.fill(gconst.YELLOW,gconst.area["announce"][value_or_color][announce])
            draw_text(screen,announce,gconst.area["announce"][value_or_color][announce])
            pygame.display.flip()
            confirmation_zone=gconst.area["announce"][value_or_color][announce] #click once to highligth, click twice to confirm
            confirmed_announce=announce



test()
