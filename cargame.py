



from matplotlib.pyplot import sca
import pygame
import time
import math
from funcs import scale_image, blit_rotate_center


grass = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)
track = scale_image(pygame.image.load("imgs/track.png"), 0.75)
track_border = scale_image(pygame.image.load("imgs/track-border.png"),0.75)
track_border_mask = pygame.mask.from_surface(track_border)
red_car = scale_image(pygame.image.load("imgs/red-car.png"), 0.25)
green_car = scale_image(pygame.image.load("imgs/green-car.png"), 0.25)
score = scale_image(pygame.image.load("imgs/score.png"),0.2)
finish = scale_image(pygame.image.load("imgs/finish.png"),0.650)
finish_mask = pygame.mask.from_surface(finish)
finish_position = (115,200)
speed = scale_image(pygame.image.load("imgs/speed.png"),0.05)
speed_mask = pygame.mask.from_surface(speed)
speed_position = (50,180)
barrier1 = scale_image(pygame.image.load("imgs/barrier1.png"),0.05)
barrier1_mask = pygame.mask.from_surface(barrier1)
barrier1_position = (613,500)

bullet = scale_image(pygame.image.load("imgs/bullet.png"),0.1)

WIDTH, HEIGHT = track.get_width(), track.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Race Game")

FPS = 60


class Vehicle:
    def __init__(self, maxspeed, rotationspeed):
        self.img = self.IMG
        self.maxspeed = maxspeed
        self.speed = 0
        self.rotationspeed = rotationspeed
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotationspeed
        elif right:
            self.angle -= self.rotationspeed

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.speed = min(self.speed + self.acceleration, self.maxspeed)
        self.move()
    def move_backward(self):
        self.speed = max(self.speed - self.acceleration, -self.maxspeed/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        self.vertical = math.cos(radians) * self.speed
        self.horizontal = math.sin(radians) * self.speed

        self.y -= self.vertical
        self.x -= self.horizontal

    def reduce_speed(self):
        if self.speed-self.acceleration > 0:
            self.speed = self.speed - self.acceleration
        else:
            self.speed=0
        self.move()
    
    def collusion(self,mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def stop(self):
        if self.speed >= 0:
            self.speed = -2
        else:
            self.speed = 1
        self.move()

    def restart(self):
        self.x, self.y = self.START_POS

    def speed_up(self):
        pass


class OurCar(Vehicle):
    IMG = red_car
    def __init__(self, maxspeed, rotationspeed):
        super().__init__(maxspeed, rotationspeed)
        self.score = 0
    START_POS = (130, 150)

class Opponent_Car(Vehicle):
    IMG = green_car
    START_POS = (150,150)

class Road_Objects:
    IMG = speed
    def __init__(self,x_coordinate,y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate
class Boost(Road_Objects):
    pass
class Barrier(Road_Objects):
    pass
class Bullet:
    IMG = bullet
    
    def __init__(self):
        self.position_x = our_car.x
        self.position_y = our_car.y
        self.img = self.IMG
        self.angle = our_car.angle

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.position_x, self.position_y), self.angle)
    
    def fire(self):
        
        radians = math.radians(our_car.angle)
        vertical_speed = math.cos(radians) * 1
        horizontal_speed = math.sin(radians) * 1
        self.position_x -= horizontal_speed*1
        self.position_y -= vertical_speed*1
        pygame.display.update()

def draw(win, images, our_car, opponent_car):
    for img, pos in images:
        win.blit(img, pos)
    opponent_car.draw(win)
    our_car.draw(win)
    pygame.display.update()




run = True
clock = pygame.time.Clock()
our_car = OurCar(4, 4)
opponent_car = Opponent_Car(4, 4)
bullet1 = Bullet()
images = [(grass, (0, 0)), (track, (0, 0)),(score, (0, 0)),(finish, (115,200)),
(speed, (50,180)),(barrier1, (613,500)),(track_border,(0,0))]

def our_car_move(our_car):
        
    keys = pygame.key.get_pressed()
    moved = False 
    if keys[pygame.K_LEFT] :
        our_car.rotate(left=True)
    if keys[pygame.K_RIGHT] :
        our_car.rotate(right=True)
    if keys[pygame.K_DOWN] :
        our_car.move_backward()
        moved = True
    if keys[pygame.K_UP] :
        moved = True
        our_car.move_forward()

    if not moved:
        our_car.reduce_speed()

def opponent_car_move(opponent_car):
    keys = pygame.key.get_pressed()
    moved = False 
    if keys[pygame.K_a]:
        opponent_car.rotate(left=True)
    if keys[pygame.K_d]:
        opponent_car.rotate(right=True)
    if keys[pygame.K_s]:
        opponent_car.move_backward()
        moved = True
    if keys[pygame.K_w]: 
        moved = True
        opponent_car.move_forward()

    if not moved:
        opponent_car.reduce_speed()


while run:
    clock.tick(FPS)
   
    draw(WIN, images, our_car, opponent_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    

    our_car.score+=0.1
    our_car_move(our_car)
    opponent_car_move(opponent_car)
    keys = pygame.key.get_pressed()
    x = True
    if keys[pygame.K_x]:
        bullet1.draw(WIN)
        bullet1.fire()
        

            
    
    finish_poi_collide = our_car.collusion(finish_mask,*finish_position)
    finish_poi_collide2 = opponent_car.collusion(finish_mask, *finish_position)
    speed_poi_collide = our_car.collusion(speed_mask,*speed_position)
    barrier_poi_collide = our_car.collusion(barrier1_mask,*barrier1_position)

    if barrier_poi_collide != None:
        our_car.stop()
    if our_car.collusion(track_border_mask) != None :
        our_car.stop()
    if opponent_car.collusion(track_border_mask) != None:
        opponent_car.stop()

    if speed_poi_collide != None:
        our_car.maxspeed += 3
        our_car.speed += 3
    else:
        our_car.maxspeed = 4
    
    if finish_poi_collide != None: 
        if finish_poi_collide[1] ==0:
            our_car.stop()
        else:
            our_car.restart() 
            opponent_car.restart()
    if finish_poi_collide2 != None: 
        if finish_poi_collide2[1] == 0:
            opponent_car.stop()
        else:
            opponent_car.restart()
            our_car.restart()

    
   
pygame.quit()
print(our_car.score)