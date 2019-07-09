# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 17:07:46 2019

@author: rthie
"""
import pygame 
import coinche_constant as const

resolution=(16*2,9*2) #32*18 cell
cell_size=(43,43)
screen_size=(resolution[0]*cell_size[0],resolution[1]*cell_size[1])


card_size=(int(2*cell_size[0]),int(3*cell_size[0]))

WHITE=(255,255,255)
RED=(125,0,0)
GREEN=(0,125,0)
BLUE=(0,0,125)
BLACK=(0,0,0)
PURPLE=(125,0,125)
YELLOW=(125,125,0)
CYAN=(0,125,125)

#grid definition
grid=[]

for line in range(resolution[0]):
  grid.append([])
  for col in range(resolution[1]):
    grid[line].append((cell_size[0]*line,cell_size[1]*col)+cell_size)

def surface(x1,y1,x2,y2) :
  """
  prends les coordonnées des deux carreaux de la grille et renvoie la surface correspondante
  """
  return((grid[x1][y1][0],grid[x1][y1][1],(1+x2-x1)*cell_size[0],(1+y2-y1)*cell_size[1]))
  


#areas definition

area={}

area["points"]=surface(0,0,9,3)

area["middle"]=surface(11,4,23,13)

area["j1"]=surface(8,15,23,17)

area["j2"]=surface(0,8,1,15)

area["j3"]=surface(11,0,18,1)

area["j4"]=surface(30,8,31,15)


area["cards"]={"board":{}}

area["cards"]["board"]["j1"]=(area["middle"][0]+int(area["middle"][2]/2),area["middle"][1]+int(area["middle"][3]/2),card_size[0],card_size[1])
area["cards"]["board"]["j2"]=(area["middle"][0]+card_size[0],area["middle"][1],card_size[0],card_size[1])
area["cards"]["board"]["j3"]=(area["middle"][0]+card_size[0],area["middle"][1],card_size[0],card_size[1])
area["cards"]["board"]["j4"]=(area["middle"][0]+card_size[0],area["middle"][1],card_size[0],card_size[1])



for i in range(1,5):
    area["cards"]["j"+str(i)]={}


    
for j in range(8):
        area["cards"]["j1"][j]=(area["j1"][0]+card_size[0]*j,area["j1"][1],card_size[0],card_size[1])
        area["cards"]["j2"][j]=(area["j2"][0],area["j2"][1]+card_size[0]/2*j,card_size[1],card_size[0])
        area["cards"]["j3"][j]=(area["j3"][0]+card_size[0]/2*j,area["j3"][1],card_size[0],card_size[1])
        area["cards"]["j4"][j]=(area["j4"][0],area["j4"][1]+card_size[0]/2*j,card_size[1],card_size[0])
        '''
        (card_size[0]+card_size[0]*j,screen_size[1]-card_size[0])
        area["cards"]["J2"][j]=(-card_size[0]/2,3*card_size[0]+card_size[0]*j/2)
        area["cards"]["J3"][j]=(screen_size[0]-4*card_size[0]-card_size[0]*j/2,-card_size[0]/2)
        area["cards"]["J4"][j]=(screen_size[0]-card_size[0],screen_size[1]-4*card_size[0]-card_size[0]*j/2)
'''

#picture load

list_picture={}

ID ="Dos"   
image = pygame.image.load('images/{}.jpg'.format(ID))
image = pygame.transform.scale(image,card_size)
list_picture[ID] = image

ID ="Dos_inverse"   
image = pygame.image.load('images/{}.jpg'.format(ID))
image = pygame.transform.scale(image,(card_size[1],card_size[0]))
list_picture[ID] = image

for numero in const.liste_numero :
    for couleur in const.liste_couleur[:4]:
        ID = numero+couleur    
        image = pygame.image.load('images/{}.jpg'.format(ID))
        image = pygame.transform.scale(image,card_size)
        list_picture[ID] = image

