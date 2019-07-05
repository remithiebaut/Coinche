# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 08:46:28 2019

@author: rthie
"""
from Card import Card
import graphic_constant as gconst

import pygame 
import coinche_constant as const


class GraphicCard(Card):
    
  def __init__(self, number, color, rest=True, position=None):
    Card.__init__(self, number=number, color=color, rest=rest)
    self.picture = gconst.list_picture[self.ID] 
    self.position=position
    self.hidden=True
    
  def display(self, inverse=False):
      if self.hidden :
        if not inverse :
          return gconst.list_picture["Dos"] #J3
        else :
          return gconst.list_picture["Dos_inverse"] #J4 J5
      else : #J1 and board
        return self.picture
            
  def erase(self,screen,color=gconst.GREEN):
    """
    erase the given position
    """
    screen.fill(color,self.position)

  def play(self, screen, new_position):
    """
    play the card at a given position
    """
    self.erase(screen)
    self.position=new_position
    screen.blit(self.picture,new_position) #rendre transparent


def test_graphic_card():  
  cards=[]
  i=0
  for numero in const.liste_numero :
    cards.append(GraphicCard(numero,"carreau", position=gconst.area["cards"]["j1"][i]))
    i+=1
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
        screen.fill(gconst.BLUE,(gconst.card_size[0],gconst.screen_size[1]-gconst.card_size[1],110,110))
        
    if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        screen.fill(gconst.BLUE,gconst.grid[31][17])
        
        """
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT : 
        draw_rect(screen,gconst.card_size,(0,0))
        
    if event.type == pygame.KEYDOWN and event.key == pygame.K_UP :
      
        afficher_cartes(screen, cartes)
        """
    #if pygame.mouse.get_pos()[1]<(gconst.area["cards"]["J1"][1]):
    for card in cards:
      mouse=pygame.mouse.get_pos()
      if mouse[0]>card.position[0] and mouse[0]<(card.position[0]+card.position[2]) and mouse[1]>card.position[1] and mouse[1]<(card.position[1]+card.position[3]):
        if  event.type == pygame.MOUSEBUTTONDOWN : 
          
           card.play(screen,gconst.area["cards"]["board"]["j1"])
           delete=cards.index(card)
           cards=cards[:delete]+cards[delete+1:]
              
             
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
    pygame.display.flip()
    
  pygame.quit()

       








if __name__=="__main__"   :
  print("Card test")
  mycard=GraphicCard("7","coeur")
  mycard2=GraphicCard("7","coeur",False)
  assert(mycard2.number=="7")
  assert(mycard2.color=="coeur")
  assert(mycard2.rest==False)
  assert(mycard.number=="7")
  assert(mycard.color=="coeur")
  assert(mycard.rest==True)
  assert(mycard.value==None)
  assert(mycard.points==0)
  assert(mycard.ID=="7coeur")

  print("test OK")
  
  print("Graphic test")

  test_graphic_card()

  print("test OK")
