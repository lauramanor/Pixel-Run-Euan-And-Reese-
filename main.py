import pygame 
import sys 
from lvl1 import *

pygame.init() 
pygame.font.init()
pygame.mixer.init()
def menu():
  mixer.music.load("menuMusic.wav")
  mixer.music.play(-1)
  
  res = (1200,720) 
  bgg = (5,100,120)
  textc=(10,255,10)
  screen = pygame.display.set_mode(res) 
  color = (255,255,255) 
    
  color_light = (0,170,170) 
    
  color_dark = (0,100,100) 
    
  width = screen.get_width() 
   
  height = screen.get_height() 

  smallfont = pygame.font.SysFont('Corbel',35) 
  
  text = smallfont.render('Play!' , True , color) 
  pygame.display.update()
  
    
  while True: 
        
      for ev in pygame.event.get(): 
            
          if ev.type == pygame.QUIT: 
              pygame.quit() 
                
        
          if ev.type == pygame.MOUSEBUTTONDOWN: 
                
      
              if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                   main() 
                    
          screen.blit(heheha, [0, 0])          
        
      mouse = pygame.mouse.get_pos() 
        
      if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
          pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 
            
      else: 
          pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 
      screen.blit(text , (width/2+50,height/2)) 
      pygame.display.update()
main2()