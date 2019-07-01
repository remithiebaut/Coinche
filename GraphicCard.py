# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 08:46:28 2019

@author: rthie
"""
from Core.Card import Card
import graphic_constant as gconst


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
    screen.fill(color,self.position)

  def play(self, screen, position_table= (gconst.screen_size[1]/2,gconst.screen_size[1]/2)):
    self.erase(screen)
    screen.blit(self.image,position_table) #rendre transparent




if __name__=="__main__"   :
  #Card test
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