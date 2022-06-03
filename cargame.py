




from turtle import position
import pygame
import time
import math

from funcs import scale_image, blit_rotate_center

a = 1.23
grass = scale_image(pygame.image.load("imgs/grass.jpg"), 2*a)
heart1 = scale_image(pygame.image.load("imgs/heart.png"),0.08*a)
heart1_mask = pygame.mask.from_surface(heart1)
heart1_position = (750,700)
track = scale_image(pygame.image.load("imgs/ourtrack.png"), a)
track_border = scale_image(pygame.image.load("imgs/ourtrack_border.png"),a)
track_border_mask = pygame.mask.from_surface(track_border)
red_car = scale_image(pygame.image.load("imgs/RedBull.png"), 0.13*a)
green_car = scale_image(pygame.image.load("imgs/green-car.png"), (a*0.6)/a)
score = scale_image(pygame.image.load("imgs/score.png"),(a*0.2)/a)
finish = scale_image(pygame.image.load("imgs/finish.png"),1.6*a)
finish_mask = pygame.mask.from_surface(finish)
finish_position = (350,650)
speed1 = scale_image(pygame.image.load("imgs/speed.png"),a*0.1/a)
speed_mask = pygame.mask.from_surface(speed1)
speed_position = (125,250)
barrier1 = scale_image(pygame.image.load("imgs/barrier1.png"),(a*0.08)/a)
barrier1_mask = pygame.mask.from_surface(barrier1)
barrier1_position = (613,500)
resume = scale_image(pygame.image.load("imgs/resume.png"),a/2)
resume_position = (500,300)
quitgame = scale_image(pygame.image.load("imgs/exitgame.png"),a/2)
quitgame_position =(380,360)
bullet = scale_image(pygame.image.load("imgs/bullet.png"),(a*0.2)/a)

WIDTH, HEIGHT = track.get_width(), track.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Race Game")

FPS = 60

class Game:
    def __init__(self) -> None:
        pass

    def pause(self):
        images.append((resume,resume_position))
        images.append((quitgame,quitgame_position))
        our_car.speed = 0
        opponent_car.speed = 0
    def resume(self):
        images.pop()
        images.pop()
        
class Vehicle:
    def __init__(self, maxspeed, rotationspeed):
        self.img = self.IMG
        self.maxspeed = maxspeed
        self.speed = 0
        self.rotationspeed = rotationspeed
        self.angle = 90
        self.x, self.y = self.START_POS
        self.acceleration = 1
        

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
            self.speed = -8
        else:
            self.speed = 8
        self.move()

    def restart(self):
        self.x, self.y = self.START_POS
        self.angle = 90
        opponent_car.maxspeed +=1

    def speed_up(self):
        pass

    def decreaseHP(self):
        our_car.HP -= 1

    def increase_max_speed(self):
        our_car.maxspeed += 3
    
    def instant_speed(self):
        our_car.speed += 3

    def DidYouTouch(self):
        pass

    def increase_HP(self):
        our_car.HP += 1
        
class OurCar(Vehicle):
    IMG = red_car
    def __init__(self, maxspeed, rotationspeed):
        super().__init__(maxspeed, rotationspeed)
        self.score = 0
        self.HP = 5
    START_POS = (300, 680)

class Opponent_Car(Vehicle):
    IMG = green_car
    START_POS = (300,730)

class Road_Objects:
    
    def __init__(self,x_coordinate,y_coordinate,img):
        self.x = x_coordinate
        self.y = y_coordinate
        self.img = img
    
    def die(self):
        images.pop(images.index((speed, (speed.x,speed.y))))
class Boost(Road_Objects):
    IMG = speed1
    
class Barrier(Road_Objects):
    IMG = barrier1 
    
class Heart(Road_Objects):
    IMG = heart1
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
        

def draw(win, images, our_car, opponent_car):
    for img, pos in images:
        win.blit(img, pos)
    opponent_car.draw(win)
    our_car.draw(win)
    
    pygame.display.update()




run = True
clock = pygame.time.Clock()
our_car = OurCar(5, 4)
opponent_car = Opponent_Car(5, 4)
barrier = Barrier(613,500,barrier1)
speed = Boost(125,250,speed1)
heart = Heart(750,700,heart1)
game = Game()
images = [(grass, (0, 0)), (track, (0, 0)),(score, (0, 0)),(finish, finish_position),
(speed.img, (speed.x,speed.y)),(barrier.img, (barrier.x,barrier.y)),(track_border,(0,0)),(heart.img,(heart.x,heart.y))]

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
y = True
x = False
z = True
t = True
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

    
    if keys[pygame.K_x]:
        bullet1 = Bullet()
        bullet1.draw(WIN)
        bullet1.fire()
        firstspeed_x = our_car.horizontal
        firstspeed_y = our_car.vertical
        x = True
    if x == True:
        bullet1.draw(WIN)   
        bullet1.position_x -= firstspeed_x
        bullet1.position_y -= firstspeed_y
        if (barrier.x-15) <= bullet1.position_x <= (barrier.x + 15) and  (barrier.y-50)<= bullet1.position_y <=(barrier.y+50):
                
                print("öl laaa")
                y = False
            

        pygame.display.update()
    
        

            
    
    finish_poi_collide = our_car.collusion(finish_mask,*finish_position)
    finish_poi_collide2 = opponent_car.collusion(finish_mask, *finish_position)
    speed_poi_collide = our_car.collusion(speed_mask,*speed_position)
    speed_poi_collide2 = opponent_car.collusion(speed_mask,*speed_position)
    barrier_poi_collide = our_car.collusion(barrier1_mask,*barrier1_position)
    barrier_poi_collide2 = opponent_car.collusion(barrier1_mask,*barrier1_position)
    heart_poi_collide = our_car.collusion(heart1_mask, *heart1_position)
    if heart_poi_collide != None:
        if t == True:
            our_car.increase_HP()
            heart.die()
            t = False
    if barrier_poi_collide != None:
        if y == True:
            our_car.stop()
            our_car.decreaseHP()
    if our_car.collusion(track_border_mask) != None :
        our_car.stop()
        our_car.decreaseHP()
    if opponent_car.collusion(track_border_mask) != None:
        opponent_car.stop()

    if speed_poi_collide != None:
        if z == True:
            our_car.increase_max_speed()
            our_car.instant_speed()
            speed.die()
            z = False
    else:
        our_car.maxspeed = 5
    
    if speed_poi_collide2 != None:
        opponent_car.increase_max_speed()
        opponent_car.instant_speed()
    else:
        opponent_car.maxspeed = 5
    

    if finish_poi_collide != None: 
        if finish_poi_collide[0] ==0:
            our_car.stop()
        else:
            our_car.restart() 
            opponent_car.restart()
    if finish_poi_collide2 != None: 
        if finish_poi_collide2[0] == 0:
            opponent_car.stop()
        else:
            opponent_car.restart()
            our_car.restart()
    if keys[pygame.K_p]:  
        game.pause()
    if keys[pygame.K_r]:
        game.resume()
   # if our_car.HP ==0:
   #     run = False
   
pygame.quit()
print(our_car.score)