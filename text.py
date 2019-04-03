# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 16:00:35 2019

@author: rthie
"""
import pygame 
import graphic_constant as gconst
from Carte import Carte
import coinche_constant as const
from Main import Main


class Game():


  def __init__(self, width=gconst.screen_size[0], height=gconst.screen_size[1], fps=30, background_color=gconst.GREEN):
      """Initialize pygame, window, background, font,...
      """
      pygame.init()
      pygame.display.set_caption("Press ESC to quit")
      self.width = width
      self.height = height
      #self.height = width // 4
      self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF)
      self.background = pygame.Surface(self.screen.get_size()).convert()
      self.color=background_color
      self.background.fill(self.color)
      self.clock = pygame.time.Clock()
      self.fps = fps
      self.playtime = 0.0
      self.screen.blit(self.background, (0, 0))


  def run(self):
    """The mainloop
    """
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            self.draw_text("yo Neggar, I am the one",position="NO")
          elif event.key == pygame.K_RIGHT:
              self.draw_text("ALLAHAKBAH",position="NO")
      self.time()
      pygame.display.flip()
    pygame.quit()
    
  def time(self):
    milliseconds = self.clock.tick(self.fps)
    self.playtime += milliseconds / 1000.0

  def draw_text(self, text, position="mid", color = gconst.BLACK,
                font_type='mono', font_size = 15):
    """
    write text in window
    """
    font = pygame.font.SysFont(font_type, font_size)
    fw, fh = font.size(text) # fw: font width,  fh: font height
    if position=="mid":
      position=((self.width - fw) // 2, (self.height - fh) // 2)  # // makes integer division in python3
    elif position=="NO":
      position=(0 , 0)
    elif position=="NE":
      position=(self.width - fw , 0)
    surface = font.render(text, True, color)
    self.screen.blit(surface, position)

####

if __name__ == '__main__':

    # call with width of window and fps
    Game().run()