import pygame, numpy
from abc import ABC, abstractmethod
WIDTH = 4000
HEIGHT = 900
BACKGROUND = (0,255,255)



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



class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__("p1_front.png", startx, starty)
        self.stand_image = self.image
        self.jump_cycle =   pygame.image.load("p1_jump01.png")

        self.walk_cycle = [pygame.image.load(f"p1_walk{i:0>2}.png") for i in range(1,13)]
        self.animation_index = 0
        self.facing_left = False

        self.speed = 8
        self.jumpspeed = 20
        self.vsp = 0
        self.gravity = 1
        self.min_jumpspeed = 4
        self.prev_key = pygame.key.get_pressed()

    def walk_animation(self):
        self.image = self.walk_cycle[self.animation_index]
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.animation_index < len(self.walk_cycle)-1:
            self.animation_index += 1
        else:
            self.animation_index = 0

    def jump_animation(self):
        self.image = self.jump_cycle
        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)

    def __init__(move_to_corner):
      (startx, starty) = (700, 700)

    def update(self, box_group, coin_group):
        hsp = 0
        onground = self.check_collision(0, 1, box_group)
        inCoin = self.check_collision(0, 1, coin_group)

        if inCoin:
          for i in (coin_group):
            Coin.move_to_corner
          
          
          #get specific coin object from the coin_group, 
          # then move that specific coin 
        
        # check keys
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
            self.vsp = -self.jumpspeed
        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed

        self.prev_key = key

        # gravity
        if self.vsp < 10 and not onground:  # 9.8 rounded up

            self.jump_animation()
            self.vsp += self.gravity

        if onground and self.vsp > 0:
            self.vsp = 0

        # movement
        self.move(hsp, self.vsp, box_group)

    def move(self, x, y, box_group):
        dx = x
        dy = y
        self.center = [Player]
        while self.check_collision(0, dy, box_group):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, box_group):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])

    def check_collision(self, x, y, grounds):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)
        self.rect.move_ip([-x, -y])
        return collide
      
vec = pygame.math.Vector2
class camera:
  def __init(self, player):
    self.player = player
    self.offset = vec(0,0)
    self.offset_float = vec(0,0)
    self.DISPLAY_W, self.DISPLAY_H - 480, 270
    self.CONST = vec(-self.DISPLAY_W / 2 -self.player.ground + 20)

    def setmethod(self,method):
      self.method = method
    
    def scroll(self):
      self.method.scroll()
class CamScroll(ABC):
  def __innit__(self, camera, player): 
    self.camera = camera
    self.player = player 
  @abstractmethod
  def scroll(self):
      pass

class Follow(CamScroll):
  def __innit__(self, camera, player):
    CamScroll.__innit__(self, camera, player)

  def scroll(self):
    self.camera.offset_float.x += (self.player.rect.x -self.camera.offset_float.x + self.camera.CONST.x)
    self.camera.offset_float.y += (self.player.rect.x -self.camera.offset_float.y + self.camera.CONST.y)
    self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
# box/coin
class Box(Sprite):
    def __init__(self, startx, starty):
        super().__init__("boxAlt.png", startx, starty)

class Coin(Sprite):
    
    def __init__(self, startx, starty):
        super().__init__("p1_Coin.png", startx, starty)


    
    def update():
      # move to corner and increase count by 1
      pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    player = Player(100, 200)
    box_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    for bx in range(0, 4000, 70):
        box_group.add(Box(bx, 300))

    box_group.add(Box(231, 120)) 
    box_group.add(Box(32, 23)) 
    box_group.add(Box(32, 92))
    box_group.add(Box(32, 161))
    box_group.add(Box(32, 230)) 
    coin_group.add(Coin(231, 60)) 
    while True:
        pygame.event.pump()
        player.update(box_group, coin_group)



        # Draw loop
        screen.fill(BACKGROUND)
        player.draw(screen)
        box_group.draw(screen)
        coin_group.draw(screen)
        pygame.display.flip()

        clock.tick(60)
if __name__ == "__main__":
    main()