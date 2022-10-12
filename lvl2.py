import pygame, numpy
from pygame import mixer
import time
import random
from lvl2 import *
coinincorner=pygame.image.load("p1_Coin.png")
deathcycle=["(insert death remark here)","Do you need glasses?","Sucks to suck",".-. ","Pixelated"]
pygame.init()
pygame.font.init()
pygame.mixer.init() 
heheheheha= pygame.image.load("skell.png")
heheheha= pygame.image.load("winScreen.png")
heheha= pygame.image.load("menuScreen2.png")
bg = pygame.image.load("BAGROUND.png")
epik= pygame.mixer.Sound("epik.wav")
CoinS= pygame.mixer.Sound("CoinCollect.wav")
JumpS= pygame.mixer.Sound("jumpSound.wav")
GGS= pygame.mixer.Sound("GG.wav")


WIDTH = 2500
HEIGHT = 900
BACKGROUND = (50, 50, 255)
COINCOUNT = 0
DEATHCOUNT = 0
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx, starty):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.center = [startx, starty]

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self, dx, dy):
        self.rect.move_ip([dx, dy])


class Coin(Sprite):
    def __init__(self, startx, starty):
        super().__init__("p1_Coin.png", startx, starty)
        self.x = startx
        self.y = starty
        self.coin_cycle = [
            pygame.image.load(f"CoinAnim/Spin_{i:0>2}.png") for i in range(1, 9)
        ]

        self.coin_animation_index = 0
    def move_to_corner(self):
      CoinS.play()
      self.rect.move_ip([WIDTH, -25])
      # COINCOUNT+=1
      pygame.display.update()
      # print(COINCOUNT)

    def coin_animation(self, x, y):
        self.image = self.coin_cycle[self.coin_animation_index]
        if self.coin_animation_index < len(self.coin_cycle) - 1:
            self.coin_animation_index += 1
        else:
            self.coin_animation_index = 0

class Enemy(Sprite):
    def __init__(self, startx, starty):
        super().__init__("God.png", startx, starty)
        self.x = startx
        self.y = starty 
class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("p1_front02.png", startx, starty)
        self.stand_image = self.image
        self.jump_cycle = pygame.image.load("p2_jump02.png")

        self.walk_cycle = [
            pygame.image.load(f"p2_walkAnim/p2_walk{i:0>2}.png") for i in range(1, 7)
        ]

        self.animation_index = 0
        self.facing_left = False

        self.speed = 8
        self.jumpspeed = 10
        self.vsp = 0
        self.gravity = 0.22
        self.min_jumpspeed = 4
        self.prev_key = pygame.key.get_pressed()
        self.is_alive = True

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle) - 1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        self.image = self.jump_cycle
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, groups):
        hsp = 0
        onground = self.check_collision(0, 1, groups['box'])

        while self.check_collision(0, 1, groups['coin']):
            coin = pygame.sprite.spritecollide(self, groups['coin'], False)
            coin[0].move_to_corner()
          

        while self.check_collision(0, 1, groups['lava']):
        
            self.is_alive = False
            lava = pygame.sprite.spritecollide(self, groups['lava'], False)
            mixer.music.set_volume(0.1)
            m=mixer.music.load("DEATHSOUND.wav")
            mixer.music.play(1)
            reset()
            time.sleep(1)
          
            main2()
        while self.check_collision(0, 1, groups['enemy']):
        
            self.is_alive = False
            lava = pygame.sprite.spritecollide(self, groups['enemy'], False)
            main2()
        while self.check_collision(0, 1, groups['death']): 
            self.is_alive = False
            death = pygame.sprite.spritecollide(self, groups['death'], False)
            mixer.music.set_volume(0.3)
            m=mixer.music.load("DEATHSOUND.wav")
            mixer.music.play(1)
            reset()
            time.sleep(1)
            main2()
        while self.check_collision(0, 1, groups['spike']):
            self.is_alive = False
            spike = pygame.sprite.spritecollide(self, groups['spike'], False)
            mixer.music.set_volume(0.3)
            m=mixer.music.load("DEATHSOUND.wav")
            mixer.music.play(1)
            reset()
            time.sleep(1)
            main2()
        while self.check_collision(0, 1, groups['GG']):
            GG = pygame.sprite.spritecollide(self, groups['GG'], False)
  
            End()
            time.sleep(2)
            epik.play(-1)
            time.sleep(4200)
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.walk_animation()
            hsp = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.walk_animation()
            hsp = self.speed
        else:
            self.image = self.stand_image

        if key[pygame.K_UP] and onground:
            JumpS.play()
            self.vsp = -self.jumpspeed


        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed

        self.prev_key = key

        
        if self.vsp < 10 and not onground:  

            self.jump_animation()
            self.vsp += self.gravity

        if onground and self.vsp > 0:
            self.vsp = 0

        self.move(hsp, self.vsp, groups)

    def move(self, x, y, groups):
        dx = x
        dy = y
        while self.check_collision(0, dy, groups['box']):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, groups['box']):
            dx -= numpy.sign(dx)


        for _ in groups['coin']:
            _.coin_animation(dx, dy)
        for group in groups.values():
            for _ in group:
                _.move(-dx, -dy)

    def move_boxs(boxx):
        for box in boxx:
            box.centerx -= 1
        return boxx

    def check_collision(self, x, y, grounds):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)
        self.rect.move_ip([-x, -y])
        return collide


class Box(Sprite):
    def __init__(self, startx, starty, img="boxAlt.png"):
        super().__init__(img, startx, starty)
class Lava(Box):
    def __init__(self, startx, starty):

        super().__init__(startx, starty, img='Lava.png')

class GG(Box):
  def __init__(self, startx, starty):

      super().__init__(startx, starty, img='GG.png')
def End():
  GGS.play()
  X = 2500
  Y = 900 
  white = (255, 255, 255)
  gold = (255,215,0)
  black = (255, 255, 255)
  display_surface = pygame.display.set_mode((X, Y))
  pygame.display.set_caption('Show Text')
  font = pygame.font.Font('freesansbold.ttf', 50)
  text = font.render('Play Again?', True, gold, white)
  text2 = font.render('Congrats! You Won!', True, gold, white)
  display_surface.blit(heheheha, [0, 0])

  pygame.display.update()  
  
class DeathBox(Box):
    def __init__(self, startx, starty):

        super().__init__(startx, starty, img='DEATH.png')

class Spike(Box):
    def __init__(self, startx, starty):

        super().__init__(startx, starty, img='Spike.png')

def reset():

  X = 1200
  Y = 600  
  white = (255, 255, 255)
  red = (255, 0, 0)
  black = (0, 0, 0)
  display_surface = pygame.display.set_mode((X, Y))


  pygame.display.set_caption('Show Text')
  print(deathcycle)
  deathnote =random.choices(deathcycle)
  font = pygame.font.Font('freesansbold.ttf', 50)
  text = font.render(deathnote[0]
+", Respawning...", True, red)
  # time.sleep(1)
  pygame.display.update()
  textRect = text.get_rect()
  textRect.center = (X // 2.3, Y // 2.3)
  player = Player(100, 200)
  player.is_alive = False
  display_surface.blit(heheheheha, [0, 0])  
  display_surface.blit(text, textRect)
  pygame.display.update()
  player = Player(100, 200)
  player.is_alive = False


def main2():
    time.sleep(.4)
    mixer.music.set_volume(0.7)
    mixer.music.load("idleMusic.wav")
    mixer.music.play(-1)
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(100, 200)   
    groups = {}
    groups['enemy'] = pygame.sprite.Group()
    groups['lava'] = pygame.sprite.Group()
    groups['death'] = pygame.sprite.Group()
    groups['box'] = pygame.sprite.Group()
    groups['coin'] = pygame.sprite.Group()
    groups['spike'] = pygame.sprite.Group()
    groups['GG'] = pygame.sprite.Group()
    for bx in range(0, 400, 70):
        box_ = Box(bx, 310)

        groups['box'].add(box_)
    groups["enemy"].add(Enemy(300, 100))
    groups['box'].add(Box(570, 100))
    groups['box'].add(Box(570, 30))      
    groups['box'].add(Box(570, -40))      
    groups['box'].add(Box(570, -110))      
    groups['box'].add(Box(570, -180))      
    groups['box'].add(Box(570, -250))      
    groups['box'].add(Box(570, 170))      
    groups['box'].add(Box(570, 240))      
    groups['box'].add(Box(570, 310))
    groups['box'].add(Box(570, -320))
    groups['box'].add(Box(570, 380))
    groups['box'].add(Box(500, 380))
    groups['box'].add(Box(430, 380))
    groups['box'].add(Box(360, 380))
    groups['lava'].add(Lava(500, 310))       
    groups['lava'].add(Lava(431, 310))       
    groups['lava'].add(Lava(362, 310))       
    groups['box'].add(Box(500, 100))  
    groups['box'].add(Box(300, -100))  
    groups['box'].add(Box(230, -100))  
    groups['box'].add(Box(160, -100))  
    groups['box'].add(Box(90, -100))  
    groups['box'].add(Box(20, -100))  
    groups['box'].add(Box(-50, -100))  
    groups['box'].add(Box(-120, -100))  
    groups['box'].add(Box(-190, -100))  
    groups['box'].add(Box(-260, -100))  
    groups['box'].add(Box(-330, -100))
    groups['box'].add(Box(580, -400))  
    groups['box'].add(Box(510, -400))  
    groups['box'].add(Box(440, -400)) 
    groups['box'].add(Box(370, -400))
    groups['box'].add(Box(300, -400))  
    groups['box'].add(Box(230, -400))  
    # groups['enemy'].add(Enemy(50, -50))  
    groups['spike'].add(Spike(100, -160))  
    groups['spike'].add(Spike(30, -160))  
    groups['spike'].add(Spike(-40, -160))  
    groups['spike'].add(Spike(170, -160))  
    groups['box'].add(Box(230, -400))  
    groups['box'].add(Box(160, -400))  
    groups['box'].add(Box(90, -400))  
    groups['box'].add(Box(20, -400))  
    groups['box'].add(Box(-50, -400))  
    groups['box'].add(Box(-120, -400))  
    groups['box'].add(Box(-190, -400))  
    groups['box'].add(Box(-260, -400))  
    groups['box'].add(Box(-330, -400))
    groups['box'].add(Box(-330, -30))
    groups['box'].add(Box(-330, 40))
    groups['box'].add(Box(-330, 110))
    groups['box'].add(Box(-330, 180))
    groups['box'].add(Box(-400, 180))
    groups['spike'].add(Spike(-400, 120))
    groups['box'].add(Box(-330, 250))
    groups['box'].add(Box(-330, 320))
    # groups['box'].add(Box(0, 240))
    groups['box'].add(Box(0, 170))
    groups['box'].add(Box(0, 100))
    groups['box'].add(Box(0, 30))
    groups['box'].add(Box(0, -40))
    groups['box'].add(Box(-700, 70))
    groups['coin'].add(Coin(-700, 10))
    groups['box'].add(Box(-770, 0))
    groups['box'].add(Box(-770, 420))
    groups['box'].add(Box(-770, 490))
    groups['box'].add(Box(-770, 560))
    groups['box'].add(Box(-770, 70))
    groups['box'].add(Box(-770, 140))
    groups['box'].add(Box(-770, 210))
    groups['box'].add(Box(-770, -70))
    groups['box'].add(Box(-770, 280))
    groups['box'].add(Box(-770, 350))
    groups['box'].add(Box(-770, -140))
    groups['box'].add(Box(-770, -210))
    groups['box'].add(Box(-770, -280))
    groups['box'].add(Box(-770, -350))
    groups['box'].add(Box(-770, -420))
    groups['box'].add(Box(-770, -490))
    groups['box'].add(Box(-770, 700))
    groups['box'].add(Box(-840, 700))
    groups['box'].add(Box(-910, 700))
    groups['box'].add(Box(-980, 700))
    groups['box'].add(Box(-1050, 700))
    groups['box'].add(Box(-1120, 700))
    groups['box'].add(Box(-1190, 700))
    groups['box'].add(Box(-1190, 630))  
    groups['box'].add(Box(-1190, 560)) 
    groups['box'].add(Box(-1190, 490))  
    groups['box'].add(Box(-1190, 420))
    groups['box'].add(Box(-1120, 420))
    groups['coin'].add(Coin(-1120, 490))
    groups['box'].add(Box(-1050, 420))  
    groups['box'].add(Box(-980, 420)) 
    groups['box'].add(Box(-910, 420)) 
    groups['box'].add(Box(-840, 420))     
    groups['box'].add(Box(-770, 420))  
    groups['box'].add(Box(-700, 700))
    groups['box'].add(Box(-630, 700))
    groups['box'].add(Box(-560, 700))
    groups['box'].add(Box(-490, 700))
    groups['box'].add(Box(-420, 700))
    groups['box'].add(Box(-350, 700))
    groups['box'].add(Box(-280, 700))
    groups['box'].add(Box(-210, 700))
    groups['box'].add(Box(-140, 700))
    groups['box'].add(Box(-70, 700))
    groups['box'].add(Box(0, 700))
    groups['lava'].add(Lava(69, 700))       
    groups['lava'].add(Lava(138, 700))       
    groups['lava'].add(Lava(207, 700))       
    groups['lava'].add(Lava(276, 700))       
    groups['box'].add(Box(69, 769))       
    groups['box'].add(Box(138, 769))       
    groups['box'].add(Box(207, 769))       
    groups['box'].add(Box(276, 769))       
    groups['box'].add(Box(345, 700))
    groups['box'].add(Box(415, 700))
    groups['GG'].add(GG(415, 597))
    groups['coin'].add(Coin(180, 500))       





    for dbx in range(-2000, 4000, 70):
        deathbox_ = DeathBox(dbx, 1000)
        groups['death'].add(deathbox_)



    
    while player.is_alive:

        pygame.event.pump()
        player.update(groups)

        
        screen.fill(BACKGROUND)

        player.draw(screen)

        for group in groups.values():
            group.draw(screen)
        pygame.display.flip()

        clock.tick(60)

    if player.is_alive == False:
      
      main()

if __name__ == "__main__":
    main2()
