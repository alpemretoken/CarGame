

from turtle import speed, window_height, window_width
import pygame
import time
import math

from pyparsing import White
from funcs import scale_image, blit_rotate_center

grass = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
track = scale_image(pygame.image.load("imgs/track2.png"), 0.68)
our_car = scale_image(pygame.image.load("imgs/red-car.png"), 0.55)
opponent_car = scale_image(pygame.image.load("imgs/green-car.png"), 0.55)
score = scale_image(pygame.image.load("imgs/score.png"),0.2)
finish = scale_image(pygame.image.load("imgs/finish.png"),0.80)
roadobject = scale_image(pygame.image.load("imgs/speed.png"),0.05)
barrier1 = scale_image(pygame.image.load("imgs/barrier1.png"),0.05)

WIDTH, HEIGHT = track.get_width(), track.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

FPS = 60


class Vehicle:
    def __init__(self, maxspeed, rotationspeed):
        self.img = self.IMG
        self.maxspeed = maxspeed
        self.vel = 0
        self.rotationspeed = rotationspeed
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.05
        

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotationspeed
        elif right:
            self.angle -= self.rotationspeed

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.maxspeed)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        if self.vel > 0:
            self.vel = min(self.vel - self.acceleration / 2)
        elif self.vel - self.acceleration < 0:
            self.vel=0
        else:
            self.vel = 0
        self.move()

class OurCar(Vehicle):
    IMG = our_car
    def __init__(self, maxspeed, rotationspeed):
        super().__init__(maxspeed, rotationspeed)
        self.score = 0


    START_POS = (600, 300)

class Opponent_Car(Vehicle):
    IMG = opponent_car
    START_POS = (640,300)

class Road_Objects:
    IMG = roadobject
    def __init__(self,x_coordinate,y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate
class Boost(Road_Objects):
    pass
class Barrier(Road_Objects):
    pass
class Bullet:
    pass


def draw(win, images, our_car, opponent_car):
    for img, pos in images:
        win.blit(img, pos)
    opponent_car.draw(win)
    our_car.draw(win)
    pygame.display.update()


run = True
clock = pygame.time.Clock()
our_car = OurCar(3, 3)
opponent_car = Opponent_Car(10, 3)

images = [(grass, (0, 0)), (track, (0, 0)),(score, (0, 0)),(finish, (590,300)),(roadobject, (613,500)),(barrier1, (640,350))]

while run:
    clock.tick(FPS)
   
    draw(WIN, images, our_car, opponent_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    

    our_car.score+=0.1
    keys = pygame.key.get_pressed()
    moved = False 
    if keys[pygame.K_LEFT] :
        our_car.rotate(left=True)
    if keys[pygame.K_RIGHT] :
        our_car.rotate(right=True)
    if keys[pygame.K_DOWN] :
        our_car.reduce_speed()
    if keys[pygame.K_UP] :
        moved = True
        our_car.move_forward()

    if not moved:
        our_car.reduce_speed()
    
    if keys[pygame.K_a]:
        opponent_car.rotate(left=True)
    if keys[pygame.K_d]:
        opponent_car.rotate(right=True)
    if keys[pygame.K_s]:
        opponent_car.reduce_speed()
    if keys[pygame.K_w]:
        moved = True
        opponent_car.move_forward()

    if not moved:
        opponent_car.reduce_speed()
    



pygame.quit()
print(our_car.score)